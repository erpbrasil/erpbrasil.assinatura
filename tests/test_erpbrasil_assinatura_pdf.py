# coding=utf-8

import os
import tempfile
from datetime import datetime

from tzlocal import get_localzone

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/teste.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha',
                                       'teste')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')

test_path = os.environ.get('test_path', 'tests/')


def test_assinatura_nfe_pdf():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
    assinador = Assinatura(certificado)

    nome_arquivo_pdf = test_path + 'files/google.pdf'
    arquivo = open(nome_arquivo_pdf, 'rb').read()

    dados_assinatura = {
        'sigflags': 3,
        'contact': 'KMEE INFORMATICA LTDA',
        'location': 'BR',
        'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        'reason': 'Teste assinatura',
    }

    assinatura = assinador.assina_pdf(
        arquivo=arquivo,
        dados_assinatura=dados_assinatura,
    )
    file_temp = tempfile.gettempdir() + '/google-signed-nfe.pdf'
    with open(file_temp, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)


def test_assinatura_multipla_pdf():
    ecpf = Certificado(certificado_ecpf_caminho, certificado_ecpf_senha, raise_expirado=False)
    assinador_ecpf = Assinatura(ecpf)

    nome_arquivo = test_path + 'files/google.pdf'
    arquivo = open(nome_arquivo, 'rb').read()

    dados_assinatura = {
        'sigflags': 3,
        'contact': 'Luis Felipe Mileo',
        'location': 'BR',
        'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        'reason': 'Teste Assinatura CPF',
    }

    assinatura1 = assinador_ecpf.assina_pdf(
        arquivo=arquivo,
        dados_assinatura=dados_assinatura,
    )
    file_temp = tempfile.gettempdir() + '/google-signed-multiple-1.pdf'
    with open(file_temp, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura1)

    arquivo2 = open(nome_arquivo, 'rb').read()

    nfe = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
    assinador_nfe = Assinatura(nfe)

    dados_assinatura = {
        'sigflags': 3,
        'contact': 'KMEE INFORMATICA LTDA',
        'location': 'BR',
        'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        'reason': 'Teste Assinatura CNPJ',
    }

    assinatura2 = assinador_nfe.assina_pdf(
        arquivo=arquivo2,
        dados_assinatura=dados_assinatura,
    )
    file_temp = tempfile.gettempdir() + '/google-signed-multiple-1.pdf'
    with open(file_temp, 'wb') as fp:
        fp.write(arquivo2)
        fp.write(assinatura2)
