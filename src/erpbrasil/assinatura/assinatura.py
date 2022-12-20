import logging
from base64 import b64encode
from hashlib import sha1

import signxml
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree

_logger = logging.getLogger(__name__)


class Assinatura(object):

    def __init__(self, certificado):
        self.certificado = certificado
        self.cert = certificado._cert
        self.chave_privada = certificado._chave
        self.senha = certificado._senha

    @classmethod
    def digest(self, text):
        hasher = sha1()
        hasher.update(str(text).encode('utf-8'))
        digest = hasher.digest()
        return b64encode(digest).decode('utf-8')

    def assina_xml(self, arquivo):
        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        )

        root = etree.fromstring(arquivo)

        signed_root = signer.sign(
            root,
            key=self.certificado.key,
            cert=self.certificado._cert,
        )

        return etree.tostring(signed_root)

    def assina_xml2(self, xml_element, reference, getchildren=False):
        for element in xml_element.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        )

        signer.namespaces = {"ds": "http://www.w3.org/2000/09/xmldsig#"}

        ref_uri = ('#%s' % reference) if reference else None

        signed_root = False
        try:
            signed_root = signer.sign(
                xml_element,
                key=self.certificado.key,
                cert=self.certificado.cert,
                reference_uri=ref_uri
            )
        except TypeError:
            signed_root = signer.sign(
                xml_element,
                key=self.certificado.key,
                cert=self.certificado._cert,
                reference_uri=ref_uri
            )

        if reference:
            element_signed = signed_root.find(".//*[@Id='%s']" % reference)
            signature = signed_root.find(
              ".//{http://www.w3.org/2000/09/xmldsig#}Signature"
            )

            if getchildren and element_signed is not None and signature is not None:
                child = element_signed.getchildren()
                child.append(signature)
            elif element_signed is not None and signature is not None:
                parent = element_signed.getparent()
                parent.append(signature)
        return etree.tostring(signed_root, encoding=str)

    def assina_nfse(self, xml_etree):

        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        )

        signed_root = signer.sign(
            xml_etree,
            key=self.chave_privada,
            cert=self.cert,
        )

        signed_root = etree.tostring(signed_root, encoding=str)

        signed_root = signed_root.replace('\r', '').replace('\n', '')

        return signed_root

    def assina_string(self, message):
        private_key = self.certificado.key
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA1()
        )
        return signature

    def assina_pdf(self, arquivo, dados_assinatura, algoritmo='sha256'):
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
            algomd=algoritmo
        )

    def verificar_assinatura_string(self, message, signature):
        public_key = self.certificado.key.public_key()
        return public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA1()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA1()
        )
