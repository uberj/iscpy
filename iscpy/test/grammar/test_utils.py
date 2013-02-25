import parsley
import pprint
import unittest
from iscpy.parse import scrub_comments

pp = pprint.PrettyPrinter(indent=4)

def make_simple(grammar, in_str, scope={}, strip=True):
    in_str = scrub_comments(in_str)
    in_str = in_str.replace('\n', '').strip()
    # TODO, stop using ScrubComments
    x = parsley.makeGrammar(grammar, scope)
    return x(in_str).S()


ISC_GRAMMAR_FILE = "/home/juber/repositories/iscpy/isc.parsley"

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.isc_grammar = ""
        for line in open(ISC_GRAMMAR_FILE).readlines():
            self.isc_grammar += ' ' * 12 + line
