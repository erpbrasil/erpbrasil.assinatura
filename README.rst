========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |tests| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/erpbrasilassinatura/badge/?version=latest
    :target: https://erpbrasilassinatura.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |tests| image:: https://github.com/erpbrasil/erpbrasil.assinatura/actions/workflows/tests.yml/badge.svg?branch=master
    :alt: Tests
    :target: https://github.com/erpbrasil/erpbrasil.assinatura/actions/workflows/tests.yml

.. |codecov| image:: https://codecov.io/gh/erpbrasil/erpbrasil.assinatura/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.assinatura

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.assinatura.svg
    :alt: PyPI Package latest release
    :target: https://erpbrasilassinatura.readthedocs.io/en/latest/

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.assinatura/v1.9.0...svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.assinatura/compare/v1.9.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.assinatura.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.assinatura

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.assinatura.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.assinatura

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.assinatura.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.assinatura


.. end-badges

Manipulação de certificados digitais, A1 e A3,  em Python, facilitando:

* Assinatura de documentos PDF
* Assinatura de documentos fiscais (XML)

Esta biblioteca faz parte do projeto: https://erpbrasil.github.io/

Instalação
==========

::

    pip install erpbrasil.assinatura          # certificado A1 (PKCS#12) e assinatura XML
    pip install erpbrasil.assinatura[pdf]     # mais assinatura de PDF (endesive)

Suporta Python 3.6 a 3.14, o que cobre do Odoo 12 ao Odoo 20. O CI testa cada
versão de Python e as três linhas do ``signxml`` (3, 4 e 5); o ``signxml`` fica
limitado a ``<4`` na instalação porque o Odoo 16 a 20 fixa ``cryptography`` em
versão que o ``signxml`` 5 não aceita.

Uso
===

::

    from erpbrasil.assinatura import Assinatura, Certificado

    certificado = Certificado("certificado.pfx", "senha")
    xml_assinado = Assinatura(certificado).assina_xml2(xml_etree, reference="NFe3519...")

Documentação
============

https://erpbrasil.github.io/

Créditos
========

Esta é uma biblioteca criada atravês do esforço de das empresas:

* Akretion https://akretion.com/pt-BR/
* KMEE https://www.kmee.com.br

Por favor consulte a lista de contribuidores: https://github.com/erpbrasil/erpbrasil.assinatura/graphs/contributors

Licença
~~~~~~~

* Free software: MIT license

Windows installation
====================

Prerequisites

* Install swig (and add swig install folder to PATH environment variable)


Ubuntu Installation
===================

::

    sudo apt-get update
    sudo apt-get install swig
    pip install erpbrasil.assinatura

Documentation
=============


https://erpbrasilassinatura.readthedocs.io/en/latest/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other

      - ::

            PYTEST_ADDOPTS=--cov-append tox
