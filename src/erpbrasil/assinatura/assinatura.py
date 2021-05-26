# coding=utf-8

from base64 import b64encode

import signxml
import xmlsec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from endesive import pdf
from endesive import signer
from endesive import xades
from lxml import etree
from OpenSSL import crypto
from xmlsec import constants as consts


class Assinatura(object):

    def __init__(self, certificado):
        self.certificado = certificado
        self.cert = certificado._cert
        self.chave_privada = certificado._chave
        self.senha = certificado._senha

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

        ns = dict()
        ns[None] = signer.namespaces['ds']
        signer.namespaces = ns

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

    def _checar_certificado(self):
        if not self.chave_privada:
            raise Exception("Certificado não existe.")

    def assina_nfse(self, template):
        self._checar_certificado()

        key = xmlsec.Key.from_memory(
            self.chave_privada,
            format=xmlsec.constants.KeyDataFormatPem,
            password=self.senha,
        )

        signature_node = xmlsec.template.create(
            template,
            c14n_method=consts.TransformInclC14N,
            sign_method=consts.TransformRsaSha1,
        )
        template.append(signature_node)
        ref = xmlsec.template.add_reference(
            signature_node, consts.TransformSha1, uri=""
        )

        xmlsec.template.add_transform(ref, consts.TransformEnveloped)
        xmlsec.template.add_transform(ref, consts.TransformInclC14N)

        ki = xmlsec.template.ensure_key_info(signature_node)
        xmlsec.template.add_x509_data(ki)

        ctx = xmlsec.SignatureContext()
        ctx.key = key

        ctx.key.load_cert_from_memory(self.cert,
                                      consts.KeyDataFormatPem)

        ctx.sign(signature_node)
        return etree.tostring(template, encoding=str)

    def assina_pdf(self, arquivo, dados_assinatura, altoritimo='sha256'):
        return pdf.cms.sign(
            datau=arquivo,
            udct=dados_assinatura,
            key=self.certificado.key,
            cert=self.certificado.cert,
            othercerts=self.certificado.othercerts,
            algomd=altoritimo
        )

    @staticmethod
    def verifica_pdf(arquivo, certificados_de_confianca):
        return pdf.verify(
            data=arquivo,
            trusted_cert_pems=certificados_de_confianca
        )

    def assina_xml(self, arquivo):
        def signproc(tosign, algosig):
            key = self.certificado.key
            signed_value_signature = key.sign(
                tosign,
                padding.PKCS1v15(),
                getattr(hashes, algosig.upper())()
            )
            return signed_value_signature

        cert = self.certificado.cert
        certcontent = signer.cert2asn(cert).dump()

        cls = xades.BES()
        doc = cls.enveloping(
            'documento.xml', arquivo, 'application/xml',
            cert, certcontent, signproc, False, True
        )

        return etree.tostring(
            doc, encoding='UTF-8', xml_declaration=True, standalone=False
        )

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

    def assina_tag(self, message):
        chave_privada = self.certificado._pkcs12.get_privatekey()
        assianado = crypto.sign(chave_privada, message, "SHA1")
        return b64encode(assianado).decode()

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
