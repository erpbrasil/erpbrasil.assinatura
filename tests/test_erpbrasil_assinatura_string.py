# coding=utf-8

import os

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/teste.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'teste')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')


def test_assinatura_string():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    assinador = Assinatura(certificado)
    texto = 'texte de assinatura'.encode('utf-8')
    assinador.assina_string(texto)


test_assinatura_string()
