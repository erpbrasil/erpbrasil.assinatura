# coding=utf-8

import os
from datetime import datetime
from tzlocal import get_localzone

from edoc_assinatura.cli import main
from edoc_assinatura.certificado import Certificado
from edoc_assinatura.assinatura import Assinatura

caminho = os.environ['caminho_certificado']
senha = os.environ['senha_certificado']


def test_main():
    assert main([]) == 0


def test_chave_cert():
    d = Certificado(caminho, senha)
    chave, certificado = d.separa_chave_certificado()
    assert chave, certificado


def test_assinatura_pdf():
    certificado = Certificado(caminho, senha)
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
        'files', 'result').replace('.pdf', '-signed-cms.pdf')
    with open(nome_arquivo, 'wb') as fp:
        fp.write(arquivo)
        fp.write(assinatura)

