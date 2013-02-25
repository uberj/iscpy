import sys
import parsley
import pprint

pp = pprint.PrettyPrinter(indent=4)

def scrub_comments(in_str):
    new_str = ''
    index = 0
    while index < len(in_str):
        c = in_str[index]
        if c == '#':
            while True:
                index += 1
                if index >= len(in_str):
                    break
                if in_str[index] == '\n':
                    break
            continue # Back to top
        elif index < len(in_str) - 2 and c == '/' and in_str[index+1] == '*':
            while True:
                index += 2
                if (index < len(in_str) - 2 and
                        in_str[index] == '*' and in_str[index + 1] == '/'):
                    break
            index = index + 2  # skip close
            continue # Back to top
        new_str += c
        index += 1
    return new_str


def make_simple(grammar, in_str, scope={}, strip=True):
    in_str = scrub_comments(in_str)
    in_str = in_str.replace('\n', '').strip()
    # TODO, stop using ScrubComments
    x = parsley.makeGrammar(grammar, scope)
    return x(in_str).S()


ISC_GRAMMAR_FILE = "/home/juber/repositories/iscpy/isc.parsley"

def main(argv):
    fname = argv[1]
    print fname
    contents = open(fname).read()
    grammar = open(ISC_GRAMMAR_FILE).read()
    grammar += '\nS = subnet_stmt'
    contents.strip()
    pp.pprint(make_simple(grammar, contents))

if __name__ == '__main__':
    main(sys.argv)
