import parsley
import pprint
import unittest
from iscpy.iscpy_core.core import ScrubComments

pp = pprint.PrettyPrinter(indent=4)

def make_simple(grammar, in_str, scope={}):
    in_str = in_str.replace('\n', '').strip()
    # TODO, stop using ScrubComments
    in_str = ScrubComments(in_str)
    x = parsley.makeGrammar(grammar, scope)
    return x(in_str).S()


ISC_GRAMMAR_FILE = "/home/juber/repositories/iscpy/isc.parsley"

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.isc_grammar = ""
        for line in open(ISC_GRAMMAR_FILE).readlines():
            self.isc_grammar += ' ' * 12 + line
