# coding=utf-8

import os
from datetime import datetime

from tzlocal import get_localzone

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado
from erpbrasil.assinatura.cli import main

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/teste.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'teste')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')


def test_main():
    assert main([]) == 0


def test_chave_cert():
    d = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    chave, certificado = d.separa_chave_certificado()
    assert chave, certificado
