
Changelog
=========

0.0.0 (2019-04-18)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.

0.3.0 (2019-11-19)
~~~~~~~~~~~~~~~~~~

* Correção da importação da biblioteca e seu namespace

0.4.0 (2019-11-20)
~~~~~~~~~~~~~~~~~~

* Acesso aos dados do certificado: Proprietário e CNPJ/CPF caso exista

0.4.1 (2019-11-25)
~~~~~~~~~~~~~~~~~~

* Compatibilidade com python 2
* Correção na assinatura

0.4.2 (2019-11-26)
~~~~~~~~~~~~~~~~~~

* Concatenar somente o elemento assinado no momento, sem mover os outros elementos de bloco. Por exemplo um lote de rps já assinados deve compor um bloco assinado, ao assinar este bloco as outras assinaturas não devem ser modificadas.

1.0.0 (2020-11-10)
~~~~~~~~~~~~~~~~~~

* Fim do suporte ao python2
* Estabilização dos testes

1.2.0 (2021-05-26)
~~~~~~~~~~~~~~~~~~

* Assinatura da nota paulista (Infelizmente com o XMLSEC, tiramos ele em uma nova versão)

1.8.0 (2025-08-12)
~~~~~~~~~~~~~~~~~~

* Leitura do PKCS#12 pela ``cryptography`` (sem ``OpenSSL.crypto.load_pkcs12``).
* Correções na data de validade e no CNPJ/CPF do certificado.

1.8.1 (2026-09-30)
~~~~~~~~~~~~~~~~~~

* Teto ``signxml<4`` e ``pyOpenSSL<24.3``: o signxml 4.2.2 muda o namespace da
  Signature e a assinatura saía fora da NFe sem erro; o pyOpenSSL 24.3 removeu
  ``OpenSSL.crypto.verify``.
* Testes que verificam a assinatura gerada (digest e RSA) em vez de só gravar o arquivo.

1.9.0 (não publicada)
~~~~~~~~~~~~~~~~~~~~~

* Suporte ao signxml 3, 4 e 5: a Signature é localizada depois de serializar a
  árvore, e o certificado é passado em PEM (antes o primeiro ``sign`` sempre
  levantava ``TypeError`` e só o fallback funcionava).
* ``assina_xml2`` aceita ``signature_algorithm`` e ``digest_algorithm``
  (RSA-SHA256 para provedores que exigem).
* Empacotamento: ``pyproject.toml`` com hatchling, namespace ``erpbrasil`` por
  ``pkgutil.extend_path`` (igual à ``erpbrasil.base``), extras ``pdf``, ``test`` e
  ``doc``, Python 3.6 a 3.14 declarado e testado no CI, publicação no PyPI por
  Release do GitHub com conferência da tag. Saem ``setup.py``, Travis e AppVeyor.
