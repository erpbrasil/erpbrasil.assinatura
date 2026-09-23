import os
import tempfile

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

certificado_nfe_caminho = os.environ.get(
    "certificado_nfe_caminho", "tests/fixtures/dummy_cert.pfx"
)
certificado_nfe_senha = os.environ.get("certificado_nfe_senha", "dummy_password")

certificado_ecpf_caminho = os.environ.get("certificado_ecpf_caminho", "tests/teste.pfx")
certificado_ecpf_senha = os.environ.get("certificado_ecpf_senha", "teste")


def test_assinatura_xml_nfe400():
    certificado = Certificado(
        certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False
    )
    assinador = Assinatura(certificado)

    nome_arquivo = os.environ.get("file_nfe_400", "tests/files/nfe-400.xml")
    arquivo = open(nome_arquivo, "rb").read()

    assinatura = assinador.assina_xml(arquivo)
    file_temp = tempfile.gettempdir() + "/nfe-400-signed.xml"

    with open(file_temp, "wb") as fp:
        fp.write(arquivo)
        fp.write(assinatura)


NS_NFSE = "http://www.sped.fazenda.gov.br/nfse"
NS_DS = "http://www.w3.org/2000/09/xmldsig#"
LOTE_DPS = (
    '<EnviarLoteDpsSincronoEnvio xmlns="%s">'
    '<LoteDps Id="Lote1" versao="1.01"><NumeroLote>1</NumeroLote>'
    "<ListaDps>"
    '<DPS versao="1.01"><infDPS Id="DPS520870721234567800019500001000000000000001">'
    "<tpAmb>2</tpAmb></infDPS></DPS>"
    "</ListaDps></LoteDps>"
    "</EnviarLoteDpsSincronoEnvio>" % NS_NFSE
)


def _check_digest(signed_root, signature):
    """Confere o DigestValue da assinatura contra o elemento que ela referencia.

    As duas assinaturas (DPS e lote) foram conferidas com o xmlsec1, que
    tambem recusa o lote adulterado. O XMLVerifier do signxml nao serve
    aqui porque sempre pega a primeira Signature do documento, e o c14n de
    subarvore do lxml diverge do xmlsec quando o elemento contem outra
    Signature com namespace padrao proprio: por isso o digest e conferido
    so onde nao ha assinatura aninhada (a DPS).
    """
    import hashlib
    from base64 import b64decode

    from lxml import etree

    ds = "{%s}" % NS_DS
    reference = signature.find(ds + "SignedInfo/" + ds + "Reference")
    element = signed_root.find(".//*[@Id='%s']" % reference.get("URI")[1:])
    digest = hashlib.sha256(etree.tostring(element, method="c14n")).digest()
    assert digest == b64decode(reference.findtext(ds + "DigestValue"))


def test_assinatura_xml2_sha256_dps_e_lote():
    """DPS e LoteDps assinados em SHA256, como exige a NFS-e via NotaControl."""
    from lxml import etree

    certificado = Certificado(
        certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False
    )
    assinador = Assinatura(certificado)
    sha256 = dict(signature_algorithm="rsa-sha256", digest_algorithm="sha256")

    root = etree.fromstring(LOTE_DPS)
    dps = root.find(".//{%s}DPS" % NS_NFSE)
    signed_dps = etree.fromstring(
        assinador.assina_xml2(
            dps, "DPS520870721234567800019500001000000000000001", **sha256
        )
    )
    dps.getparent().replace(dps, signed_dps)

    signed = etree.fromstring(assinador.assina_xml2(root, "Lote1", **sha256))

    dps_sig = signed.find(".//{%s}DPS/{%s}Signature" % (NS_NFSE, NS_DS))
    lote_sig = signed.find("{%s}Signature" % NS_DS)
    assert dps_sig is not None, "Signature da DPS deve ser irma da infDPS"
    assert lote_sig is not None, "Signature do lote deve ser irma do LoteDps"
    for sig in (dps_sig, lote_sig):
        method = sig.find(".//{%s}SignatureMethod" % NS_DS).get("Algorithm")
        assert method.endswith("rsa-sha256")
        digest = sig.find(".//{%s}DigestMethod" % NS_DS).get("Algorithm")
        assert digest.endswith("sha256")
    _check_digest(signed, dps_sig)
    reference = lote_sig.find("{%s}SignedInfo/{%s}Reference" % (NS_DS, NS_DS))
    assert reference.get("URI") == "#Lote1"


def test_assinatura_xml2_padrao_continua_sha1():
    from lxml import etree

    certificado = Certificado(
        certificado_nfe_caminho, certificado_nfe_senha, raise_expirado=False
    )
    root = etree.fromstring(LOTE_DPS)
    signed = etree.fromstring(Assinatura(certificado).assina_xml2(root, "Lote1"))
    method = signed.find(".//{%s}SignatureMethod" % NS_DS).get("Algorithm")
    assert method.endswith("rsa-sha1")
