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


def test_assinatura_xml_nfe400():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    assinador = Assinatura(certificado)

    nome_arquivo = 'tests/files/nfe-400.xml'
    arquivo = open(nome_arquivo, 'rb').read()

    assinatura = assinador.assina_xml(
        arquivo=arquivo,
    )
    nome_arquivo = nome_arquivo.replace(
        'files', 'result').replace('.xml', '-signed.xml')
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)


test_assinatura_xml_nfe400()
