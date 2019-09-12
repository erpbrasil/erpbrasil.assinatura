# coding=utf-8

import tempfile
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from OpenSSL import crypto
from pytz import UTC


from .excecoes import CertificadoExpirado


class Certificado(object):

    def __init__(self, arquivo, senha):
        """Permite informar um arquivo PFX binario ou o path do arquivo"""

        if isinstance(arquivo, str):
            self._arquivo = open(arquivo, 'rb').read()

        if isinstance(arquivo, bytes):
            self._arquivo = arquivo

        self._senha = senha

        # Salva o arquivo pfx no formato binario pkc12
        self._pkcs12 = crypto.load_pkcs12(self._arquivo,
                                          self._senha)

        # Extrai o certicicado
        self._cert = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                             self._pkcs12.get_certificate())

        # Extrai a chave
        self._chave = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                             self._pkcs12.get_privatekey())

        self._x509 = crypto.load_certificate(crypto.FILETYPE_PEM,
                                             self._cert)

        self._cn = ''
        for k, v in self._x509.get_issuer().get_components():
            k = k.decode('utf-8')
            v = v.decode('utf-8')
            if k == 'CN':
                self._cn = v.decode('utf-8')

        if self._x509.has_expired():
            raise CertificadoExpirado('Certificado Expirado!!!')

        self.key, self.cert, self.othercerts = \
            self._load_key_and_certificates()

    def inicio_validade(self):
        """Pega a data inicial de validade do certificado"""
        inicio_validade = datetime.strptime(
            self._x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
        return UTC.localize(inicio_validade)

    def fim_validade(self):
        """Pega a data final de validade do certificado"""
        fim_validade = datetime.strptime(
            self._x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        return UTC.localize(fim_validade)

    def emissor(self):
        """Pega o nome do emissor do certificado"""
        return self._cn

    def proprietario(self):
        """Pega o nome do proprietário do certificado"""
        if ':' in self._cn:
            proprietario = self._cn.rsplit(':', 1)[0]
        else:
            proprietario = self._cn
        return proprietario

    def cnpj(self):
        # As vezes tem o nome e CNPJ do proprietário
        cnpj = ''
        if ':' in self._cn:
            cnpj = self._cn.rsplit(':', 1)[1]
        return cnpj

    def cert_chave(self):
        """Retorna o certificado e a chave"""
        return self._cert.decode(), self._chave.decode()

    def pkcs12(self):
        """Retorna o arquivo pfx no formato binario pkc12"""
        return self._pkcs12

    def save_cert_key(self):
        cert, chave = self.get_cert_chave()
        cert_temp = tempfile.mkstemp()[1]
        key_temp = tempfile.mkstemp()[1]

        arq_temp = open(cert_temp, 'w')
        arq_temp.write(cert)
        arq_temp.close()

        arq_temp = open(key_temp, 'w')
        arq_temp.write(chave)
        arq_temp.close()

        return cert_temp, key_temp

    def _load_key_and_certificates(self):
        """
        :return:
        """
        return load_key_and_certificates(
            data=self.abre_arquivo(),
            password=self.senha,
            backend=default_backend()
        )
