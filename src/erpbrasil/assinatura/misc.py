"""
Miscellaneous tools for Assinatura.
"""
import datetime
from base64 import b64encode

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates
from cryptography.x509.oid import NameOID


def create_fake_certificate_file(valid, passwd, issuer, country, subject):
    """Creating a fake certificate

    This certificate is useful to be used in test cases,
    it is not valid to test the transmission of 'Notas Fiscais' in the homologation environment.

    :param valid: True or False
    :param passwd: Some password
    :param issuer: Some string, like EMISSOR A TESTE
    :param country: Some country: BR
    :param subject: Some string: CERTIFICADO VALIDO TESTE
    :return: base64 file
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()
    builder = x509.CertificateBuilder()

    builder = builder.subject_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, subject),
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            ]
        )
    )

    builder = builder.issuer_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, issuer),
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            ]
        )
    )

    one_year = datetime.timedelta(365, 0, 0)
    today = datetime.datetime.today()

    if valid:
        time_before = today
        time_after = today + one_year
    else:
        time_before = today - one_year
        time_after = today

    builder = builder.not_valid_before(time_before)
    builder = builder.not_valid_after(time_after)

    builder = builder.serial_number(2009)

    builder = builder.public_key(public_key)

    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA3_512(),
    )

    p12 = serialize_key_and_certificates(
        name=subject.encode(),
        key=private_key,
        cert=certificate,
        cas=None,
        encryption_algorithm=BestAvailableEncryption(passwd.encode()),
    )

    return b64encode(p12)
