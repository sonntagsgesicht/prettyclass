
.. image:: logo.png


Python Project *prettyclass*
----------------------------


.. image:: https://github.com/sonntagsgesicht/prettyclass/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/sonntagsgesicht/prettyclass/actions/workflows/python-package.yml
    :alt: GitHubWorkflow

.. image:: https://img.shields.io/readthedocs/prettyclass
   :target: http://prettyclass.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/github/license/sonntagsgesicht/prettyclass
   :target: https://github.com/sonntagsgesicht/prettyclass/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/prettyclass?label=github
   :target: https://github.com/sonntagsgesicht/prettyclass/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/prettyclass
   :target: https://pypi.org/project/prettyclass/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/prettyclass
   :target: https://pypi.org/project/prettyclass/
   :alt: PyPI - Python Version

.. image:: https://pepy.tech/badge/prettyclass
   :target: https://pypi.org/project/prettyclass/
   :alt: PyPI Downloads


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> import prettyclass

after installation.


.. code-block:: python

    >>> from prettyclass import prettyclass

    >>> @prettyclass()
    ... class ABC:
    ...     def __init__(self, a, *b, c, d=1, e, **f):
    ...         '''creates ABC instance'''

The decorator adds automaticly all argument fields as attributes.

.. code-block:: python

    >>> abc = ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')
    >>> abc.__dict__
    {'a': 1, 'b': (2, [3, 4]), 'c': 5, 'd': 6, 'e': 7, 'f': {'g': 'A', 'h': 'B'}}

    >>> abc.a, abc.b, abc.c, abc.d, abc.e, abc.f
    (1, (2, [3, 4]), 5, 6, 7, {'g': 'A', 'h': 'B'})

and returns a pretty nice representation of an instance

.. code-block:: python

    >>> abc
    ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')

Note the difference between 'str' and 'repr'

.. code-block:: python

    >>> str(abc)
    'ABC(1, 2, [3, 4], c=5, d=6, e=7, g=A, h=B)'

    >>> repr(abc)
    "ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')"

Copy works by default, too.

.. code-block:: python

    >>> from copy import copy
    >>> copy(abc)
    ABC(1, 2, [3, 4], c=5, d=6, e=7, g='A', h='B')


Note, the string representation commits entries
which coincide with defaults

.. code-block:: python

    >>> ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')
    ABC(1, 2, [3, 4], c=5, e=7, g='A', h='B')


Documentation
-------------

More documentation available at
`https://prettyclass.readthedocs.io <https://prettyclass.readthedocs.io>`_


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install prettyclass


License
-------

Code and documentation are available according to the license
(see LICENSE file in repository).
