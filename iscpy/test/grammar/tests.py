import sys
sys.path.insert(0, '')
import unittest
from iscpy.test.grammar.option_tests import *
from iscpy.test.grammar.subnet_tests import *
from iscpy.test.grammar.cond_tests import *
from iscpy.test.grammar.host_tests import *
from iscpy.test.grammar.pool_tests import *
from iscpy.test.grammar.real_subnet_test import *



if __name__ == '__main__':
    unittest.main()

