import parsley
from iscpy.test.grammar.test_utils import BaseTest, make_simple


class ISCSubnetParseTests(BaseTest):

    def setUp(self):
        super(ISCSubnetParseTests, self).setUp()

    def test_bracket(self):
        test_param = """
            {
                foo  bar;
            }
        """
        grammar = self.isc_grammar + """
            S = '{' ws option*:opts '}' -> opts
        """
        self.assertEqual(
            [('parameter', 'foo', 'bar')],
            make_simple(grammar, test_param)
        )

    def test_bracket2(self):
        test_param = """
            {
                foo  bar;
            option foo-option         10.0.0.5;
                foo  baz;
            option bar-option         10.0.0.5;
            }
        """
        grammar = self.isc_grammar + """
            S = '{' ws option*:opts '}' -> opts
        """
        self.assertEqual(
            [('parameter', 'foo', 'bar'), ('option', 'foo-option', '10.0.0.5'),
                ('parameter', 'foo', 'baz'),
                ('option', 'bar-option', '10.0.0.5')],
            make_simple(grammar, test_param)
        )

    def test_octet(self):
        # Make sure we aren't being greedy
        grammar = self.isc_grammar + """
            S = octet:o1 ' ' octet:o2 -> (o1, o2)
        """
        self.assertEqual(('0', '0'), make_simple(grammar, '0 0'))

        grammar = self.isc_grammar + """
            S = octet
        """
        self.assertEqual('0', make_simple(grammar, '0'))
        self.assertEqual('255', make_simple(grammar, '255'))
        self.assertEqual('100', make_simple(grammar, '100'))
        self.assertRaises(parsley.ParseError, make_simple, *(grammar, '256'))
        self.assertRaises(parsley.ParseError, make_simple, *(grammar, '00'))
        self.assertRaises(parsley.ParseError, make_simple, *(grammar, '011'))
        examples = ['1', '111', '0', '200']
        for example in examples:
            self.assertEqual(example, make_simple(grammar, example))

    def test_ipv4(self):
        grammar = self.isc_grammar + """
            S = ipv4_address
        """
        self.assertEqual('10.0.0.0', make_simple(grammar, '10.0.0.0'))
        examples = [
            '10.0.0.1',
            '255.0.0.0',
            '255.255.0.0',
            '255.255.255.0',
            '255.255.255.255',
            '255.255.255.254'
        ]
        for example in examples:
            self.assertEqual(example, make_simple(grammar, example))

    def test_subnet(self):
        grammar = self.isc_grammar + """
            S = subnet_stmt
        """
        test_in = """
            subnet 10.0.0.0 netmask 10.0.0.0 {
                foo bar;
                foo 10.0.0.0;
            }
        """
        self.assertEqual(
                ('subnet', {
                    'body': [('parameter', 'foo', 'bar'), ('parameter', 'foo', '10.0.0.0')],
                    'netmask': '10.0.0.0',
                    'network': '10.0.0.0'
                    }
                ),
        make_simple(grammar, test_in))

    def test_subnet_if(self):
        grammar = self.isc_grammar + """
            S = subnet_stmt
        """
        test_in = """
            subnet 10.0.0.0 netmask 10.0.0.0 {
                foo bar;
                foo 10.0.0.0;
                if foo = bar {
                    option baz 10.0.0.0;

                }
                baz foo 10.1.0.0;
            }
        """
        self.assertEqual(
            (   'subnet',
                {   'body': [   ('parameter', 'foo', 'bar'),
                                ('parameter', 'foo', '10.0.0.0'),
                                (   'condition',
                                    ('foo ', '=', 'bar '),
                                    'then',
                                    [('option', 'baz', '10.0.0.0')]),
                                ('parameter', 'baz', 'foo 10.1.0.0')],
                    'netmask': '10.0.0.0',
                    'network': '10.0.0.0'}),
            make_simple(grammar, test_in)
        )

if __name__ == '__main__':
    import unittest
    unittest.main()
