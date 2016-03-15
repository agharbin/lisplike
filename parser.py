import tokenizer
import sys

token_stream = []

def apply_func(f, args):
    if f == "+":
        return int(args[0]) + int(args[1])

def parse_expression():
    global token_stream

    token = token_stream.next()
    if token[0] != "ID":
        print "ERROR: expected identifier"
    func = token[1]
    args = []
    while token[0] != "RPAREN":
        token = token_stream.next()
        args.append(token[1])
    return apply_func(func, args)

def parse():
    global token_stream
    
    token = token_stream.next()
    if token[0] == "LPAREN":
        return parse_expression()
    elif token[0] == "LBRACK":
        return parse_list()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token_stream = tokenizer.tokenize(sys.argv[1])
        print parse()
    else:
        token_stream = tokenizer.tokenize(sys.stdin.read())
        print parse()
