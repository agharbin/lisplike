import tokenizer
import sys

token_stream = []
next_token = []

def get_next():
    global token_stream
    global next_token

    try:
        next_token = token_stream.next()
    except StopIteration:
        pass

def apply_func(f, args):
    # handle primitives
    if f == "+":
        result = 0
        for i in args:
            result = result + i
        return result
    if f == "-":
        return args[0] - args[1]
    if f == "*":
        result = 1
        for i in args:
            result = result * i
        return result
    if f == "/":
        return args[0] / args[1]

def parse_expression():
    global next_token

    if next_token[0] == "ID":
        pass # unimplemented
    elif next_token[0] == "INT":
        result = int(next_token[1])
        get_next()
        return result
    elif next_token[0] == "FLOAT":
        result = float(next_token[1])
        get_next()
        return result
    elif next_token[0] == "STRING":
        result = next_token[1]
        get_next()
        return result
    elif next_token[0] == "LPAREN":
        get_next() # skip left parentheses
    
        if next_token[0] != "ID":
            print "ERROR: expected identifier"
        func = next_token[1]
        get_next() # advance past function name

        args = []
        while next_token[0] != "RPAREN":
            args.append(parse_expression())

        get_next() # advance past right paren
        return apply_func(func, args)

def parse():
    global next_token
    
    get_next()
    if next_token[0] == "LBRACK":
        return parse_list()
    else:
        return parse_expression()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token_stream = tokenizer.tokenize(sys.argv[1])
        print parse()
    else:
        token_stream = tokenizer.tokenize(sys.stdin.read())
        print parse()
