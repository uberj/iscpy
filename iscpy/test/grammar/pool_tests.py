from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp


class ISCPoolParseTests(BaseTest):

    def setUp(self):
        super(ISCPoolParseTests, self).setUp()

        self.host_grammar = self.isc_grammar + """
            S = stmt_list
        """
    def test_no_options(self):
        test_param = """
            pool {
                foo bar;
            }
        """
        self.assertEqual(
            [('pool', [('parameter', 'foo', 'bar')])],
            make_simple(self.host_grammar, test_param)
        )

    def test_multiple(self):
        test_param = """
            pool {
                failover peer "dhcp-failover";
                deny dynamic bootp clients;
                range 10.0.0.0 10.0.0.247;
            }
        """
        self.assertEqual(
            [   (   'pool',
                [   ('parameter', 'failover', 'peer "dhcp-failover"'),
                    ('parameter', 'deny', 'dynamic bootp clients'),
                    ('parameter', 'range', '10.0.0.0 10.0.0.247')])],
            make_simple(self.host_grammar, test_param)
        )

if __name__ == '__main__':
    import unittest
    unittest.main()
