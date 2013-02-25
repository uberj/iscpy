import sys
import parsley
import pprint
from parsley import wrapGrammar

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



ISC_GRAMMAR_FILE = "/home/juber/repositories/iscpy/isc.parsley"
grammar = open(ISC_GRAMMAR_FILE).read()
grammar += '\nS = stmt_list'

path_swap = ('/etc/dhcpconfig-autodeploy',
"/home/juber/sysadmins/dhcpconfig/dhcpconfig-autodeploy/mtv1")

class ISCGrammar(parsley.makeGrammar(grammar, {}, unwrap=True)):
    def resolve_include(self, path):
        fname = path.replace(*path_swap)
        return parse_file(fname)

def construct(scope={}):
    return wrapGrammar(ISCGrammar)

def parse(in_str):
    in_str = scrub_comments(in_str)
    in_str = in_str.replace('\n', '').strip()
    g = construct()
    return g(in_str).S()

def parse_file(fname):
    contents = open(fname).read()
    return parse(contents)

def main(argv):
    fname = argv[1]
    print fname
    pp.pprint(parse_file(fname))

if __name__ == '__main__':
    main(sys.argv)
