# coding=utf-8

from endesive import pdf, signer, xades
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Assinatura(object):

    def __init__(self, certificado):
        self.certificado = certificado

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
        doc = cls.build(
            'documento.xml', arquivo, 'application/xml',
            cert, certcontent, signproc, False, True
        )

        from lxml import etree

        return etree.tostring(
            doc, encoding='UTF-8', xml_declaration=True, standalone=False
        )
