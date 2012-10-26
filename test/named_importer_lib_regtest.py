#!/usr/bin/python

# Copyright (c) 2009, Purdue University
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# 
# Neither the name of the Purdue University nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Regression test for iscpy.py

Make sure you are running this against a database that can be destroyed.

DO NOT EVER RUN THIS TEST AGAINST A PRODUCTION DATABASE.
"""

__copyright__ = 'Copyright (C) 2009, Purdue University'
__license__ = 'BSD'
__version__ = '#1.0.3#'


import unittest
import os

import iscpy


NAMED_FILE = 'test_data/named.example.conf'


class TestNamedImport(unittest.TestCase):

  def setUp(self):
    self.named_file = open(NAMED_FILE).read()
    self.maxDiff = None

  def testScrubComments(self):
    self.assertEqual(iscpy.ScrubComments(self.named_file),
                     'options {\ndirectory "/var/domain";\nrecursion yes;\n'
                     'allow-query { any; };\nmax-cache-size 512M;\n};\n\n'
                     'logging {\nchannel "security" {\n'
                     'file "/var/log/named-security.log" '
                     'versions 10 size 10m;\nprint-time yes;\n};\n'
                     'channel "query_logging" {\nsyslog local5;\n'
                     'severity info;\n};\ncategory "client" { "null"; };\n'
                     'category "update-security" { "security"; };\n'
                     'category "queries" { "query_logging"; };\n};\n\n'
                     'controls {\ninet * allow { control-hosts; } keys '
                     '{rndc-key; };\n};\n\ninclude "/etc/rndc.key";\n\n'
                     'acl control-hosts {\n127.0.0.1/32;\n192.168.1.3/32;\n};\n'
                     '\nacl admin {\n192.168.0.0/16;\n192.168.1.2/32;\n'
                     '192.168.1.4/32;\n};\n\nview "unauthorized" {\n'
                     'recursion no;\nmatch-clients { network-unauthorized; };\n'
                     'additional-from-auth no;\nadditional-from-cache no;\n\n'
                     'zone "0.0.127.in-addr.arpa" {\ntype slave;\n'
                     'file "test_data/university.rev.bak";\nmasters {\n'
                     '192.168.1.3;\n'
                     '};\n};\n\nzone "1.210.128.in-addr.arpa" {\ntype master;\n'
                     'file "test_data/test_reverse_zone.db";\n'
                     'allow-query { network-unauthorized; };\n};\n\n'
                     'zone "." {\ntype hint;\nfile "named.ca";\n};\n};\n\n'
                     'view "authorized" {\nrecursion yes;\n'
                     'match-clients { network-authorized; };\n'
                     'allow-recursion { network-authorized; };\n'
                     'allow-query-cache { network-authorized; };\n'
                     'additional-from-auth yes;\nadditional-from-cache yes;\n\n'
                     'zone "university.edu" {\ntype slave;\n'
                     'file "test_data/university.db.bak";\nmasters {\n'
                     '192.168.11.37;\n};\ncheck-names ignore;\n};\n\n'
                     'zone "smtp.university.edu" {\ntype master;\n'
                     'file "test_data/test_zone.db";\nmasters {\n'
                     '192.168.11.37;\n};\n};\n\nzone "." {\ntype hint;\n'
                     'file "named.ca";\n};\n};\n\n')
  def testExplode(self):
    self.assertEqual(iscpy.Explode(self.named_file),
                     ['options', '{', 'directory "/var/domain"', ';',
                      'recursion yes', ';', 'allow-query', '{', 'any', ';', '}',
                      ';', 'max-cache-size 512M', ';', '}', ';', 'logging', '{',
                      'channel "security"', '{',
                      'file "/var/log/named-security.log" versions 10 size 10m',
                      ';', 'print-time yes', ';', '}', ';',
                      'channel "query_logging"', '{', 'syslog local5', ';',
                      'severity info', ';', '}', ';', 'category "client"', '{',
                      '"null"', ';', '}', ';', 'category "update-security"',
                      '{', '"security"', ';', '}', ';', 'category "queries"',
                      '{', '"query_logging"', ';', '}', ';', '}', ';',
                      'controls', '{', 'inet * allow', '{', 'control-hosts',
                      ';', '}', 'keys', '{', 'rndc-key', ';', '}', ';',
                      '}', ';', 'include "/etc/rndc.key"', ';',
                      'acl control-hosts', '{', '127.0.0.1/32', ';',
                      '192.168.1.3/32', ';', '}', ';', 'acl admin', '{',
                      '192.168.0.0/16', ';', '192.168.1.2/32', ';',
                      '192.168.1.4/32', ';', '}', ';', 'view "unauthorized"',
                      '{', 'recursion no', ';', 'match-clients', '{',
                      'network-unauthorized', ';', '}', ';',
                      'additional-from-auth no', ';',
                      'additional-from-cache no', ';',
                      '//\t// Loopback network\t//\tzone "0.0.127.in-addr.arpa"',
                      '{', 'type slave', ';',
                      'file "test_data/university.rev.bak"',
                      ';', 'masters', '{', '192.168.1.3', ';', '}', ';', '}',
                      ';',
                      '//\t// 192.168.1.0/24\t//\tzone "1.210.128.in-addr.arpa"',
                      '{', 'type master', ';',
                      'file "test_data/test_reverse_zone.db"', ';',
                      'allow-query', '{', 'network-unauthorized', ';', '}', ';',
                      '}', ';', '//\t// Cache File\t//\tzone "."', '{',
                      'type hint', ';', 'file "named.ca"', ';', '}', ';', '}',
                      ';', 'view "authorized"', '{', 'recursion yes', ';',
                      'match-clients', '{', 'network-authorized', ';', '}', ';',
                      'allow-recursion', '{', 'network-authorized', ';', '}',
                      ';', 'allow-query-cache', '{', 'network-authorized', ';',
                      '}', ';', 'additional-from-auth yes', ';',
                      'additional-from-cache yes', ';', 'zone "university.edu"',
                      '{', 'type slave', ';',
                      'file "test_data/university.db.bak"', ';', 'masters', '{',
                      '192.168.11.37', ';', '}', ';', 'check-names ignore', ';',
                      '}', ';',
                      '//\t// Internal view of "smtp.university.edu"\t//\tzone "smtp.university.edu"',
                      '{', 'type master', ';', 'file "test_data/test_zone.db"',
                      ';', 'masters', '{', '192.168.11.37', ';', '}', ';', '}',
                      ';', '//\t// Cache File\t//\tzone "."', '{', 'type hint',
                      ';', 'file "named.ca"', ';', '}', ';', '}', ';'])

  def testParse(self):
    self.assertEqual(iscpy.ParseTokens(
        iscpy.Explode(
            iscpy.ScrubComments(self.named_file))),
        {'acl control-hosts': {'127.0.0.1/32': True, '192.168.1.3/32': True},
         'acl admin': {'192.168.1.2/32': True, '192.168.1.4/32': True,
                       '192.168.0.0/16': True},
         'view "authorized"': {'zone "smtp.university.edu"':
             {'masters': {'192.168.11.37': True},
              'type': 'master', 'file': '"test_data/test_zone.db"'},
              'allow-query-cache': {'network-authorized': True},
              'allow-recursion': {'network-authorized': True},
              'recursion': 'yes',
              'zone "university.edu"': {'check-names': 'ignore',
                                        'masters': {'192.168.11.37': True},
              'type': 'slave', 'file': '"test_data/university.db.bak"'},
              'match-clients': {'network-authorized': True},
              'zone "."': {'type': 'hint', 'file': '"named.ca"'},
                           'additional-from-cache': 'yes',
                           'additional-from-auth': 'yes'},
              'controls': [{'inet * allow': {'control-hosts': True}},
                           {'keys': {'rndc-key': True}}],
          'view "unauthorized"': 
              {'zone "1.210.128.in-addr.arpa"':
                  {'allow-query': {'network-unauthorized': True},
                   'type': 'master',
                   'file': '"test_data/test_reverse_zone.db"'},
               'recursion': 'no',
               'match-clients': {'network-unauthorized': True},
               'zone "."': {'type': 'hint', 'file': '"named.ca"'},
               'zone "0.0.127.in-addr.arpa"': {
                   'masters': {'192.168.1.3': True}, 'type': 'slave',
                   'file': '"test_data/university.rev.bak"'},
               'additional-from-cache': 'no', 'additional-from-auth': 'no'},
               'logging': {'category "update-security"': {'"security"': True},
                           'category "queries"': {'"query_logging"': True},
                           'channel "query_logging"': 
                               {'syslog': 'local5', 'severity': 'info'},
                               'category "client"': {'"null"': True},
                               'channel "security"':
                                   {'file': '"/var/log/named-security.log" versions 10 size 10m',
                                    'print-time': 'yes'}},
          'include': '"/etc/rndc.key"',
          'options': {'directory': '"/var/domain"', 'recursion': 'yes',
                      'allow-query': {'any': True}, 'max-cache-size': '512M'}})

  def testMakeNamedDict(self):
    self.assertEqual(iscpy.dns.MakeNamedDict(self.named_file),
        {'acls': {'admin': ['192.168.1.2/32', '192.168.1.4/32',
                            '192.168.0.0/16'],
                  'control-hosts': ['127.0.0.1/32', '192.168.1.3/32']},
         'options': {'include': '"/etc/rndc.key"',
                     'logging': {'category "update-security"':
                         {'"security"': True},
                         'category "queries"': {'"query_logging"': True},
                         'channel "query_logging"':
                             {'syslog': 'local5', 'severity': 'info'},
                         'category "client"': {'"null"': True},
                         'channel "security"':
                         {'file': '"/var/log/named-security.log" versions 10 size 10m',
                              'print-time': 'yes'}},
                     'options': {'directory': '"/var/domain"',
                                 'recursion': 'yes',
                                 'allow-query': {'any': True},
                                 'max-cache-size': '512M'},
                     'controls': [{'inet * allow': {'control-hosts': True}},
                                  {'keys': {'rndc-key': True}}]},
         'orphan_zones': {},
         'views':
             {'authorized': {'zones':
                 {'university.edu':
                     {'type': 'slave',
                      'options': {'masters': {'192.168.11.37': True},
                                  'check-names': 'ignore'},
                      'file': 'test_data/university.db.bak'},
                  'smtp.university.edu':
                     {'type': 'master',
                      'options': {'masters': {'192.168.11.37': True}},
                      'file': 'test_data/test_zone.db'},
                  '.':
                     {'type': 'hint', 'options': {}, 'file': 'named.ca'}},
                 'options': {'allow-recursion': {'network-authorized': True},
                             'recursion': 'yes',
                             'match-clients': {'network-authorized': True},
                             'allow-query-cache': {'network-authorized': True},
                             'additional-from-cache': 'yes',
                             'additional-from-auth': 'yes'}},
              'unauthorized': {'zones':
                 {'0.0.127.in-addr.arpa':
                     {'type': 'slave',
                      'options': {'masters': {'192.168.1.3': True}},
                      'file': 'test_data/university.rev.bak'},
                  '1.210.128.in-addr.arpa':
                     {'type': 'master',
                      'options': {'allow-query':
                          {'network-unauthorized': True}},
                      'file': 'test_data/test_reverse_zone.db'},
                  '.':
                     {'type': 'hint', 'options': {}, 'file': 'named.ca'}},
              'options': {'recursion': 'no', 'additional-from-cache': 'no',
                          'match-clients': {'network-unauthorized': True},
                          'additional-from-auth': 'no'}}}})

  def testMakeZoneViewOptions(self):
    self.assertEqual(iscpy.dns.MakeZoneViewOptions(
        iscpy.dns.MakeNamedDict(self.named_file)),
        {'zones':
            {'university.edu':
                'masters { 192.168.11.37; };\n'
                'check-names ignore;',
             '0.0.127.in-addr.arpa': 'masters { 192.168.1.3; };',
             'smtp.university.edu': 'masters { 192.168.11.37; };',
             '1.210.128.in-addr.arpa': 'allow-query { network-unauthorized; };',
             '.': ''},
         'views':
            {'authorized': 'allow-recursion { network-authorized; };\n'
                           'recursion yes;\nmatch-clients { '
                           'network-authorized; };\nallow-query-cache { '
                           'network-authorized; };\nadditional-from-cache '
                           'yes;\nadditional-from-auth yes;',
             'unauthorized': 'recursion no;\nadditional-from-cache no;\n'
                             'match-clients { network-unauthorized; };\n'
                             'additional-from-auth no;'}})

  def testMakeNamedHeader(self):
    self.assertEqual(iscpy.dns.DumpNamedHeader(
        iscpy.dns.MakeNamedDict(self.named_file)),
        'include "/etc/rndc.key";\n'
        'logging { category "update-security" { "security"; };\n'
                  'category "queries" { "query_logging"; };\n'
                  'channel "query_logging" { syslog local5;\nseverity info; };\n'
                  'category "client" { "null"; };\n'
                  'channel "security" { file "/var/log/named-security.log" '
                                       'versions 10 size 10m;\nprint-time '
                                       'yes; }; };\n'
        'options { directory "/var/domain";\nrecursion yes;\n'
                  'allow-query { any; };\nmax-cache-size 512M; };\n'
        'controls { inet * allow { control-hosts; } keys { rndc-key; }; '
        '};')

  def testMakeISC(self):
    self.assertEqual(iscpy.MakeISC(
        {'level1': {'level2': {'level3': {'level4': {
            'test1': True, 'test2': True, 'test3': True}}}},
         'newarg': 'newval', 'new_stanza': {'test': True}}),
        'new_stanza { test; };\n'
        'level1 { level2 { level3 { level4 { test1;\n'
                                            'test3;\n'
                                            'test2; }; }; }; };\n'
        'newarg newval;')
    self.assertEqual(iscpy.MakeISC(iscpy.ParseISCString(self.named_file)),
      'acl control-hosts { 127.0.0.1/32;\n'
      '192.168.1.3/32; };\n'
      'acl admin { 192.168.1.2/32;\n'
      '192.168.1.4/32;\n'
      '192.168.0.0/16; };\n'
      'view "authorized" { zone "smtp.university.edu" { masters { 192.168.11.37; };\n'
      'type master;\n'
      'file "test_data/test_zone.db"; };\n'
      'allow-query-cache { network-authorized; };\n'
      'allow-recursion { network-authorized; };\n'
      'recursion yes;\n'
      'zone "university.edu" { check-names ignore;\n'
      'masters { 192.168.11.37; };\n'
      'type slave;\n'
      'file "test_data/university.db.bak"; };\n'
      'match-clients { network-authorized; };\n'
      'zone "." { type hint;\n'
      'file "named.ca"; };\n'
      'additional-from-cache yes;\n'
      'additional-from-auth yes; };\n'
      'controls { inet * allow { control-hosts; } keys { rndc-key; }; };\n'
      'view "unauthorized" { zone "1.210.128.in-addr.arpa" { allow-query { network-unauthorized; };\n'
      'type master;\n'
      'file "test_data/test_reverse_zone.db"; };\n'
      'recursion no;\n'
      'match-clients { network-unauthorized; };\n'
      'zone "." { type hint;\n'
      'file "named.ca"; };\n'
      'zone "0.0.127.in-addr.arpa" { masters { 192.168.1.3; };\n'
      'type slave;\n'
      'file "test_data/university.rev.bak"; };\n'
      'additional-from-cache no;\n'
      'additional-from-auth no; };\n'
      'logging { category "update-security" { "security"; };\n'
      'category "queries" { "query_logging"; };\n'
      'channel "query_logging" { syslog local5;\n'
      'severity info; };\n'
      'category "client" { "null"; };\n'
      'channel "security" { file "/var/log/named-security.log" versions 10 size 10m;\n'
      'print-time yes; }; };\n'
      'include "/etc/rndc.key";\n'
      'options { directory "/var/domain";\n'
      'recursion yes;\n'
      'allow-query { any; };\n'
      'max-cache-size 512M; };')

if( __name__ == '__main__' ):
  unittest.main()
