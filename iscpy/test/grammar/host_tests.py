from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp


class ISCHostParseTests(BaseTest):

    def setUp(self):
        super(ISCHostParseTests, self).setUp()

        self.host_grammar = self.isc_grammar + """
            S = stmt_list
        """
    def test_no_options(self):
        test_param = """
            host foo.bar.scl3.mozilla.com-nic2  {
            }
        """
        self.assertEqual(
            [('host', 'foo.bar.scl3.mozilla.com-nic2', [])],
            make_simple(self.host_grammar, test_param)
        )

    def test_options(self):
        test_param = """
            host foo.bar.scl3.mozilla.com-nic2  {
                foo bar;
                foo bar;
                foo bar;
            }
        """
        self.assertEqual(
            [(   'host',
                'foo.bar.scl3.mozilla.com-nic2',
                [   ('parameter', 'foo', 'bar'),
                    ('parameter', 'foo', 'bar'),
                    ('parameter', 'foo', 'bar')])],
            make_simple(self.host_grammar, test_param)
        )
    def test_multiple(self):
        test_param = """
            host foo.bar.scl3.mozilla.com-nic2  {
                foo bar;
                foo bar;
            }
            host foo.bar.scl3.mozilla.com-nic2  {
                foo bar;
                foo bar;
            }
            host foo.bar.scl3.mozilla.com-nic2  {
                foo bar;
                foo bar;
            }
        """
        self.assertEqual(
            [   (   'host',
                    'foo.bar.scl3.mozilla.com-nic2',
                    [('parameter', 'foo', 'bar'), ('parameter', 'foo', 'bar')]),
                (   'host',
                    'foo.bar.scl3.mozilla.com-nic2',
                    [('parameter', 'foo', 'bar'), ('parameter', 'foo', 'bar')]),
                (   'host',
                    'foo.bar.scl3.mozilla.com-nic2',
                    [('parameter', 'foo', 'bar'), ('parameter', 'foo', 'bar')])],
            make_simple(self.host_grammar, test_param))

if __name__ == '__main__':
    import unittest
    unittest.main()
