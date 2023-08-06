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

import unittest
import summer


class DomainTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_entity(self):
        ent = summer.Entity()
        self.assertTrue(ent == ent)
        self.assertEqual(ent, ent)
        ent.id = 4
        ent2 = summer.Entity()
        ent2.id = 4
        self.assertTrue(ent == ent2)
        self.assertEqual(ent, ent2)

    def test_ldap_entity(self):
        ent = summer.LdapEntity()
        self.assertTrue(ent == ent)
        self.assertEqual(ent, ent)
        ent.dn = "dc=summer,dn=lion"
        ent2 = summer.LdapEntity()
        ent2.dn = "dc=summer,dn=lion"
        self.assertTrue(ent == ent2)
        self.assertEqual(ent, ent2)

    def test_filter(self):
        flt = summer.Filter.get_default()
        self.assertEqual(1, flt.page)
        self.assertEqual(-1, flt.max_results)
        self.assertEqual(0, flt.get_offset())

        flt = summer.Filter(1, 20)
        self.assertEqual(1, flt.page)
        self.assertEqual(20, flt.max_results)

        self.assertEqual(0, flt.get_offset())
        flt.page += 1
        self.assertEqual(20, flt.get_offset())
        flt.page += 1
        self.assertEqual(40, flt.get_offset())
        flt.page += 1
        self.assertEqual(60, flt.get_offset())
        flt.page += 1
        self.assertEqual(80, flt.get_offset())
        flt.page += 3  # +7 in total
        self.assertEqual(140, flt.get_offset())
        flt.page -= 3
        self.assertEqual(80, flt.get_offset())


if __name__ == "__main__":
    unittest.main()
