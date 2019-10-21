# coding=utf-8

import os

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado
from cryptography.exceptions import InvalidSignature

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/teste.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'teste')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')


def test_assinatura_string():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
    assinador = Assinatura(certificado)
    text = 'test of signature'.encode('utf-8')
    text1 = 'test of signature1'.encode('utf-8')
    signature1 = assinador.assina_string(text1)
    try:
        assinador.verificar_assinatura_string(text, signature1)
        raise
    except InvalidSignature:
        print("test passed")


test_assinatura_string()
