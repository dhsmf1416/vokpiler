import re
from PredictiveParser import tokenize
p2 = re.compile("[a-zA-Z_][a-zA-Z_0-9]*")
p_function = re.compile("[a-zA-Z_0-9]*[(].*[)]")
definitions = ["int","float","for","if","return","printf"]
functionList = []
def check_match(p,expr):
    return p.match(expr) and p.match(expr).end() == len(expr)
class SymbolEntry(object):
    def __init__(self, symbol_name, state_type, current_value, length, trace,scope):
        self.symbol_name = symbol_name
        self.type = state_type
        self.current_value = current_value
        self.length = length
        self.trace = trace
        self.scope = scope
        self.node_next = None
class SymbolTable(object):
    def __init__(self):
        self.first = SymbolEntry(None, None, None, None,[],1)
        self.last = self.first
    def del_scope_var(self, scope):
        prev_node = self.first
        curr_node = self.first.node_next
        while curr_node:
            if curr_node.scope == scope:
                if self.last == curr_node:
                    self.last = prev_node
                prev_node.node_next = curr_node.node_next
                curr_node = prev_node.node_next
            else:
                prev_node = curr_node
                curr_node = prev_node.node_next
    def add(self, x):
        self.last.node_next = x
        self.last = x
        x = self.first
        while x.node_next:
            x = x.node_next
    def __str__(self):
        curr_node = self.first.node_next
        print_str = ""
        while curr_node:
            if curr_node.symbol_name:
                symbol_name = curr_node.symbol_name
            else:
                symbol_name = "@"
            if curr_node.type:
                symbol_type = curr_node.type
            else:
                symbol_type = "@"
            if curr_node.current_value == 0 or curr_node.current_value:
                current_value = curr_node.current_value
            else:
                current_value = "@"
            if curr_node.length:
                length = curr_node.length
            else:
                length = "@"

            print_str += str(symbol_name) + " " + str(symbol_type) + " " + str(current_value) + " " + str(length) + " " + str(curr_node.scope)+ "\n"
            curr_node = curr_node.node_next
        return print_str
    def find(self, name):
        iter_curr = self.first
        while iter_curr != None:
            if iter_curr.symbol_name == name and iter_curr.scope == scope_stack.getScope():
                return iter_curr
            else:
                iter_curr = iter_curr.node_next
        return None
        # print("Run-time error : line %d" % (global_line_num))
        # print("Error: in class SymbolTable, def modify : no such symbol")

    def delete_one(self, name):
        iter_curr = self.first.node_next
        prev_curr = self.first
        while iter_curr != None:
            if iter_curr.symbol_name == name and iter_curr.scope == scope_stack.getScope():
                if self.last == iter_curr:
                    self.last = prev_curr
                prev_curr.node_next = iter_curr.node_next
                return None
            else:
                prev_curr = iter_curr
                iter_curr = iter_curr.node_next
        return None
        # print("Error: in class SymbolTable, def modify : no such symbol")
    def modify(self, name, value, line):
        if name[-1] == "]":
            curr_symbol = self.find(name[:-4])
            curr_index = int(name[-2])
            curr_symbol.current_value = value
            curr_symbol.trace[curr_index].append([value, line])
        else:
            curr_symbol = self.find(name)
            curr_symbol.current_value = value
            curr_symbol.trace[0].append([value, line])
def is_valid_name(name):
    if name in definitions:
        return False
    m = p2.match(name)
    if m and m.end() == len(name):
        return True
    return False

class ScopeStack(object):
    def __init__(self):
        self.stack = []
        self.curr_index = 0
    def getScope(self):
        return self.curr_index
    def addScope(self, caller_node):
        self.stack.append((caller_node, self.curr_index))
        self.curr_index += 1
    def delScope(self):
        return_node, return_index = self.stack.pop()
        self.curr_index = return_index
        return return_node
scope_stack = ScopeStack()
class Error:
    msg = None
    typ = None
    def __init__(self, typ, msg):
        self.msg = msg
        self.typ = typ
    def __str__(self):
        return self.msg
idx = 0
class Node(object):
    line = 0
    def __init__(self, state_type, token):
        global idx
        self.type = state_type
        self.token = token
        self.node_next = None
        self.node_false_next = None
        self.line_next = None
        self.tree = None
        idx += 1
        self.idx = idx
    def __str__(self):
        if self.node_next:
            none = self.node_next.idx
        else:
            none = -1
        if self.line_next:
            line = self.line_next.idx
        else:
            line = -1
        if self.node_false_next:
            nfn = self.node_false_next.idx
        else:
            nfn = -1
        return "LINE " + str(self.line) + "," + str(self.idx)+ " : " + str(none) + "," + str(line) + "," + str(nfn) + " : "+ str(self.token)
    def find_last_node(self):
        if not self.line_next:
            return self
        return self.line_next.find_last_node()

class ArithNode(object):
    def __init__(self, expr):
        self.expr = expr
        self.var = None
        self.prev = None
        self.next = None
    def __str__(self):
        return self.expr
class LinkedList(object):
  def __init__(self):
    self.first = Node("empty",None)
    self.last = None
    self.count = 0

  def add_first(self, x):
    x.node_next = self.first
    self.first = x

  def add_last(self, x):
    self.last.node_next = x
    self.last = x

  def add_next(self, x, y):
    if y == self.last:
      add_last(x)
    else:
      x.node_next = y.node_next
      y.node_next = x

class Function(object):
    name = None
    return_type = None
    num_of_params = None
    param_list = None
    linkedList = None
    first = None
    def __init__(self, return_type, func_name, param_list):
        self.return_type = return_type
        self.name = func_name
        self.param_list = param_list
        self.num_of_params = len(param_list)
        self.linkedList = LinkedList()
        self.first = Node("empty","")
    def link_last(self, new_node):
        if not self.first.find_last_node().node_next:
            self.first.find_last_node().node_next = new_node
        self.first.find_last_node().line_next = new_node
def parse_condition(s): # return type: Node
    toks = tokenize(s)
    ast = Node(toks[1], toks)
    ast.tree = parse_cond_arith(s)
    return ast
def parse_cond_arith(s): # return type: ArithNode
    toks = tokenize(s)
    if toks[0] == '#':
        parent = ArithNode(toks[0])
        left = ArithNode(toks[1])
        right = ArithNode(toks[2])
        parent.prev = left
        parent.next = right
        return parent
    if len(toks) == 1:
        return parse_statement(toks[0])
    parent = ArithNode(toks[1])
    left = parse_statement(toks[0])
    right = parse_statement(toks[2])
    parent.prev = left
    parent.next = right
    return parent
def parse_equal(s):
    toks = tokenize(s)
    ast = Node(toks[1], toks)
    ast.tree = ArithNode(toks[1])
    _left = parse_statement(toks[0])
    _right = parse_statement(' '.join(toks[2:]))
    if Error == type(_left):
        return _left
    if Error == type(_right):
        return _right
    ast.tree.prev = _left
    ast.tree.next = _right
    return ast

def parse_func_declare(return_type, func_name, param_list):
    if not return_type in ["int","float"]:
        return Error("", "Syntax error : line")
        # return Error("","invalid return type")
    if not is_valid_name(func_name):
        return Error("", "Syntax error : line")
        # return Error("","invalid function name")
    for func in functionList:
        if func.name == func_name:
            return Error("", "Syntax error : line")
            # return Error("","duplicate function name")
    p3 = re.compile('(int|float) [a-zA-Z_][a-zA-Z_0-9]*')
    p4 = re.compile('(int|float) [*][a-zA-Z_][a-zA-Z_0-9]*')
    p5 = re.compile('(int|float)[*] [a-zA-Z_][a-zA-Z_0-9]*')
    p6 = re.compile('void')
    final_params = []
    for param in param_list:
        param = param.strip(" ")
        m = p3.match(param)
        if m and m.end() == len(param) and is_valid_name(param.split(" ")[1]):
            final_params.append([param.split(" ")[0],param.split(" ")[1]])
            continue
        m = p4.match(param)
        if m and m.end() == len(param) and is_valid_name(param.split(" *")[1]):
            final_params.append([param.split(" *")[0]+"*",param.split(" *")[1]])
            continue
        m = p5.match(param)
        if m and m.end() == len(param) and is_valid_name(param.split("* ")[1]):
            final_params.append([param.split("* ")[0]+"*",param.split("* ")[1]])
            continue
        m = p6.match(param)
        if m and m.end() == len(param):
            continue
        return Error("", "Syntax error : line")
        # return Error("","invalid params")
    return Function(return_type, func_name, final_params)

def parse_statement(s): # return type : ArithNode
    s.strip()
    if s[0] == "(" and s[-1] == ")":
        s = s.lstrip("(").rstrip(")")
    if any(op in s for op in ['+','-','<','>','*','/']):
            x = parse_cond_arith(s)
            if type(x) != Error:
                return x
    s.strip()
    ### Bracket elimination
    if any(br in s for br in ["(", ")"]):
        if check_match(p_function,s):
            func_name = s.split("(")[0]
            param_list = s[len(func_name)+1:-1]
            x = ArithNode("#")
            x.prev = ArithNode(func_name)
            x.next = ArithNode(param_list)
            return x
        return Error("", "Syntax error : line")
        # return Error("", "bracket mismatch")

    # else: function or variable

    return ArithNode(s)


def parse_assignment(s):
    token = tokenize(s)
    node = Node(None, token)
    if token[0] == "int":
        node.type = "int"
        return parse_int(node, token)
    elif token[0] == "float":
        node.type = "float"
        return parse_float(node, token)
    elif len(token) == 1:
        node.type = "="
        return parse_plusplus(node, token)
    elif token[0] == "return":
        if len(token)!=2:
            return Error("", "Syntax error : line")
            # return Error("", "return type has too many or less arguments")
        node.type = "return"
        node.tree = parse_statement(token[1])
        return node
    elif token[0] == "printf":
        node.type = "print"
        return node
    else:
        node.type = "="
        return parse_equal(s)
    # return None
def parse_plusplus(n, token):
    if len(token) != 1 or not "++" in token[0] or not token[0][-2:] == "++":
        return Error("", "Syntax error : line")
        # return "syntax error"
    var = token[0][:-2]
    toks = [var,"=",var,"+","1"]
    n.tree = ArithNode(toks[1])
    n.tree.prev = parse_statement(toks[0])
    n.tree.next = parse_statement(' '.join(toks[2:]))
    return n
p3 = re.compile("[a-zA-Z_][a-zA-Z_0-9]*[[][1-9][0-9]*[]]")
def parse_int(n, token):
    array_flag = False
    not_array_flag = False
    new_token = [token[0],[]]
    for t in token[1]:
        if p3.match(t):
            n.type = "int*"
            array_flag = True
            nums = t.split("[")[1][:-1]
            try:
                new_token[1].append([t.split("[")[0],int(nums)])
            except ValueError:
                return Error("", "Syntax error : line")
                # return Error("","Error: parse_int: invalid length")
        elif p2.match(t):
            n.type = "int"
            not_array_flag = True
            new_token[1].append(t)
        else:
            return Error("", "Syntax error : line")
            # return Error("","Error: parse_int: invalid variable name")
    if array_flag and not_array_flag:
        return Error("", "Syntax error : line")
        # return Error("","Error: parse_int: invalid params")
    n.token = new_token
    return n
def parse_float(n, token):
    array_flag = False
    not_array_flag = False
    new_token = [token[0]]
    for t in token[1]:
        if p3.match(t):
            n.type = "float*"
            array_flag = True
            nums = t.split("[")[1][:-1]
            try:
                new_token.append([t.split("[")[0],int(nums)])
            except ValueError:
                return Error("", "Syntax error : line")
                # return "Error: parse_float: invalid length"
        elif p2.match(t):
            n.type = "float"
            not_array_flag = True
            new_token.append([t])
        else:
            return Error("", "Syntax error : line")
            # return "Error: parse_float: invalid variable name"
    if array_flag and not_array_flag:
        return Error("", "Syntax error : line")
        # return "Error: parse_float: invalid params"
    n.token = new_token
    return n