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


from copy import copy
from pickle import dumps, loads
from unittest import TestCase

from prettyclass import prettyclass


class FirstUnitTests(TestCase):
    def setUp(self):
        flags = {'init' : True, 'repr' : True, 'copy' : True, 'eq' : True,
                 'nonzero' : True, 'hash' : True, 'json' : True}

        @prettyclass(**flags)
        class ABC:
            def __init__(self, a, *b, c, d=4, e, **f):
                ...


        @prettyclass(**flags)
        class CDE(ABC):
            def __init__(self, a, *b, c, d=4, e, g=0, **f):
                ...


        @prettyclass(**flags)
        class FGH(CDE):
            def __init__(self, a, *b, c, d=4, e, g=0, h=10, **f):
                ...

        self.flags = flags
        self.ABC = ABC
        self.CDE = CDE
        self.FGH = FGH
        self.cls_pre = 'FirstUnitTests.setUp.<locals>.'

        self.abc = ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')
        self.cde = CDE(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')
        self.fgh = FGH(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')

    def test_init(self):
        obj = self.abc
        self.assertEqual(1, obj.a)
        self.assertEqual((2, [3, 4]), obj.b)
        self.assertEqual(5, obj.c)
        self.assertEqual(1, obj.d)
        self.assertEqual(7, obj.e)
        self.assertEqual({'g': 'A', 'h': 'B'}, obj.f)

    def test_inheritance(self):
        obj = self.abc
        self.assertEqual(1, obj.a)
        self.assertEqual((2, [3, 4]), obj.b)
        self.assertEqual(5, obj.c)
        self.assertEqual(1, obj.d)
        self.assertEqual(7, obj.e)
        self.assertEqual({'g': 'A', 'h': 'B'}, obj.f)

        obj = self.cde
        self.assertEqual(1, obj.a)
        self.assertEqual((2, [3, 4]), obj.b)
        self.assertEqual(5, obj.c)
        self.assertEqual(1, obj.d)
        self.assertEqual(7, obj.e)
        self.assertEqual('A', obj.g)
        self.assertEqual({'h': 'B'}, obj.f)

        obj = self.fgh
        self.assertEqual(1, obj.a)
        self.assertEqual((2, [3, 4]), obj.b)
        self.assertEqual(5, obj.c)
        self.assertEqual(1, obj.d)
        self.assertEqual(7, obj.e)
        self.assertEqual('A', obj.g)
        self.assertEqual('B', obj.h)
        self.assertEqual({}, obj.f)

    def test_str(self):
        s = str(self.abc)
        c = self.cls_pre
        self.assertEqual(c + "ABC(1, 2, [3, 4], c=5, d=1, e=7, g=A, h=B)", s)

    def test_repr(self):
        s = repr(self.abc)
        c = self.cls_pre
        self.assertEqual(c + "ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')", s)

        # test omitting default values
        aab = self.ABC(1, 2, [3, 4], c=5, d=4, e=7, g='A', h='B')
        s = repr(aab)
        self.assertEqual(c + "ABC(1, 2, [3, 4], c=5, e=7, g='A', h='B')", s)

        # test repr of callable argument
        aaa = self.ABC(1, 2, [3, 4], c=dir, d=4, e=7, g='A', h='B')
        s = repr(aaa)
        self.assertEqual(c + "ABC(1, 2, [3, 4], c=dir, e=7, g='A', h='B')", s)

        s = repr(self.cde)
        c = self.cls_pre
        self.assertEqual(c + "CDE(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')", s)

        s = repr(self.fgh)
        c = self.cls_pre
        self.assertEqual(c + "FGH(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')", s)

    def test_copy(self):
        s = repr(copy(self.abc))
        c = self.cls_pre
        self.assertEqual(c + "ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')", s)
        self.assertEqual(repr(self.abc), s)

    def test_eq(self):
        self.assertEqual(self.abc, copy(self.abc))
        abb = self.ABC(1, 1, [3, 4], c=5, d=1, e=7, g='A', h='B')
        self.assertNotEqual(self.abc, abb)

    def test_bool(self):
        self.assertTrue(self.abc)
        abb = self.ABC(1, 0, [3, 4], c=5, d=1, e=7, g='A', h='B')
        self.assertFalse(abb)

    def test_hash(self):
        h = hash(self.abc)
        self.assertTrue(isinstance(h, int))
        self.assertEqual(hash(self.abc), h)
        abb = self.ABC(1, 1, [3, 4], c=5, d=1, e=7, g='A', h='B')
        self.assertNotEqual(hash(self.abc), hash(abb))

    def test_json(self):
        j = self.abc.__json__()
        self.assertEqual(self.abc, self.ABC.from_json(j))
        self.assertEqual(j, self.ABC.from_json(j).__json__())

    def test_pickle(self):
        from for_test_pickle import ABC
        abc = ABC(1, 2, [3, 4], c=5, d=1, e=7, g='A', h='B')
        p = dumps(abc)
        self.assertEqual(repr(abc), repr(loads(p)))
        self.assertEqual(p, dumps(loads(p)))
