###Build a tree node###
import re
def check_match(p,expr):
    return p.match(expr) and p.match(expr).end() == len(expr)
p_function = re.compile("[a-zA-Z_][a-zA-Z_0-9]*[(].*[)]")
class Node(object):
    def __init__(self, typ, val, left=None, right=None):
        self.typ=typ
        self.val=val
        self.left=left
        self.right=right

    def getType(self):
        return self.typ

    def setType(self, newtyp):
        self.typ=newtyp

    def getVal(self):
        return self.val

    def setVal(self, newval):
        self.val=newval

    def getLeft(self):
        return self.left

    def setLeft(self, newleft):
        self.left=newleft

    def getRight(self):
        return self.right

    def setRight(self, newright):
        self.right=newright

###Detect incorrect syntax###
class IncorrectSyntax(Exception):
    def __init__(self, msg, tok):
        self.msg=msg
        self.tok=tok


###Functions to construct non-terminals###
def parse_factor(toks):
    if len(toks)==0:
        raise IncorrectSyntax("Expected factor, but input is empty", '')

    tok = toks.pop(0)
    if tok.isspace():       # white space; continue to next token
        return parse_factor(toks)
    elif tok.isalpha():     # identifier
        return Node(typ="id", val=tok)
    elif tok.isdigit():     # number
        while len(toks)>0 and toks[0].isdigit():
            tok = list(tok)         # change token into mutable type
            tok.append(toks.pop(0)) # make token multiple-digit number
        return Node(typ="num", val=str(int(''.join(tok))))   # save token value into a string type
    else:               # invalid character, such as operator
        raise IncorrectSyntax("Expected identifier or number", tok)

def parse_term_prime(toks):
    if len(toks)>0:
        tok = toks[0]       # one lookahead
        if tok.isspace():   # white space; continue to next token
            toks.pop(0)
            tok = toks[0]   # guaranteed that there is next token, because of tokenize function

        if tok=='*' or tok=='/':
            tok = toks.pop(0)
            return Node(typ="op", val=tok, right=parse_term(toks))

def parse_term(toks):
    factor = parse_factor(toks)
    term_prime = parse_term_prime(toks)
    if term_prime == None:
        return factor
    term_prime.setLeft(factor)  # push subtree <factor>
    return term_prime

def parse_expr_prime(toks):
    if len(toks)>0:
        tok = toks[0]       # one lookahead
        if tok.isspace():   # white space; continue to next token
            toks.pop(0)
            tok = toks[0]   # guaranteed that there is next token; refer to 'tokenize' function for reason

        if tok=='+' or tok=='-':
            tok = toks.pop(0)
            return Node(typ="op", val=tok, right=parse_expr(toks))
        else:
            raise IncorrectSyntax("Expected addition/subtraction after term", tok)

def parse_expr(toks):
    term = parse_term(toks)
    expr_prime = parse_expr_prime(toks)
    if expr_prime == None:
        return term
    expr_prime.setLeft(term)  # push subtree <term>
    return expr_prime
##########################################

'''Helper function to replace white space with a single space in input string line
                    & change into mutable data type(list)'''
def tokenize(str_line):
    # there are no white space at both ends, and tokens are seperated by single space
    if len(str_line) >= 3 and str_line[-2:] == '++':
        return [str_line.strip(" ")]
    if check_match(p_function,str_line) and str_line[:6] != "printf":
        return ['#',str_line.split("(")[0],str_line[len(str_line.split("(")[0])+1:-1]]
    if str_line[:7] == "return ":
        return ["return",str_line[7:].strip(" ")]
    if " = " in str_line:
        if str_line.count(" = ") != 1:
            return Error("", "Syntax error : line")
            # return Error("","Error")
        token = str_line.split(" = ")
        token.insert(1,'=')
        return token
    if str_line[:4] == "int ":
        return ["int",[i.strip(" ") for i in str_line[4:].strip(" ").split(",")]]
    if str_line[:6] == "float ":
        return ["float",[i.strip(" ") for i in str_line[6:].strip(" ").split(",")]]
    if str_line[:6] == "printf":
        return ["printf",str_line[7:-1]]
    bracket_stack = 0
    token = []
    for i in range(len(str_line)):
        if bracket_stack == 0 and str_line[i] in ['+','-','/','*','>','<']:
            token.append(str_line[:i].strip())
            token.append(str_line[i])
            token.append(str_line[i+1:].strip())
            return token
        if str_line[i] == '(':
            bracket_stack += 1
        if str_line[i] == ')':
            if bracket_stack == 0:
                return Error("", "Syntax error : line")
                # return Error("","Error")
            bracket_stack -= 1
    return str_line.strip().split()

'''Parse the given input string line'''
def parser(str_line):
    toks = tokenize(str_line)
    if len(toks)==0:
        raise IncorrectSyntax("There is only white space on this line", toks)
    return parse_expr(toks)


'''Helper function to concatenate strings'''
def merge(str1, str2, str3):
    return str1+str2+str3

'''Express the parsed tree in pre_order syntax string'''
def pre_order(root):
    if root == None:
        return ''
    return merge(root.getVal(), pre_order(root.getLeft()), pre_order(root.getRight()))

def main():
    # Read input file
    file_in = open("input.txt", "r")
    file_out = open("output.txt", "w")

    # Iterate lines in file
    for line in file_in:
        try:
            expr_result = pre_order(parser(line))
            file_out.write(expr_result+'\n')
        except IncorrectSyntax as e:
            file_out.write("incorrect syntax" + '\n')

    file_in.close()
    file_out.close()