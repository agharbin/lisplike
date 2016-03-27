import tokenizer
import sys

token_stream = []
next_token = []

var_dict = {}

def add_items(args):
    return reduce(lambda x,y: ("INT",x[1]+y[1]), args, ("INT",0))

def mult_items(args):
    return reduce(lambda x,y: ("INT",x[1]*y[1]), args, ("INT",1))

def sub_items(args):
    return ("INT", args[0][1] - args[1][1])

def div_items(args):
    return ("INT", args[0][1] / args[1][1])

def define(args):
    var_dict[args[0][1]] = args[1]

def expect(item, t_type):
    if item[0] != t_type:
        print "Error: expected", t_type
        sys.exit()

var_dict["+"] = ("FUNC", add_items)
var_dict["-"] = ("FUNC", sub_items)
var_dict["*"] = ("FUNC", mult_items)
var_dict["/"] = ("FUNC", div_items)

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
    if id_name not in var_dict:
        print "Error:", id_name, "not defined"
        sys.exit()
    return var_dict[id_name]

def parse_expression():
    global next_token

    if next_token[0] == "ID":
        result = next_token[1]
        get_next()
        return lookup(result)
    elif next_token[0] == "INT":
        result = int(next_token[1])
        get_next()
        return ("INT",result)
    elif next_token[0] == "FLOAT":
        result = float(next_token[1])
        get_next()
        return ("FLOAT",result)
    elif next_token[0] == "STRING":
        result = next_token[1]
        get_next()
        return ("STRING",result)
    elif next_token[0] == "LPAREN":
        get_next() # skip left parentheses

        expect(next_token,"ID")

        # Handle define calls
        if next_token[1] == "DEF":
            get_next()
            name = next_token[1]

            get_next()
            rest = parse_expression()

            var_dict[name] = rest
            
            expect(next_token,"RPAREN")
            get_next() # move past right paren
        # Handle function calls
        else:
            func = parse_expression() # get function name

            args = []
            while next_token[0] != "RPAREN":
                args.append(parse_expression())

            get_next() # advance past right paren
            return apply_func(func, args)

def parse():
    global next_token
    
    while next_token != "EOF":
        result = parse_expression()
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
