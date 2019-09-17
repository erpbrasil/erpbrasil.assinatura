# coding=utf-8

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from OpenSSL import crypto


class Certificado(object):

    def __init__(self, caminho_arquivo, senha):
        self.caminho_arquivo = caminho_arquivo
        self.senha = str.encode(senha)
        self.key, self.cert, self.othercerts = \
            self._load_key_and_certificates()

    def abre_arquivo(self):
        return open(self.caminho_arquivo, 'rb').read()

    def separa_chave_certificado(self):
        """ Realiza a separação da chave e do certificado
        :return:
        """
        p12 = crypto.load_pkcs12(self.abre_arquivo(), self.senha)
        certificado = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                              p12.get_certificate())
        chave = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                       p12.get_privatekey())
        return chave, certificado

    def _load_key_and_certificates(self):
        """
        :return:
        """
        return load_key_and_certificates(
            data=self.abre_arquivo(),
            password=self.senha,
            backend=default_backend()
        )
