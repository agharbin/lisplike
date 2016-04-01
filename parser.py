import tokenizer
import sys

token_stream = []
next_token = []

environment = {}

def add_items(args):
    return reduce(lambda x,y: ("INT",x[1]+y[1]), args, ("INT",0))

def mult_items(args):
    return reduce(lambda x,y: ("INT",x[1]*y[1]), args, ("INT",1))

def sub_items(args):
    return ("INT", args[0][1] - args[1][1])

def div_items(args):
    return ("INT", args[0][1] / args[1][1])

def define(args):
    environment[args[0][1]] = args[1]

def expect(item, t_type):
    if item[0] != t_type:
        print "Error: expected", t_type
        sys.exit()

environment["+"] = ("FUNC", add_items)
environment["-"] = ("FUNC", sub_items)
environment["*"] = ("FUNC", mult_items)
environment["/"] = ("FUNC", div_items)

def get_next():
    global token_stream
    global next_token

    try:
        next_token = token_stream.next()
    except StopIteration:
        next_token = "EOF"

def apply_func(f, args):
    expect(f,"FUNC")
    return f[1](args)

def lookup(id_name):
    if id_name not in environment:
        print "Error:", id_name, "not defined"
        sys.exit()
    return environment[id_name]

def evaluate(expr):
    if isinstance(expr, tuple):
        if expr[0] == "ID":
            return lookup(expr[1])
        else:
            return expr # literal
    elif isinstance(expr, list): # We have a function application
        f = expr[0]
        if f[1] == "DEF":
            name = expr[1]
            val  = expr[2]
            environment[name[1]] = evaluate(val)
        else: # function application
            func = evaluate(f)
            args = []
            for e in expr[1:]:
                args.append(evaluate(e))
            return apply_func(func, args)
    else: # error
        print "Evaluate error"


def parse_expression():
    global next_token

    if next_token[0] == "LPAREN":
        get_next() # skip left parentheses

        elements = []
        while next_token[0] != "RPAREN":
            elements.append(parse_expression())

        get_next() # advance past right paren
        return elements
    elif next_token[0] == "INT":
        result = ("INT",int(next_token[1]))
        get_next()
        return result
    elif next_token[0] == "FLOAT":
        result = ("INT",int(next_token[1]))
        get_next()
        return result
    else: # String type
        result = next_token
        get_next()
        return result

def parse():
    global next_token
    
    while next_token != "EOF":
        result = evaluate(parse_expression())
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token_stream = tokenizer.tokenize(sys.argv[1])
        get_next()
        print parse()[1]
    else:
        token_stream = tokenizer.tokenize(sys.stdin.read())
        get_next()
        print parse()[1]
