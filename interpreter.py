''' interpret.py '''
import re
import sys
from structure import *

symbol_table = SymbolTable()
p_int = re.compile("[0-9][0-9]*")
p_float = re.compile("^[-+]?[0-9]+\.[0-9]+$")
p_var = re.compile("[a-zA-Z_][a-zA-Z_0-9]*")
p_array = re.compile("[a-zA-Z_][a-zA-Z_0-9]*[[].*[]]")
p_function = re.compile("[a-zA-Z_][a-zA-Z_0-9]*[(].*[)]")
definitions = ["int","float","for","if","return","printf"]


def inter_int(n):
   arg_len = len(n.token[1])
   for i in range(0, arg_len):
      if symbol_table.find(n.token[1][i]) or n.token[1][i] in (definitions + [function.name for function in functionList]):
        return Error("", "Run-time error : line")
      curr_node = SymbolEntry(n.token[1][i], "int", None, None, [[]],scope_stack.getScope())
      symbol_table.add(curr_node)
      curr_node.trace[0].append([None, n.line])

def inter_float(n):
   arg_len = len(n.token[1])
   for i in range(0, arg_len):
      if symbol_table.find(n.token[1][i]) or n.token[1][i] in (definitions + [function.name for function in functionList]):
        return Error("", "Run-time error : line")
      curr_node = SymbolEntry(n.token[1][i], "float", None, None, [[]],scope_stack.getScope())
      symbol_table.add(curr_node)
      curr_node.trace[0].append([None, n.line])

def inter_int_star(n):
   arg_len = len(n.token[1])
   for i in range(0, arg_len):
      if symbol_table.find(n.token[1][i][0]) or n.token[1][i] in (definitions + [function.name for function in functionList]):
            return Error("", "Run-time error : line")
      array_len = n.token[1][i][1]
      curr_node = SymbolEntry(n.token[1][i][0], "int*", [None] * array_len, array_len, [[] for i in range(array_len)],scope_stack.getScope())
      symbol_table.add(curr_node)
      for j in range(0, array_len):
         curr_node.trace[j].append([None, n.line])

def inter_float_star(n):
   arg_len = len(n.token[1])
   for i in range(0, arg_len):
      if symbol_table.find(n.token[1][i][0]) or n.token[1][i] in (definitions + [function.name for function in functionList]):
            return Error("", "Run-time error : line")
      array_len = n.token[1][i][1]
      curr_node = SymbolEntry(n.token[1][i][0], "float*", [None] * array_len, array_len, [[] for i in range(array_len)],scope_stack.getScope())
      symbol_table.add(curr_node)
      for j in range(0, array_len):
         curr_node.trace[j].append([None, n.line])


def check_match(p, expr):
    return p.match(expr) and p.match(expr).end() == len(expr)


def inter_assign(arith_node, line):
    if arith_node.expr != "=":
        return Error("", "Run-time error : line")
        # return Error("", "assignment interpretation error")
    lhs = arith_node.prev.expr
    if arith_node.next.expr != '#':
        rhs = eval_ast(arith_node.next)
    else:
        rhs = arith_node.next
        rhs = symbol_table.find(rhs).current_value
        x = symbol_table.delete_one(arith_node.next)
    global p_var, p_int, p_float, p_array
    # Case #1: variable
    if check_match(p_var, lhs):
        entry = symbol_table.find(lhs)
        if not entry:
            return Error("", "Run-time error : line")

        if (entry.type == "int" and type(rhs) == int) or (entry.type == "float" and type(rhs) == float):
            entry.current_value = rhs
            entry.trace[0].append((rhs, line))
        else:
            return Error("", "Run-time error : line")
            # return Error("", "variable type mismatch")

    # Case #2: array element
    elif check_match(p_array, lhs):
        # Array info
        comp = lhs.split("[")
        array_name = comp[0]
        array_index = comp[1].strip("]")
        try:
            array_index = int(array_index)
        except ValueError:
            index_entry = symbol_table.find(array_index)
            if not index_entry:
                return Error("", "Run-time error : line")
                # return Error("", "Error: in class SymbolTable, def modify : no such symbol")
            array_index = index_entry.current_value
        entry = symbol_table.find(array_name)
        if not entry:
            return Error("", "Run-time error : line")
        if (entry.type == "int*" and type(rhs) == int) or (entry.tpe == "float*" and type(rhs) == float):
            if index_entry.current_value in range(entry.length):
                entry.current_value[index_entry.current_value] = rhs
            else:
                return Error("", "Run-time error : line")
                # return Error("", "array index error!")
            entry.trace[array_index].append((rhs, line))
        else:
            return Error("", "Run-time error : line")
            # return Error("", "array element type mismatch")
    else:
        return Error("", "Run-time error : line")
        # return Error("", "assignment error")


### Helper function for inter_assign
def eval_ast(arith_node):
    '''Evaluate AST'''
    '''For example, 7 = 3+4'''
    op = arith_node.expr
    global p_int, p_float, p_var, p_array

    if op == '#':
        rhs = arith_node
        rhs = symbol_table.find(rhs).current_value
        x = symbol_table.delete_one(arith_node)
        return rhs
    if op == '+':
        return eval_ast(arith_node.prev) + eval_ast(arith_node.next)
    elif op == '-':
        return eval_ast(arith_node.prev) - eval_ast(arith_node.next)
    elif op == '*':
        return eval_ast(arith_node.prev) * eval_ast(arith_node.next)
    elif op == '/':
        return eval_ast(arith_node.prev) / eval_ast(arith_node.next)
    elif check_match(p_int, op):    # leaf node, int
        return int(op)
    elif check_match(p_float, op):  # leaf node, float
        return float(op)
    elif check_match(p_var, op):    # leaf node, symbol
        entry = symbol_table.find(op)
        if entry:
            return entry.current_value
        else:
            return Error("", "Run-time error : line")
            # return Error("", "invalid symbol")
    elif check_match(p_array, op):  # leaf node, array element
        entry = symbol_table.find(op.split("[")[0])
        if entry:
            try:
                index = op.split("[")[1].strip("]")
                index = int(index)
            except ValueError:
                index_entry = symbol_table.find(index)
                if not index_entry:
                    return Error("", "Run-time error : line")
                    # return Error("", "Error: in class SymbolTable, def modify : no such symbol")
                index = index_entry.current_value
            return entry.current_value[index]
        else:
            return Error("", "Run-time error : line")
            # return Error("", "invalid symbol")
    else:
        return Error("", "Run-time error : line")
        # return Error("", "invalid expression in arithmetic ast")

pp1 = re.compile("[(].*[)]")
pp2 = re.compile("[\"].*[\"]")


def inter_print(s):
    s = [a.strip(" ") for a in s.split(",")]
    if len(s) == 0:
        return Error("", "Run-time error : line")
        # return Error("", "no argument")
    if len(s) == 1:
        if not (s[0][0] == '"' and s[0][-1] == '"' and len(s[0]) >= 2):
            return Error("", "Run-time error : line")
        print(s[0][1:-1])
        return "1"
            # return Error("", "invalid argument")
        ### PRINT!
    if len(s) == 2:
        if s[0] == '"%d\\n"':
            if check_match(p_array, s[1]):
                sym_name = s[1].split("[")[0]
                sym_var = s[1].split("[")[1][:-1]
                sym = symbol_table.find(sym_name)
                if not sym:
                    return Error("", "Run-time error : line")
                    # return Error("", sym_name + " is not defined")
                if not sym.length or (sym.length and sym.length <= int(sym_var)):
                    return Error("", "Run-time error : line")
                    # return Error("", "index error")
                print(int(sym.current_value[int(sym_var)]))
                return "1"
            else:
                sym = symbol_table.find(s[1])
                if not sym:
                    return Error("", "Run-time error : line")
                    # return Error("", sym + " is not defined")
                if sym.type in ["int", "float"]:
                    print(int(sym.current_value))
                    return "1"
                else:
                    return Error("", "Run-time error : line")
                    # return Error("", "type error")
        if s[0] == '"%f\\n"':
            if check_match(p_array, s[1]):
                sym_name = s[1].split("[")[0]
                sym_var = s[1].split("[")[1][:-1]
                sym = symbol_table.find(sym_name)
                if not sym:
                    return Error("", "Run-time error : line")
                    # return Error("", sym_name + " is not defined")
                if not sym.length or (sym.length and sym.length <= int(sym_var)):
                    return Error("", "Run-time error : line")
                    # return Error("", "index error")
                print(float(sym.current_value[int(sym_var)]))
                return "1"
            else:
                sym = symbol_table.find(s[1])
                if not sym:
                    return Error("", "Run-time error : line")
                    # return Error("", sym + " is not defined")
                if sym.type in ["int", "float"]:
                    print(float(sym.current_value))
                    return "1"
                else:
                    return Error("", "Run-time error : line")
                    # return Error("", "type error")
    return Error("", "Run-time error : line")
    # return Error("", "not supported this version")


def inter_return(arith_node):
    return_val = eval_ast(arith_node)
    symbol_table.del_scope_var(scope_stack.getScope())
    scope_stack.delScope()
    return return_val


def inter_cond(arith_node):
    if arith_node.expr not in [">", "<", ">=", "<=", "==", "!="]:
        return Error("", "Run-time error : line")
        # return Error("", "condition interpretation error")

    op = arith_node.expr
    lhs = eval_ast(arith_node.prev)
    rhs = eval_ast(arith_node.next)
    global p_var, p_int, p_float, p_array
    # Case #1: int, float
    if type(lhs) in [int, float] and type(rhs) in [int, float]:
        return str(eval_cond(lhs, op, rhs))

    else:
        return Error("", "Run-time error : line")
        # return Error("", "variable type mismatch")


### Helper function of inter_cond
def eval_cond(lhs, op, rhs):
    if op == ">":
        return lhs > rhs
    elif op == "<":
        return lhs < rhs
    elif op == ">=":
        return lhs >= rhs
    elif op == "<=":
        return lhs <= rhs
    elif op == "==":
        return lhs == rhs
    elif op == "!=":
        return lhs != rhs


def interpreter(node):
    if node.type == "int":
        return inter_int(node)
    elif node.type == "float":
        return inter_float(node)
    elif node.type == "int*":
        return inter_int_star(node)
    elif node.type == "float*":
        return inter_float_star(node)
    elif node.type == "print":
        return inter_print(node.token[1])
    elif node.type == '=':
        return inter_assign(node.tree, node.line)
    elif node.type in [">", "<", ">=", "<=", "==", "!="]:
        return inter_cond(node.tree)
    elif node.type == "return":
        return inter_return(node.tree)
    else:
        return "}"