# tokenizer.py
# 
# A simple interpreter for a lisp-like language in python

import sys
import sets

needsValue = sets.Set(["ID","INT","FLOAT","STRING"])

def isalpha(char):
    if ord(char) in range(ord('A'),ord('Z')): return True
    else: return False

def isnumeric(char):
    if ord(char) in range(ord('0'),ord('9')): return True
    else: return False

def tokenize_start(char,value):
    if   char == "(": return ("LPAREN", "","")
    elif char == ")": return ("RPAREN", "","")
    elif isalpha(char): return ("ID","",char)
    elif isnumeric(char): return ("NUM","",char)
    else: return ("START", "", "")

def tokenize_id(char,value):
    if isalpha(char): return ("ID","",value + char)
    elif char == "(": return ("LPAREN","ID",value)
    elif char == ")": return ("RPAREN","ID",value)
    else: return ("START", "ID", value) # End of input case

def tokenize_lparen(char,value):
    if isalpha(char): return ("ID","LPAREN",char)
    elif char == "(": return ("LPAREN","LPAREN","")
    elif char == ")": return ("RPAREN","LPAREN","")
    else: return ("START","LPAREN","")

def tokenize_rparen(char,value):
    if isalpha(char): return ("ID","RPAREN",char)
    elif char == "(": return ("LPAREN","RPAREN","")
    elif char == ")": return ("RPAREN","RPAREN","")
    else: return ("START","RPAREN","")

def tokenize_num(char, value):
    if isnumeric(char): return ("NUM","",value + char)
    elif char == ".": return ("FLOAT", "", value + char) 
    elif char == "(": return ("LPAREN","INT",value)
    elif char == ")": return ("RPAREN","INT",value)
    else: return ("START", "INT", value)

def tokenize_float(char, value):
    if isnumeric(char): return ("FLOAT","",value + char)
    elif char == "(": return ("LPAREN","FLOAT",value)
    elif char == ")": return ("RPAREN","FLOAT",value)
    else: return ("START", "FLOAT", value)

def tokenize(source):
    FSM = {
        "START"  : tokenize_start,
        "ID"     : tokenize_id,
        "LPAREN" : tokenize_lparen,
        "RPAREN" : tokenize_rparen,
        "NUM"    : tokenize_num,
        "FLOAT"  : tokenize_float
    }
    state = "START"
    value = ""
    for char in source:
        state,token,value = FSM[state](char,value)
        if token != "":
            if token in needsValue:
                yield (token,value)
            else:
                yield (token,"")

    state,token,value = FSM[state](" ",value)
    if token != "":
        if token in needsValue:
            yield (token,value)
        else:
            yield (token,"")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for token in tokenize(sys.argv[1]):
            print token
    else:
        for token in tokenize(sys.stdin.read()):
            print token
