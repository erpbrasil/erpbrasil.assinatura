# coding=utf-8

import os
from edoc_assinatura.certificado import Certificado
from edoc_assinatura.assinatura import Assinatura


certificado_nfe_caminho = os.environ['certificado_nfe_caminho']
certificado_nfe_senha = os.environ['certificado_nfe_senha']

certificado_ecpf_caminho = os.environ['certificado_ecpf_caminho']
certificado_ecpf_senha = os.environ['certificado_ecpf_senha']


def test_assinatura_xml_nfe400():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    assinador = Assinatura(certificado)

    nome_arquivo = './files/nfe-400.xml'
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
