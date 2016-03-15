# tokenizer.py
# 
# A simple interpreter for a lisp-like language in python

import sys
import sets

needsValue = sets.Set(["ID","INT","FLOAT","STRING"])
multiChar  = sets.Set(["ID","INT","FLOAT"])

def isalpha(char):
    if ord(char) in range(ord('A'),ord('Z')): return True
    else: return False

def isnumeric(char):
    if ord(char) in range(ord('0'),ord('9')): return True
    else: return False

def issymbol(char):
    if char == "+" or char == "-" or char == "*" or char == "/":
        return True
    else:
        return False

def tokenize_start(char,value):
    if   char == "(": return ("START", "LPAREN","")
    elif char == ")": return ("START", "RPAREN","")
    elif char == "[": return ("START", "LBRACK","")
    elif char == "]": return ("START", "RBRACK","")
    elif char == "\"": return ("STRING", "", "")
    elif isalpha(char) or issymbol(char): return ("ID","",char)
    elif isnumeric(char): return ("NUM","",char)
    else: return ("START", "", "")

def tokenize_id(char,value):
    if isalpha(char): return ("ID","",value + char)
    else: return ("START", "ID", value) 

def tokenize_num(char, value):
    if isnumeric(char): return ("NUM","",value + char)
    elif char == ".": return ("FLOAT", "", value + char) 
    else: return ("START", "INT", value)

def tokenize_float(char, value):
    if isnumeric(char): return ("FLOAT","",value + char)
    else: return ("START", "FLOAT", value)

def tokenize_string(char,value):
    if char == "\"": return ("START", "STRING", value)
    else: return ("STRING", "", value + char)

def emit_token(token,value):
    if token != "":
        if token in needsValue:
            return (token,value)
        else:
            return (token,"")

def tokenize(source):
    FSM = {
        "START"  : tokenize_start,
        "ID"     : tokenize_id,
        "NUM"    : tokenize_num,
        "FLOAT"  : tokenize_float,
        "STRING" : tokenize_string
    }
    state = "START"
    value = ""
    for char in source:
        state,token,value = FSM[state](char,value)
        t = emit_token(token,value)
        if t: yield t
        if token in multiChar:
            state,token,value = FSM["START"](char,"")
            t = emit_token(token,value)
            if t: yield t
    # If input ends on a variable-length token, process a character to terminate
    state,token,value = FSM[state]("\n",value)
    t = emit_token(token,value)
    if t: yield t

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for token in tokenize(sys.argv[1]):
            print token
    else:
        for token in tokenize(sys.stdin.read()):
            print token
