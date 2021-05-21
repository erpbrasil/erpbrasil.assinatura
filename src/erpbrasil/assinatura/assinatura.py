# coding=utf-8
import sys
import signxml
from OpenSSL import crypto
from base64 import b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from endesive import pdf
from endesive import signer
from endesive import xades
from lxml import etree
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from re import sub, search
from hashlib import sha1


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

    def assina_nfse(self, xml_etree):

        signer = signxml.XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        )

        ns = dict()
        ns[None] = signer.namespaces['ds']
        signer.namespaces = ns

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

    def assina_pdf(self, arquivo, dados_assinatura, altoritimo='sha256'):
        return pdf.cms.sign(
            datau=arquivo,
            udct=dados_assinatura,
            key=self.certificado.key,
            cert=self.certificado.cert,
            othercerts=self.certificado.othercerts,
            algomd=altoritimo
        )

    def assina_tag(self, message):
        privateKeyContent = (self.certificado._chave).decode('utf-8')
        message = message.encode('utf-8')
        message = SHA.new(message)
        rsaKey = RSA.importKey(privateKeyContent)
        signer = PKCS1_v1_5.new(rsaKey)
        signature = signer.sign(message)
        return b64encode(signature).decode()

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
