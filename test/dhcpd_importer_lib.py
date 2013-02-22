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
import iscpy


NAMED_FILE = 'test_data/dhcpd.example.conf'


class TestNamedImport(unittest.TestCase):
  def testMakeNamedHeader(self):
    return
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
