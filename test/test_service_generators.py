#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2015: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2009-2014:
#     Jean Gabes, naparuba@gmail.com
#     Hartmut Goebel, h.goebel@goebel-consult.de
#     Grégory Starck, g.starck@gmail.com
#     Gerhard Lausser, gerhard.lausser@consol.de
#     Sebastien Coavoux, s.coavoux@free.fr

#  This file is part of Shinken.
#
#  Shinken is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shinken is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

#
# This file is used to test reading and processing of config files
#

from alignak_test import *


class TestConfig(AlignakTest):
    def setUp(self):
        self.setup_with_file(['etc/alignak_service_generators.cfg'])

    def test_service_generators(self):

        host = self.sched.hosts.find_by_name("test_host_0_gen")
        host.checks_in_progress = []
        host.act_depend_of = []  # ignore the router
        router = self.sched.hosts.find_by_name("test_router_0")
        router.checks_in_progress = []
        router.act_depend_of = []  # ignore the router
        svc = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "test_ok_0")

        print "All service of", "test_host_0_gen"
        for s in host.services:
            print self.sched.services[s].get_name()
        # We ask for 4 services with our disks :)
        svc_c = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service C")
        svc_d = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service D")
        svc_e = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service E")
        svc_f = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service F")
        svc_g = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service G")

        self.assertIsNot(svc_c, None)
        self.assertIsNot(svc_d, None)
        self.assertIsNot(svc_e, None)
        self.assertIsNot(svc_f, None)
        self.assertIsNot(svc_g, None)

        # two classics
        self.assertEqual(['C', '80%', '90%'], svc_c.check_command.args)
        self.assertEqual(['D', '95%', '70%'], svc_d.check_command.args)
        # a default parameters
        self.assertEqual(['E', '38%', '24%'], svc_e.check_command.args)
        # and another one
        self.assertEqual(['F', '95%', '70%'], svc_f.check_command.args)
        # and the tricky last one (with no value :) )
        self.assertEqual(['G', '38%', '24%'], svc_g.check_command.args)


        # Now check that the dependencies are also created as Generated Service C Dependant -> Generated Service C
        svc_c_dep = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service C Dependant")
        self.assertIsNot(svc_c_dep, None)
        # Dep version should a child of svc
        self.assertIn(svc_c_dep.uuid, svc_c.child_dependencies)
        # But not on other of course
        self.assertNotIn(svc_c_dep.uuid, svc_d.child_dependencies)

        

    def test_service_generators_not(self):
        host = self.sched.hosts.find_by_name("test_host_0_gen")
        host.checks_in_progress = []
        host.act_depend_of = []  # ignore the router
        router = self.sched.hosts.find_by_name("test_router_0")
        router.checks_in_progress = []
        router.act_depend_of = []  # ignore the router
        svc = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "test_ok_0")

        print "All service of", "test_host_0_gen"
        for s in host.services:
            print self.sched.services[s].get_name()
        # We ask for 4 services with our disks :)
        svc_c = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service NOT C")
        svc_d = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service NOT D")
        svc_e = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service NOT E")
        svc_f = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service NOT F")
        svc_g = self.sched.services.find_srv_by_name_and_hostname("test_host_0_gen", "Generated Service NOT G")

        self.assertIsNot(svc_c, None)
        self.assertIsNot(svc_d, None)
        self.assertIs(None, svc_e)
        self.assertIs(None, svc_f)
        self.assertIsNot(svc_g, None)

    def test_service_generators_key_generator(self):

        host = self.sched.hosts.find_by_name("sw_0")
        host.checks_in_progress = []
        host.act_depend_of = []  # ignore the router

        print "All service of", "sw_0"
        for s in host.services:
            print self.sched.services[s].get_name()

        # We ask for our 6*46 + 6 services with our ports :)
        # _ports  Unit [1-6] Port [0-46]$(80%!90%)$,Unit [1-6] Port 47$(80%!90%)$
        for unit_id in xrange(1, 7):
            for port_id in xrange(0, 47):
                n = "Unit %d Port %d" % (unit_id, port_id)
                print "Look for port", 'Generated Service ' + n
                svc = self.sched.services.find_srv_by_name_and_hostname("sw_0", 'Generated Service ' + n)
                self.assertIsNot(svc, None)
        for unit_id in xrange(1, 7):
            port_id = 47
            n = "Unit %d Port %d" % (unit_id, port_id)
            print "Look for port", 'Generated Service ' + n
            svc = self.sched.services.find_srv_by_name_and_hostname("sw_0", 'Generated Service ' + n)
            self.assertIsNot(svc, None)

    def test_service_generators_array(self):

        host = self.sched.hosts.find_by_name("sw_1")
        host.checks_in_progress = []
        host.act_depend_of = []  # ignore the router

        print "All service of", "sw_1"
        for s in host.services:
            print self.sched.services[s].get_name()

        svc = self.sched.services.find_srv_by_name_and_hostname("sw_1", 'Generated Service Gigabit0/1')
        self.assertIsNot(svc, None)
        self.assertEqual('check_service!1!80%!90%', svc.check_command.call)

        svc = self.sched.services.find_srv_by_name_and_hostname("sw_1", 'Generated Service Gigabit0/2')
        self.assertIsNot(svc, None)
        self.assertEqual('check_service!2!80%!90%', svc.check_command.call)

        svc = self.sched.services.find_srv_by_name_and_hostname("sw_1", 'Generated Service Ethernet0/1')
        self.assertIsNot(svc, None)
        self.assertEqual('check_service!3!80%!95%', svc.check_command.call)

        svc = self.sched.services.find_srv_by_name_and_hostname("sw_1", 'Generated Service ISDN1')
        self.assertIsNot(svc, None)
        self.assertEqual('check_service!4!80%!95%', svc.check_command.call)


if __name__ == '__main__':
    unittest.main()
