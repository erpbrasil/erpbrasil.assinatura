# coding=utf-8

import os
import unittest

from cryptography.exceptions import InvalidSignature

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/fixtures/dummy_cert.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'dummy_password')


class TestSignatureStringMethods(unittest.TestCase):

    def test_positive_signature_string(self):
        certificado = Certificado(
            certificado_nfe_caminho,
            certificado_nfe_senha,
            raise_expirado=False
        )
        assinador = Assinatura(certificado)
        text = 'test of signature'.encode('utf-8')
        signature = assinador.assina_string(text)
        result = assinador.verificar_assinatura_string(text, signature)
        self.assertEqual(result, None)

    def test_false_positive_signature_string(self):
        certificado = Certificado(
            certificado_nfe_caminho,
            certificado_nfe_senha,
            raise_expirado=False
        )
        assinador = Assinatura(certificado)
        text = 'test of signature'.encode('utf-8')
        text1 = 'test of signature1'.encode('utf-8')
        signature1 = assinador.assina_string(text1)
        with self.assertRaises(InvalidSignature):
            assinador.verificar_assinatura_string(text, signature1)


if __name__ == '__main__':
    unittest.main()
