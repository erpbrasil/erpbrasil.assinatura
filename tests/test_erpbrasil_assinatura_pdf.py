# coding=utf-8

import os
from datetime import datetime

from tzlocal import get_localzone

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get('certificado_nfe_caminho',
                                         'tests/teste.pfx')
certificado_nfe_senha = os.environ.get('certificado_nfe_senha', 'teste')

certificado_ecpf_caminho = os.environ.get('certificado_ecpf_caminho',
                                          'tests/teste.pfx')
certificado_ecpf_senha = os.environ.get('certificado_ecpf_senha', 'teste')


def test_assinatura_nfe_pdf():
    certificado = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
    assinador = Assinatura(certificado)

    nome_arquivo = 'tests/files/google.pdf'
    arquivo = open(nome_arquivo, 'rb').read()

    dados_assinatura = {
        b'sigflags': 3,
        b'contact': b'KMEE INFORMATICA LTDA',
        b'location': b'BR',
        b'signingdate': str.encode(
            datetime.now(get_localzone()).strftime("%Y%M%d%H%M%S%Z")),
        b'reason': b'Teste assinatura',
    }

    assinatura = assinador.assina_pdf(
        arquivo=arquivo,
        dados_assinatura=dados_assinatura,
    )

    with open('/tmp/google-signed-nfe.pdf', 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)


def test_assinatura_multipla_pdf():
    ecpf = Certificado(certificado_ecpf_caminho, certificado_ecpf_senha, raise_expirado=False)
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

    nome_arquivo = '/tmp/google-signed-multiple-1.pdf'
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura1)

    arquivo2 = open(nome_arquivo, 'rb').read()

    nfe = Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)
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
    with open('/tmp/google-signed-multiple-1.pdf', 'wb') as fp:
        fp.write(arquivo2)
        fp.write(assinatura2)
