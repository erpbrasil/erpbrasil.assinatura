import base64
import datetime
import os
import tempfile

import pytz
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.x509.oid import NameOID

from .excecoes import CertificadoExpirado
from .excecoes import CertificadoSenhaInvalida
from .excecoes import ErroDeLeituraDeArquivo


class Certificado():
    """Classe para representar o certificado digital"""

    def __init__(self, arquivo, senha, raise_expirado=True):
        """Permite informar um arquivo PFX binario ou o path do arquivo"""

        self._senha = self._encode_senha(senha)

        if os.path.exists(arquivo):
            try:
                self._arquivo = open(arquivo, "rb").read()
            except IOError as io_error:
                raise ErroDeLeituraDeArquivo("Erro ao ler o arquivo!!!") from io_error
        elif isinstance(arquivo, bytes):
            self._arquivo = base64.b64decode(arquivo)
        elif isinstance(arquivo, str):
            self._arquivo = arquivo

        try:
            self.key, self.cert, self.othercerts = self._load_key_and_certificates()
        except ValueError as value_error:
            raise CertificadoSenhaInvalida(
                "Certificado ou senha inválida!!!"
            ) from value_error

        if raise_expirado and self.expirado:
            raise CertificadoExpirado("Certificado Expirado!!!")

        self._chave = self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        self._cert = self.cert.public_bytes(encoding=serialization.Encoding.PEM)

    def _load_key_and_certificates(self):
        """
        :return:
        """
        return load_key_and_certificates(
            data=self._arquivo, password=self._senha, backend=default_backend()
        )

    @property
    def inicio_validade(self):
        """Pega a data inicial de validade do certificado"""
        return self.cert.not_valid_before.replace(tzinfo=pytz.UTC)

    @property
    def fim_validade(self):
        """Pega a data final de validade do certificado"""
        return self.cert.not_valid_after.replace(tzinfo=pytz.UTC)

    @property
    def emissor(self):
        """Pega o nome do emissor do certificado"""
        return self.cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @property
    def proprietario(self):
        """Pega o nome do proprietário do certificado"""
        return self.cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @property
    def cnpj_cpf(self):
        """Pega o CNPJ ou CPF do proprietário do certificado"""
        # As vezes tem o nome e cnpj_cpf do proprietário
        proprietario = self.proprietario
        if ":" in proprietario:
            cnpj_cpf = proprietario.rsplit(":", 1)[1]
            return cnpj_cpf
        return ""

    @property
    def expirado(self):
        """Verifica se o certificado está expirado"""
        today = datetime.datetime.today()
        if today > self.cert.not_valid_after:
            return True
        return False

    def cert_chave(self):
        """Retorna o certificado e a chave"""
        return self._cert.decode(), self._chave.decode()

    @staticmethod
    def _encode_senha(senha):
        if isinstance(senha, str):
            return senha.encode()
        return senha


class ArquivoCertificado():
    """Classe para ser utilizada quando for necessário salvar o arquivo
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

        tmp = os.fdopen(self.key_fd, "w")
        tmp.write(cert)

        tmp = os.fdopen(self.cert_fd, "w")
        tmp.write(key)

    def __enter__(self):
        return self.key_path, self.cert_path

    def __exit__(self, type, value, traceback):
        os.remove(self.key_path)
        os.remove(self.cert_path)


def save_cert_key(cert, key):
    """Salva o certificado e a chave em arquivos temporários"""
    cert_temp = tempfile.mkstemp()[1]
    key_temp = tempfile.mkstemp()[1]

    arq_temp = open(cert_temp, "w")
    arq_temp.write(cert)
    arq_temp.close()

    arq_temp = open(key_temp, "w")
    arq_temp.write(key)
    arq_temp.close()

    return cert_temp, key_temp
