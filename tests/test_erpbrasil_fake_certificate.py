import datetime
from unittest import TestCase

from erpbrasil.assinatura import certificado
from erpbrasil.assinatura.excecoes import CertificadoExpirado
from erpbrasil.assinatura.misc import create_fake_certificate_file


class Tests(TestCase):
    """Simple test for fake certificate creation."""

    def setUp(self):
        self.cert_country = "BR"
        self.cert_issuer_a = "EMISSOR A TESTE"
        self.cert_issuer_b = "EMISSOR B TESTE"
        self.cert_subject_valid = "CERTIFICADO VALIDO TESTE"
        self.cert_date_exp = datetime.datetime.today() + datetime.timedelta(days=365)
        self.cert_subject_invalid = "CERTIFICADO INVALIDO TESTE"
        self.cert_passwd = "123456"
        self.cert_name = "{} - {} - {} - Valid: {}".format(
            "NF-E",
            "A1",
            self.cert_subject_valid,
            self.cert_date_exp.strftime("%Y%M%d"),
        )

        self.certificate_valid = create_fake_certificate_file(
            valid=True,
            passwd=self.cert_passwd,
            issuer=self.cert_issuer_a,
            country=self.cert_country,
            subject=self.cert_subject_valid,
        )

        self.certificate_invalid = create_fake_certificate_file(
            valid=False,
            passwd=self.cert_passwd,
            issuer=self.cert_issuer_b,
            country=self.cert_country,
            subject=self.cert_subject_invalid,
        )

    def test_valid_certificate(self):
        """Check a valid certificate"""
        cert = certificado.Certificado(self.certificate_valid, self.cert_passwd)
        self.assertEqual(cert.emissor, self.cert_issuer_a)
        self.assertEqual(cert.proprietario, self.cert_subject_valid)
        self.assertEqual(
            cert.fim_validade.strftime("%Y%M%d"),
            self.cert_date_exp.strftime("%Y%M%d")
        )

    def test_invalid_certificate(self):
        """Check a invalid certificate"""
        with self.assertRaises(CertificadoExpirado):
            certificado.Certificado(self.certificate_invalid, self.cert_passwd)
