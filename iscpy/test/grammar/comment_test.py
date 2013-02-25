from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp
from iscpy.parse import scrub_comments_and_nl


class ISCRealSubnetTests(BaseTest):

    def setUp(self):
        super(ISCRealSubnetTests, self).setUp()

        self.real_grammar = self.isc_grammar + """
            S = uncommented
        """
    def test_single_line(self):
        test_param = """1 2 # skip
        no 
        888 # skip me
4
4
        
        
        888 # skip me
        3
        """
        # If it parses, we are probably good
        print scrub_comments_and_nl(test_param)
        #self.assertTrue('asdf' not in res)
        #self.assertTrue('#' not in res)

    def test_multi_line(self):
        test_param = """
        top
        /*
        asdf
        */
        bottom # skip me
        """
        # If it parses, we are probably good
        print scrub_comments_and_nl(test_param)



if __name__ == '__main__':
    import unittest
    unittest.main()
