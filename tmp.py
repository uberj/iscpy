import sys
sys.path.insert(0, '')

from iscpy.iscpy_core.core import ParseISCString

test_file = 'test/test_data/dhcpd.example.conf'

ParseISCString(open(test_file, 'r').read())

