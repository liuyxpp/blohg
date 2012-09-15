# -*- coding: utf-8 -*-
"""
    blohg.tests
    ~~~~~~~~~~~

    Main unit test package.

    :copyright: (c) 2010-2012 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import unittest
from blohg.tests.hgapi import HgApiTestCase
from blohg.tests.hgapi.repo import RepositoryTestCase, \
     RepoStateStableTestCase, RepoStateVariableTestCase
from blohg.tests.hgapi.templates import MercurialLoaderTestCase


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HgApiTestCase))
    suite.addTest(unittest.makeSuite(MercurialLoaderTestCase))
    suite.addTest(unittest.makeSuite(RepoStateStableTestCase))
    suite.addTest(unittest.makeSuite(RepoStateVariableTestCase))
    suite.addTest(unittest.makeSuite(RepositoryTestCase))
    return suite
