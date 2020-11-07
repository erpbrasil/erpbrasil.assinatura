# coding=utf-8

import os
import tempfile

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/fixtures/dummy_cert.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'dummy_password')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')


def test_assinatura_xml_nfe400():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
    assinador = Assinatura(certificado)

    nome_arquivo = os.environ.get('file_nfe_400', 'tests/files/nfe-400.xml')
    arquivo = open(nome_arquivo, 'rb').read()

    assinatura = assinador.assina_xml(arquivo)
    file_temp = tempfile.gettempdir() + '/nfe-400-signed.xml'

    with open(file_temp, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)


test_assinatura_xml_nfe400()
