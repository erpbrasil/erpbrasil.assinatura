# coding=utf-8


class CertificadoExpirado(Exception):
    """Lançado quando é tentado abrir um certificado já expirado."""


class ErroDeLeituraDeArquivo(Exception):
    """Lançado quando não é possível abrir um aquivo."""


class CertificadoSenhaInvalida(Exception):
    """Lançado quando não é possível abrir um aquivo."""
