# Copyright (C) 2009-2020 Martin Slouf <martinslouf@users.sourceforge.net>
#
# This file is a part of Summer.
#
# Summer is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Relatively advanced standalone example.

Check the sample config files in this directory.  Look at the single
:py:module:`tmplproject` module.
"""

import logging.config
import os.path
import sys
import unittest

# configure logging as soon as possible
LOGGING_CFG = os.path.join(os.path.dirname(__file__), "logging.cfg")
logging.config.fileConfig(LOGGING_CFG)
logger = logging.getLogger(__name__)
logger.info("logging config = %s", LOGGING_CFG)

from summer.test.examples.tmplproject.tmplproject import main


class TmplProjectTest(unittest.TestCase):
    """Demonstrates various summer features in *real-world* project."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tmplproject(self):
        logger.info("#### TEST STARTS HERE ####")
        self.assertEqual(0, main.main(sys.argv[1:]))
        logger.info("#### TEST ENDS HERE ####")


if __name__ == "__main__":
    unittest.main()
