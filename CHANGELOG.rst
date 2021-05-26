
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
