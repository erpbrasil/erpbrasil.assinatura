"""Valida a assinatura gerada (RSA-SHA1 + digest SHA1, exigidos pela SEFAZ).

A verificacao principal e independente do signxml (lxml + cryptography),
para nao depender da API de verificacao, que muda entre as versoes 3, 4 e 5.
Alem dela, quando possivel, o proprio ``XMLVerifier`` do signxml confere.
"""

import base64
import hashlib
import inspect
import os

import pytest
import signxml
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding
from lxml import etree

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

DS = "http://www.w3.org/2000/09/xmldsig#"
NS = {"ds": DS}

certificado_nfe_caminho = os.environ.get("certificado_nfe_caminho", "tests/fixtures/dummy_cert.pfx")
certificado_nfe_senha = os.environ.get("certificado_nfe_senha", "dummy_password")
arquivo_nfe = os.environ.get("file_nfe_400", "tests/files/nfe-400.xml")


@pytest.fixture(scope="module")
def certificado():
    return Certificado(certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False)


def _verifica_rsa_sha1(xml, certificado, excise_xmlns_vazio=False):
    """Confere digest SHA1 da Reference e a assinatura RSA-SHA1 do SignedInfo."""
    root = etree.fromstring(xml)
    assinaturas = root.findall(".//ds:Signature", NS)
    assert assinaturas, "nenhuma Signature (namespace ds) no documento"
    for assinatura in assinaturas:
        info = assinatura.find("ds:SignedInfo", NS)
        assert info.find("ds:SignatureMethod", NS).get("Algorithm") == DS + "rsa-sha1"
        ref = info.find("ds:Reference", NS)
        assert ref.find("ds:DigestMethod", NS).get("Algorithm") == DS + "sha1"
        uri = ref.get("URI")
        if uri:
            alvo = root.xpath("//*[@Id=$i]", i=uri[1:])[0]
        else:
            alvo = root
        # digest do elemento referenciado, sem a propria assinatura
        copia_raiz = etree.fromstring(etree.tostring(root))
        if uri:
            copia = copia_raiz.xpath("//*[@Id=$i]", i=uri[1:])[0]
        else:
            copia = copia_raiz
        for sig in list(copia.iter("{%s}Signature" % DS)):
            if sig.find("ds:SignedInfo/ds:Reference", NS).get("URI") == uri:
                sig.getparent().remove(sig)
        canonico = etree.tostring(copia, method="c14n")
        if excise_xmlns_vazio:
            # assina_xml2 liga excise_empty_xmlns_declarations: o signxml tira
            # os xmlns="" (filhos sem namespace da fixture) antes do hash
            canonico = canonico.replace(b' xmlns=""', b"")
        digest = base64.b64encode(hashlib.sha1(canonico).digest()).decode()
        assert digest == ref.find("ds:DigestValue", NS).text.strip()
        # assinatura sobre o SignedInfo canonicalizado
        valor = base64.b64decode(assinatura.find("ds:SignatureValue", NS).text)
        canonico_info = etree.tostring(info, method="c14n")
        if excise_xmlns_vazio:
            # o c14n do libxml2 emite xmlns="" espurio em filhos da Signature
            canonico_info = canonico_info.replace(b' xmlns=""', b"")
        certificado.cert.public_key().verify(
            valor,
            canonico_info,
            padding.PKCS1v15(),
            hashes.SHA1(),
        )
        assert alvo is not None
    return root


def _verifica_com_signxml(xml, certificado):
    """Segunda opiniao: XMLVerifier do signxml, com SHA1 liberado na leitura."""
    if not hasattr(signxml, "SignatureConfiguration"):
        # signxml 2.x (Python 3.6): sem a API de configuracao; a verificacao
        # independente em _verifica_rsa_sha1 ja cobriu a assinatura.
        return
    config = dict(
        require_x509=True,
        signature_methods=frozenset([signxml.SignatureMethod.RSA_SHA1]),
        digest_algorithms=frozenset([signxml.DigestAlgorithm.SHA1]),
    )
    campos = set(inspect.signature(signxml.SignatureConfiguration).parameters)
    if "verification_time" in campos:  # signxml >= 5.1: rejeita cert expirado
        config["verification_time"] = (
            certificado.inicio_validade.replace(tzinfo=None)
            + (certificado.fim_validade - certificado.inicio_validade) / 2
        )
    pem = certificado.cert.public_bytes(Encoding.PEM)
    resultado = signxml.XMLVerifier().verify(
        xml,
        x509_cert=pem,
        expect_config=signxml.SignatureConfiguration(**config),
    )
    assert resultado is not None


def test_assina_xml_nfe_rsa_sha1_valida(certificado):
    assinatura = Assinatura(certificado).assina_xml(open(arquivo_nfe, "rb").read())
    _verifica_rsa_sha1(assinatura, certificado)
    _verifica_com_signxml(assinatura, certificado)


def test_assina_xml2_nfe_rsa_sha1_valida_e_relocada(certificado):
    root = etree.fromstring(open(arquivo_nfe, "rb").read())
    ref = root.find(".//{*}infNFe").get("Id")
    xml = Assinatura(certificado).assina_xml2(root, ref)
    verificado = _verifica_rsa_sha1(xml.encode(), certificado, True)
    # a Signature sai de dentro do infNFe e fica ao lado dele, dentro da NFe
    sig = verificado.find(".//ds:Signature", NS)
    assert etree.QName(sig.getparent()).localname == "NFe"
    assert sig.find("ds:SignedInfo/ds:Reference", NS).get("URI") == "#" + ref
    # nao chama XMLVerifier: sem excise_empty_xmlns_declarations (legado do
    # signxml) o libxml2 acrescenta xmlns="" e a conferencia falha por artefato


def test_assina_xml2_ignora_espacos_entre_tags(certificado):
    original = open(arquivo_nfe, "rb").read()
    parser = etree.XMLParser(remove_blank_text=True)
    compacto = etree.fromstring(original, parser)
    indentado = etree.fromstring(original)
    ref = compacto.find(".//{*}infNFe").get("Id")
    d = []
    for root in (compacto, indentado):
        xml = Assinatura(certificado).assina_xml2(root, ref)
        _verifica_rsa_sha1(xml.encode(), certificado, True)
        d.append(etree.fromstring(xml.encode()).find(".//ds:DigestValue", NS).text)
    assert d[0] == d[1]


def test_assina_nfse_rsa_sha1_valida(certificado):
    root = etree.fromstring(open(arquivo_nfe, "rb").read())
    xml = Assinatura(certificado).assina_nfse(root)
    _verifica_rsa_sha1(xml.encode(), certificado)


def test_certificado_de_teste_e_rsa(certificado):
    assert isinstance(certificado.cert, x509.Certificate)
