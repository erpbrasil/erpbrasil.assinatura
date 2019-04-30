# coding=utf-8

import os
from datetime import datetime
from tzlocal import get_localzone

from edoc_assinatura.certificado import Certificado
from edoc_assinatura.assinatura import Assinatura

certificado_nfe_caminho = os.environ['certificado_nfe_caminho']
certificado_nfe_senha = os.environ['certificado_nfe_senha']

certificado_ecpf_caminho = os.environ['certificado_ecpf_caminho']
certificado_ecpf_senha = os.environ['certificado_ecpf_senha']


def test_assinatura_nfe_pdf():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    assinador = Assinatura(certificado)

    nome_arquivo = 'tests/files/google.pdf'
    arquivo = open(nome_arquivo, 'rb').read()

    dados_assinatura = {
        b'sigflags': 3,
        b'contact': b'KMEE INFORMATICA LTDA',
        b'location': b'BR',
        b'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        b'reason': b'Teste edoc assinatura',
    }

    assinatura = assinador.assina_pdf(
        arquivo=arquivo,
        dados_assinatura=dados_assinatura,
    )
    nome_arquivo = nome_arquivo.replace(
        'files', 'result').replace('.pdf', '-signed-nfe.pdf')
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)


def test_assinatura_multipla_pdf():
    ecpf = Certificado(certificado_ecpf_caminho, certificado_ecpf_senha)
    assinador_ecpf = Assinatura(ecpf)

    nome_arquivo = 'tests/files/google.pdf'
    arquivo = open(nome_arquivo, 'rb').read()

    dados_assinatura = {
        b'sigflags': 3,
        b'contact': b'Luis Felipe Mileo',
        b'location': b'BR',
        b'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        b'reason': b'Teste Assinatura CPF',
    }

    assinatura1 = assinador_ecpf.assina_pdf(
        arquivo=arquivo,
        dados_assinatura=dados_assinatura,
    )

    nome_arquivo = nome_arquivo.replace(
        'files', 'result').replace('.pdf', '-signed-multiple-1.pdf')
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura1)

    arquivo2 = open(nome_arquivo, 'rb').read()

    nfe = Certificado(certificado_nfe_caminho, certificado_nfe_senha)
    assinador_nfe = Assinatura(nfe)

    dados_assinatura = {
        b'sigflags': 3,
        b'contact': b'KMEE INFORMATICA LTDA',
        b'location': b'BR',
        b'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        b'reason': b'Teste Assinatura CNPJ',
    }

    assinatura2 = assinador_nfe.assina_pdf(
        arquivo=arquivo2,
        dados_assinatura=dados_assinatura,
    )

    nome_arquivo = nome_arquivo.replace(
        'signed-multiple-1.pdf',
        'signed-multiple-2.pdf'
    )
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo2)
        fp.write(assinatura2)
