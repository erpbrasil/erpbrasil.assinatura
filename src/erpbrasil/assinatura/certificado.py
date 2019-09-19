# coding=utf-8

import os
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
                self._cn = v.encode('utf-8')


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

    def _load_key_and_certificates(self):
        """
        :return:
        """
        return load_key_and_certificates(
            data=self.abre_arquivo(),
            password=self.senha,
            backend=default_backend()
        )


class ArquivoCertificado(object):
    """ Classe para ser utilizada quando for necessário salvar o arquivo
    temporariamente, garantindo a segurança que o mesmo sera salvo e apagado
    rapidamente

    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha)

    with ArquivoCertificado(certificado, 'w') as (key, cert):
        print(key.name)
        print(cert.name)
    """

    def __init__(self, certificado, method):
        self.key_fd, self.key_path = tempfile.mkstemp()
        self.cert_fd, self.cert_path = tempfile.mkstemp()

        cert, key = certificado.cert_chave()

        tmp = os.fdopen(self.key_fd, 'w')
        tmp.write(cert)

        tmp = os.fdopen(self.cert_fd, 'w')
        tmp.write(key)

    def __enter__(self):
        return self.key_path, self.cert_path

    def __exit__(self, type, value, traceback):
        os.remove(self.key_path)
        os.remove(self.cert_path)
