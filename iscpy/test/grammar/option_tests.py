import unittest

from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp

class ISCOptionParseTests(BaseTest):

    def setUp(self):
        super(ISCOptionParseTests, self).setUp()

        self.test_single_option_grammar = self.isc_grammar + """
            S = option
        """

        self.test_options_grammar = self.isc_grammar + """
            options = option*
            S = options
        """

    def test1(self):
        """
        Match any char a-Z or secial chars
        """
        grammar = self.isc_grammar + """
            S = letter | other
        """
        self.assertEqual('a', make_simple(grammar, 'a'))
        self.assertEqual('_', make_simple(grammar, '_'))

    def test3(self):
        """
        Match multiple char or secial chars
        """
        grammar = self.isc_grammar + """
            all = letter | other
            S = <all*>
        """
        self.assertEqual('abb', make_simple(grammar, 'abb'))
        self.assertEqual('_"-', make_simple(grammar, '_"-'))
        self.assertEqual('kj-adf_"', make_simple(grammar, 'kj-adf_"'))

    def test_option(self):
        """
            Match one option at a time
        """
        grammar = self.isc_grammar + """
            S = option
        """
        test_option1 = "option foo    bar;"
        self.assertEqual(('option', 'foo', 'bar'), make_simple(grammar, test_option1))

        test_option2 = "option foo    bar baz;"
        self.assertEqual(('option', 'foo', 'bar baz'), make_simple(grammar, test_option2))

        test_option3 = "option domain-name-servers 10.22.75.40, 10.22.75.41;"
        self.assertEqual(
            ('option', 'domain-name-servers', '10.22.75.40, 10.22.75.41'),
            make_simple(grammar, test_option3)
        )

        test_option4 = 'option domain-search       "foobar.com", "dc1.foobar.com", "foobar.org", "foobar.net";'
        self.assertEqual(
            ('option', 'domain-search', '"foobar.com", "dc1.foobar.com", "foobar.org", "foobar.net"'),
            make_simple(grammar, test_option4)
        )

    def test_options1(self):
        """
            Match multiple options at a time
        """
        test_option1 = """   option foo    bar;"""
        self.assertEqual([('option', 'foo', 'bar')], make_simple(self.test_options_grammar, test_option1))

    def test_options2(self):
        test_option2 = """
            option foo    bar;
            option baz    bee;
        """
        self.assertEqual(
            [('option', 'foo', 'bar'), ('option', 'baz', 'bee')],
            make_simple(self.test_options_grammar, test_option2)
        )

    def test_options3(self):
        test_option3 = """
            option ntp-servers         10.0.0.5;
            option subnet-mask         255.255.255.0;
            option routers             10.0.0.1;
            option domain-name-servers 10.22.75.40, 10.22.75.41;
            option domain-search       "foobar.com", "dc1.foobar.com", "foobar.org", "foobar.net";
            option domain-name         "foobar.com";
        """
        self.assertEqual(
        [
            ('option', 'ntp-servers', '10.0.0.5'),
            ('option', 'subnet-mask', '255.255.255.0'),
            ('option', 'routers', '10.0.0.1'),
            ('option', 'domain-name-servers', '10.22.75.40, 10.22.75.41'),
            ('option', 'domain-search', '"foobar.com", "dc1.foobar.com", "foobar.org", "foobar.net"'),
            ('option', 'domain-name', '"foobar.com"')
        ], make_simple(self.test_options_grammar, test_option3))

    def test_paramter1(self):

        test_param = """foo  bar;"""

        self.assertEqual(
            ('parameter', 'foo', 'bar'),
            make_simple(self.test_single_option_grammar, test_param)
        )

    def test_paramter2(self):

        test_param = """
            foo  bar;
            next-server                10.0.0.5;
            next-server                11.0.0.5;
        """

        self.assertEqual(
            [('parameter', 'foo', 'bar'), ('parameter', 'next-server',
                '10.0.0.5'), ('parameter', 'next-server', '11.0.0.5')],
            make_simple(self.test_options_grammar, test_param)
        )

    def test_option_paramter(self):

        test_param = """
            foo  bar;
            option foo-option         10.0.0.5;
            foo  baz;
            option bar-option         10.0.0.5;
        """

        self.assertEqual(
            [('parameter', 'foo', 'bar'), ('option', 'foo-option', '10.0.0.5'),
             ('parameter', 'foo', 'baz'), ('option', 'bar-option',
                 '10.0.0.5')],
            make_simple(self.test_options_grammar, test_param)
        )

    def test_bracket_option_paramter(self):
        test_param = """
            foo  bar;
            option foo-option         10.0.0.5;
            foo  baz;
            option bar-option         10.0.0.5;
        """

        self.assertEqual(
            [('parameter', 'foo', 'bar'), ('option', 'foo-option', '10.0.0.5'),
             ('parameter', 'foo', 'baz'), ('option', 'bar-option',
                 '10.0.0.5')],
            make_simple(self.test_options_grammar, test_param)
        )

    def test_equal_in_param(self):
        test_param = """
            option dhcp-parameter-request-list = concat(option dhcp-parameter-request-list,d0,d1,d2,d3);
        """

        self.assertEqual(
            [(  'parameter',
                'dhcp-parameter-request-list',
                'concat(option dhcp-parameter-request-list,d0,d1,d2,d3)')],
            make_simple(self.test_options_grammar, test_param)
        )

    def failing1(self):
        test_param = """
            option domain-name         "mozilla.com";
        """

        self.assertEqual(
                [('option', 'domain-name', '"mozilla.com"')],
                make_simple(self.test_options_grammar, test_param)
        )

    def failing2(self):
        test_param = """
            option gpxe.bus-id         code 177 = string;
        """

        print make_simple(self.test_options_grammar, test_param)
        return
        self.assertEqual(
                [('option', 'domain-name', '"mozilla.com"')],
                make_simple(self.test_options_grammar, test_param)
        )


if __name__ == '__main__':
    unittest.main()
