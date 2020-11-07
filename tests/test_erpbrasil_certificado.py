# coding=utf-8

import os
from unittest import TestCase

from erpbrasil.assinatura.certificado import ArquivoCertificado
from erpbrasil.assinatura.certificado import Certificado


class Tests(TestCase):

    def setUp(self):
        self.certificado_caminho = os.environ.get(
            'certificado_nfe_caminho', 'tests/fixtures/dummy_cert.pfx')
        self.certificado_senha = os.environ.get(
            'certificado_nfe_senha', 'dummy_password')
        self.certificado = Certificado(
            self.certificado_caminho,
            self.certificado_senha,
            raise_expirado=False
        )

    def test_chave_cert(self):
        chave, certificado = \
            self.certificado.cert_chave()
        assert chave, certificado

    def test_atributos(self):
        self.certificado.inicio_validade
        self.certificado.fim_validade
        self.certificado.cert_chave
        self.certificado.emissor
        self.certificado.proprietario
        self.certificado.cnpj_cpf
        self.certificado.expirado

    def test_abertura_arquivo_temporariamente(self):
        caminho_key = caminho_cert = False
        with ArquivoCertificado(self.certificado, 'w') as (key, cert):
            caminho_key = key
            caminho_cert = cert
            self.assertTrue(os.path.exists(caminho_key))
            self.assertTrue(os.path.exists(caminho_cert))
        self.assertFalse(os.path.exists(caminho_key))
        self.assertFalse(os.path.exists(caminho_cert))
