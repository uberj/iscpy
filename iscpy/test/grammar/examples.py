import parsley

import unittest
def make_simple(grammar, in_str, scope={}):
    x = parsley.makeGrammar(grammar, scope)
    return x(in_str).S()

class SimpleParsley(unittest.TestCase):
    def test1(self):
        """
        Match any char a-Z
        """
        grammar = """
            S = :c ?('a' <= c <= 'z' or 'A' <= c <= 'Z') -> c
        """
        self.assertEqual('a', make_simple(grammar, 'a'))

    def test2(self):
        """
        Match any char a-Z or secial chars
        """
        grammar = """
            letter = :c ?('a' <= c <= 'z' or 'A' <= c <= 'Z') -> c
            other = :c ?(c in ('-', '_', '.', "'", '"', ',')) -> c
            S = letter | other
        """
        self.assertEqual('a', make_simple(grammar, 'a'))
        self.assertEqual('_', make_simple(grammar, '_'))

    def test3(self):
        """
        Match multiple char or secial chars
        """
        grammar = """
            letter = :c ?('a' <= c <= 'z' or 'A' <= c <= 'Z') -> c
            other = :c ?(c in ('-', '_', '.', "'", '"', ',')) -> c
            all = letter | other
            S = <all*>
        """
        self.assertEqual('abb', make_simple(grammar, 'abb'))
        self.assertEqual('_"-', make_simple(grammar, '_"-'))
        self.assertEqual('kj-adf_"', make_simple(grammar, 'kj-adf_"'))

    def test4(self):
        """
        Alternation + Iteration: (pg 33)
            Consume one charater, then let another rule consume the other.
            consume charaters
        """
        grammar = """
            match_a = 'a':c -> ('match_a', c)
            match_b = 'b':c -> ('match_b', c)

            match_ab = match_a:r | match_b:r -> r
            S = match_ab*
        """
        self.assertEqual(
            [('match_a', 'a'), ('match_b', 'b')], make_simple(grammar, 'ab')
        )
        self.assertEqual(
            [('match_a', 'a'), ('match_a', 'a')], make_simple(grammar, 'aa')
        )

    def test5(self):
        """
        Alternation + Iteration 2: (pg 33)
        """
        grammar = """
            S = ('b' | 'a')
        """
        self.assertEqual(
            'a', make_simple(grammar, 'a')
        )
        grammar = """
            S = ('b' | 'a')*
        """
        self.assertEqual(
            ['a', 'b'], make_simple(grammar, 'ab')
        )


    def test6(self):
        """
        Token built in?
        """
        grammar = """
            S = token('a')
        """
        self.assertEqual(
            ' a ', make_simple(grammar, 'a')
        )


if __name__ == '__main__':
    unittest.main()
