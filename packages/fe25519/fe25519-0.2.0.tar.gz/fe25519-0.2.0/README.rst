=======
fe25519
=======

Native Python implementation of Ed25519 field elements and operations.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/fe25519.svg
   :target: https://badge.fury.io/py/fe25519
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/nthparty/fe25519.svg?branch=master
    :target: https://travis-ci.com/nthparty/fe25519

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/fe25519/badge.svg?branch=master
   :target: https://coveralls.io/github/nthparty/fe25519?branch=master

Purpose
-------
This library provides a native Python implementation of `Ed25519 <https://ed25519.cr.yp.to/>`_ field elements and a number of operations over them. The library makes it possible to fill gaps in prototype applications that may have specific limitations with respect to their operating environment or their ability to rely on dependencies.

The implementation is based upon and is compatible with the corresponding implementation of Ed25519 field elements used in `libsodium <https://github.com/jedisct1/libsodium>`_.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install fe25519

The library can be imported in the usual ways::

    import fe25519
    from fe25519 import fe25519

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Concise unit tests are implemented with the help of `fountains <https://pypi.org/project/fountains/>`_ and new reference bit lists for these tests can be generated in the following way::

    python test/test_fe25519.py

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint fe25519

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
Beginning with version 0.1.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
