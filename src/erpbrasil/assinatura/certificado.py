# coding=utf-8

import base64
import os
import tempfile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from OpenSSL import crypto
from pytz import UTC

from .excecoes import CertificadoExpirado
from .excecoes import CertificadoSenhaInvalida
from .excecoes import ErroDeLeituraDeArquivo


class Certificado(object):

    def __init__(self, arquivo, senha, raise_expirado=True):
        """Permite informar um arquivo PFX binario ou o path do arquivo"""

        self._senha = senha

        try:
            try:
                self._arquivo = base64.b64decode(arquivo)

                # Salva o arquivo pfx no formato binario pkc12
                self._pkcs12 = crypto.load_pkcs12(self._arquivo,
                                                  self._senha)
            except Exception:
                if isinstance(arquivo, bytes):
                    self._arquivo = arquivo
                elif isinstance(arquivo, str):
                    self._arquivo = open(arquivo, 'rb').read()

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

            self.key, self.cert, self.othercerts = \
                self._load_key_and_certificates()

        except IOError:
            raise ErroDeLeituraDeArquivo('Erro ao ler o arquivo!!!')
        except crypto.Error:
            raise CertificadoSenhaInvalida('Certificado ou senha inválida!!!')

        if raise_expirado and self._x509.has_expired():
            raise CertificadoExpirado('Certificado Expirado!!!')

    def _load_key_and_certificates(self):
        """
        :return:
        """
        return load_key_and_certificates(
            data=self._arquivo,
            password=self._senha.encode(),
            backend=default_backend()
        )

    @property
    def inicio_validade(self):
        """Pega a data inicial de validade do certificado"""
        return UTC.localize(self.cert.not_valid_before)

    @property
    def fim_validade(self):
        """Pega a data final de validade do certificado"""
        return UTC.localize(self.cert.not_valid_after)

    @property
    def emissor(self):
        """Pega o nome do emissor do certificado"""
        return self._x509.get_issuer().CN

    @property
    def proprietario(self):
        """Pega o nome do proprietário do certificado"""
        return self._x509.get_subject().CN

    @property
    def cnpj_cpf(self):
        # As vezes tem o nome e cnpj_cpf do proprietário
        proprietario = self.proprietario
        if ':' in proprietario:
            cnpj_cpf = proprietario.rsplit(':', 1)[1]
            return cnpj_cpf
        return ''

    @property
    def expirado(self):
        if self._x509.has_expired():
            return True
        return False

    def cert_chave(self):
        """Retorna o certificado e a chave"""
        return self._cert.decode(), self._chave.decode()

    def pkcs12(self):
        """Retorna o arquivo pfx no formato binario pkc12"""
        return self._pkcs12


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
