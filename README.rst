========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/erpbrasilassinatura/badge/?version=latest
    :target: https://erpbrasilassinatura.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/erpbrasil/erpbrasil.assinatura.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/erpbrasil/erpbrasil.assinatura

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/erpbrasil/erpbrasil.assinatura?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/erpbrasil/erpbrasil.assinatura

.. image:: https://requires.io/github/erpbrasil/erpbrasil.assinatura/requirements.svg?branch=master
     :target: https://requires.io/github/erpbrasil/erpbrasil.assinatura/requirements/?branch=master
     :alt: Requirements Status

.. |codecov| image:: https://codecov.io/gh/erpbrasil/erpbrasil.assinatura/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.assinatura

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.assinatura.svg
    :alt: PyPI Package latest release
    :target: https://erpbrasilassinatura.readthedocs.io/en/latest/

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.assinatura/v0.2.1...svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.assinatura/compare/v0.2.1....master

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

Assinatura de documentos com certificados digitais A1 e A3

* Free software: MIT license

Installation
============

::

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
