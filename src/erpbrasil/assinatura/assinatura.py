import logging
from base64 import b64encode
from hashlib import sha1

import signxml
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree

_logger = logging.getLogger(__name__)


class XMLSignerWithSHA1(signxml.XMLSigner):
    """
    Extension of the `XMLSigner` class that adds support for the SHA1 hash algorithm
    to the XML signature process.
    Note:
        SHA1-based algorithms are not supported in the default configuration because
        they are not secure, but in the NF-e project, other more modern algorithms
        are still not accepted.
    """

    def check_deprecated_methods(self):
        "Override to disable deprecated Check"


class Assinatura(object):
    def __init__(self, certificado):
        self.certificado = certificado
        self.cert = certificado._cert
        self.chave_privada = certificado._chave
        self.senha = certificado._senha

    @classmethod
    def digest(self, text):
        hasher = sha1()
        hasher.update(str(text).encode("utf-8"))
        digest = hasher.digest()
        return b64encode(digest).decode("utf-8")

    def assina_xml(self, arquivo):
        signer = XMLSignerWithSHA1(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        root = etree.fromstring(arquivo)

        signed_root = signer.sign(
            root,
            key=self.certificado.key,
            cert=self.certificado._cert,
        )

        return etree.tostring(signed_root)

    @staticmethod
    def _normaliza_namespaces(root):
        """Devolve a arvore com a Signature no namespace ds de fato.

        A partir do signxml 4.2.2, com o namespace padrao ds
        (``signer.namespaces = {None: ds}``), a Signature nasce na arvore SEM
        namespace e so ganha o ds na serializacao. Buscas por
        ``{ds}Signature`` (e a relocacao da assinatura) deixam de achar o
        elemento. Serializar e reler normaliza; nas versoes anteriores e
        inofensivo.
        """
        return etree.fromstring(etree.tostring(root))

    def assina_xml2(
        self,
        xml_element,
        reference,
        getchildren=False,
        signature_algorithm="rsa-sha1",
        digest_algorithm="sha1",
    ):
        """Assina o elemento referenciado por ``Id``.

        SHA1 continua o padrao porque a SEFAZ ainda exige; webservices mais
        novos (ex.: NFS-e padrao nacional via NotaControl) rejeitam SHA1 e
        pedem ``signature_algorithm="rsa-sha256"``/``digest_algorithm="sha256"``.
        """
        for element in xml_element.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None
            if element.tail is not None and not element.tail.strip():
                element.tail = None

        signer = XMLSignerWithSHA1(
            method=signxml.methods.enveloped,
            signature_algorithm=signature_algorithm,
            digest_algorithm=digest_algorithm,
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        signer.excise_empty_xmlns_declarations = True
        signer.namespaces = {None: signxml.namespaces.ds}

        ref_uri = ("#%s" % reference) if reference else None

        # cert como PEM: todas as versoes do signxml (3.x, 4.x e 5.x) aceitam;
        # o objeto x509.Certificate solto nunca foi aceito (levantava TypeError)
        signed_root = signer.sign(
            xml_element,
            key=self.certificado.key,
            cert=self.certificado._cert,
            reference_uri=ref_uri,
        )
        signed_root = self._normaliza_namespaces(signed_root)

        if reference:
            element_signed = signed_root.find(".//*[@Id='%s']" % reference)
            # o documento pode ja trazer outras assinaturas (ex.: DPS assinada
            # dentro do lote): a que acabou de ser criada e a que referencia
            # este Id, nao a primeira que aparecer
            signature = next(
                (
                    sig
                    for sig in signed_root.iter(
                        "{http://www.w3.org/2000/09/xmldsig#}Signature"
                    )
                    if sig.find(
                        "{http://www.w3.org/2000/09/xmldsig#}SignedInfo/"
                        "{http://www.w3.org/2000/09/xmldsig#}Reference"
                    ).get("URI")
                    == ref_uri
                ),
                None,
            )

            if getchildren and element_signed is not None and signature is not None:
                child = element_signed.getchildren()
                child.append(signature)
            elif element_signed is not None and signature is not None:
                parent = element_signed.getparent()
                parent.append(signature)
        return etree.tostring(signed_root, encoding=str)

    def assina_nfse(self, xml_etree):
        signer = XMLSignerWithSHA1(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        signed_root = signer.sign(
            xml_etree,
            key=self.chave_privada,
            cert=self.cert,
        )
        signed_root = etree.tostring(signed_root, encoding=str)

        return signed_root

    def assina_string(self, message):
        private_key = self.certificado.key
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA1(),
        )
        return signature

    def sign_pkcs1v15_sha1(self, data):
        """
        Sign data using PKCS1v15 padding and SHA1 hash algorithm.

        This method is specifically tailored for the NFSe Paulistana RPS signing process.

        Args:
            data (bytes): Data to be signed.

        Returns:
            bytes: Generated signature.
        """
        private_key = self.certificado.key
        signature = private_key.sign(data, padding.PKCS1v15(), hashes.SHA1())
        return signature

    def assina_pdf(self, arquivo, dados_assinatura, algoritmo="sha256"):
        try:
            from endesive import pdf
        except ImportError:
            _logger.info(
                "assina_pdf requires the https://github.com/m32/endesive"
                "package but it is not bundled by default"
                "to avoid depending on pyopenssl which is deprecated"
            )
            return False
        return pdf.cms.sign(
            datau=arquivo,
            udct=dados_assinatura,
            key=self.certificado.key,
            cert=self.certificado.cert,
            othercerts=self.certificado.othercerts,
            algomd=algoritmo,
        )

    def verificar_assinatura_string(self, message, signature):
        public_key = self.certificado.key.public_key()
        return public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA1(),
        )
