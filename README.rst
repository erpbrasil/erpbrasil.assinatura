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

.. |travis| image:: https://travis-ci.org/python-edoc/edoc-assinatura.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/python-edoc/edoc-assinatura

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/python-edoc/edoc-assinatura?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/python-edoc/edoc-assinatura

.. |requires| image:: https://requires.io/github/python-edoc/edoc-assinatura/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/python-edoc/edoc-assinatura/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/python-edoc/edoc-assinatura/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/python-edoc/edoc-assinatura

.. |version| image:: https://img.shields.io/pypi/v/edoc-assinatura.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/edoc-assinatura

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-edoc/edoc-assinatura/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/python-edoc/edoc-assinatura/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/edoc-assinatura.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/edoc-assinatura

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/edoc-assinatura.svg
    :alt: Supported versions
    :target: https://pypi.org/project/edoc-assinatura

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/edoc-assinatura.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/edoc-assinatura


.. end-badges

Assinatura de documentos com certificados digitais A1 e A3

* Free software: MIT license

Installation
============

::

    pip install edoc-assinatura

Documentation
=============


https://edoc-assinatura.readthedocs.io/


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
