# coding=utf-8

from endesive import pdf


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

    def assina_xml(self):
        pass
