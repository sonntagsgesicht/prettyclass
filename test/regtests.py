# -*- coding: utf-8 -*-

# auxilium
# --------
# A Python project for an automated test and deploy toolkit - 100%
# reusable.
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Sunday, 11 October 2020
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


import pydoc

from regtest import RegressionTestCase

from prettyclass import prettyclass


# first run will build reference values (stored in files)
# second run will test against those reference values
# to update reference values simply remove the according files

class FirstRegTests(RegressionTestCase):

    compression = False

    def setUp(self):
        flags = {'init' : True, 'repr' : True, 'copy' : True, 'eq' : True,
                 'nonzero' : True, 'hash' : True, 'json' : True}

        @prettyclass(**flags)
        class ABC:
            def __init__(self, a, *b, c, d=4, e, **f):
                ...

        self.ABC = ABC

    def test_instance_help(self):
        h = pydoc.render_doc(self.ABC, "Help on %s")
        self.assertRegressiveEqual(h)

    def test_decorator_help(self):
        h = pydoc.render_doc(prettyclass, "Help on %s")
        self.assertRegressiveEqual(h)
