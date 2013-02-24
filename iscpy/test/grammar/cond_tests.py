import sys
sys.path.insert(0, '')

from iscpy.test.grammar.test_utils import BaseTest, make_simple, pp
import unittest


class ISCCondTests(BaseTest):

    def setUp(self):
        super(ISCCondTests, self).setUp()
        self.if_grammar = self.isc_grammar + """
            S = stmt_list
        """
    def test_cond(self):
        test_param = """
            if exists gpxe.bus-id {
                    site-option-space "pxelinux";

                    if exists dhcp-parameter-request-list {
                        option dhcp-parameter-request-list = concat(option dhcp-parameter-request-list,d0,d1,d2,d3);
                    }
            }
        """
        #pp.pprint(make_simple(self.if_grammar, test_param))

    def test_nested(self):
        test_param = """
            if asdf a = d asdf {
                if asdf a = d asdf {
                    if asdf a = d asdf {
                        if asdf a = d asdf {
                            if asdf a = d asdf {
                            }
                        }
                    }
                    if asdf a = d asdf {
                        if asdf a = d asdf {
                        }
                    }
                }
                if asdf a = d asdf {
                    if asdf a = d asdf {
                    }
                }
            }
        """
        self.assertEqual(
        [   (   'condition',
            ('asdf a ', '=', 'd asdf '),
            'then',
            [   (   'condition',
                    ('asdf a ', '=', 'd asdf '),
                    'then',
                    [   (   'condition',
                            ('asdf a ', '=', 'd asdf '),
                            'then',
                            [   (   'condition',
                                    ('asdf a ', '=', 'd asdf '),
                                    'then',
                                    [   (   'condition',
                                            ('asdf a ', '=', 'd asdf '),
                                            'then',
                                            [])])]),
                        (   'condition',
                            ('asdf a ', '=', 'd asdf '),
                            'then',
                            [   (   'condition',
                                    ('asdf a ', '=', 'd asdf '),
                                    'then',
                                    [])])]),
                (   'condition',
                    ('asdf a ', '=', 'd asdf '),
                    'then',
                    [('condition', ('asdf a ', '=', 'd asdf '), 'then', [])])])],
            make_simple(self.if_grammar, test_param))

    def test_no_opts_if(self):
        test_param = """
            if a = d {
            }
        """
        self.assertEqual(
            [('condition', ('a ', '=', 'd '), 'then', [])],
            make_simple(self.if_grammar, test_param)
        )

    def test_if(self):
        test_param = """
            key_first bar;
            key_first bar;
            if a b c = d {
                key_second bar;
                key_second bar;
                if d = c {
                    key_third bar;
                    key_third bar;
                }
                key_fourth bar;
                key_fourth bar;
            }
            key_fifth bar;
            key_fifth bar;
        """
        self.assertEqual(
            [   ('parameter', 'key_first', 'bar'),
                ('parameter', 'key_first', 'bar'),
                (   'condition',
                    ('a b c ', '=', 'd '),
                    'then',
                    [   ('parameter', 'key_second', 'bar'),
                        ('parameter', 'key_second', 'bar'),
                        (   'condition',
                            ('d ', '=', 'c '),
                            'then',
                            [   ('parameter', 'key_third', 'bar'),
                                ('parameter', 'key_third', 'bar')]),
                        ('parameter', 'key_fourth', 'bar'),
                        ('parameter', 'key_fourth', 'bar')]),
                ('parameter', 'key_fifth', 'bar'),
                ('parameter', 'key_fifth', 'bar')],
            make_simple(self.if_grammar, test_param)
        )


if __name__ == '__main__':
    unittest.main()
