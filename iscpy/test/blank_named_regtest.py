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
    self.named_file = (
        'include "/home/jcollins/roster-dns-management/test/test_data/rndc.key";'
        'options { pid-file "test_data/named.pid";};\n'
        'controls { inet 127.0.0.1 port 35638 allow{localhost;} keys {rndc-key;};};')
    self.maxDiff = None


  def testParse(self):
    self.assertEqual(iscpy.Explode(iscpy.ScrubComments(self.named_file)),
        ['include "/home/jcollins/roster-dns-management/test/test_data/rndc.key"',
         ';', 'options', '{', 'pid-file "test_data/named.pid"', ';', '}', ';',
         'controls', '{', 'inet 127.0.0.1 port 35638 allow', '{', 'localhost',
         ';', '}', 'keys', '{', 'rndc-key', ';', '}', ';', '}', ';'])
    self.assertEqual(iscpy.ParseISCString(self.named_file),
        {'include': '"/home/jcollins/roster-dns-management/test/test_data/rndc.key"',
         'options': {'pid-file': '"test_data/named.pid"'},
         'controls': [{'inet 127.0.0.1 port 35638 allow': {'localhost': True}},
                      {'keys': {'rndc-key': True}}]})
    self.assertEqual(iscpy.MakeISC(iscpy.ParseISCString(self.named_file)),
        'include "/home/jcollins/roster-dns-management/test/test_data/rndc.key";\n'
        'options { pid-file "test_data/named.pid"; };\n'
        'controls { inet 127.0.0.1 port 35638 allow { localhost; } keys { rndc-key; }; };')

if( __name__ == '__main__' ):
  unittest.main()
