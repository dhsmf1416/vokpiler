# -*- coding: utf-8 -*-
import re
from structure import *
from interpreter import *
top = 0
global_line_num = 0
currentStack = []
class ForLoop:
    first = None
    third = None
    def __init__(self, first, second, third):
        self.first = first
        self.first.node_next = second
        self.first.line_next = second
        self.third = third
        self.third.node_next = second
        self.third.line_next = Node("empty","")
    def link_last(self, new_node):
        if not self.first.find_last_node().node_next:
            self.first.find_last_node().node_next = new_node
        self.first.find_last_node().line_next = new_node
class IfCondition:
    first = None
    def __init__(self, condition):
        self.first = condition
    def link_last(self, new_node):
        if not self.first.find_last_node().node_next:
            self.first.find_last_node().node_next = new_node
        self.first.find_last_node().line_next = new_node
def parse_for_loop(raw_text):
    three_statements = raw_text.split(';')
    if not len(three_statements) == 3:
        return Error("syntax", "Syntax error : line")
        #return Error("","3")
    first = parse_assignment(three_statements[0])
    second = parse_condition(three_statements[1])
    third = parse_assignment(three_statements[2])
    # first, second, third가 모두 제대로 된 함수여야 함
    if not (type(first) == Node and type(second) == Node and type(third) == Node):
        return Error("syntax", "Syntax error : line")
        # return Error("","Error type 4")
    return ForLoop(first,second,third)

def parse_if_condition(raw_text):
    return IfCondition(parse_condition(raw_text))

p1 = re.compile("[(].*[)]")
def parse_one_line(raw_text):
    ### ERROR 1 CHECK
    last = raw_text[-1]
    raw_text = raw_text[:-1].strip(" ")
    if not last in ["{","}",";"]:
        return Error("syntax", "Syntax error : line")
        # return Error("","1")
    ### general assignment
    if last == ";":
        result = parse_assignment(raw_text)
    if last == "{":
        m = p1.search(raw_text)
        if m.end() != len(raw_text):
            return Error("syntax", "Syntax error : line")
            # return Error("","2")
        my_syms = []
        for sym in raw_text[:m.start()].split(" "):
            if sym:
                my_syms.append(sym)
        if len(my_syms) == 1:
            if my_syms[0] == "for":
                return parse_for_loop(m.group()[1:-1])
            if my_syms[0] == "if":
                return parse_if_condition(m.group()[1:-1])
        if len(my_syms) == 2:
            if my_syms[0] in ["int","float"]:
                if is_valid_name(my_syms[1]):
                    #print("parse_one_line : is_valid_name")
                    param_list = m.group()[1:-1].split(",")
                    #print(param_list)
                    return parse_func_declare(my_syms[0],my_syms[1],param_list)
                else:
                    return Error("syntax", "Syntax error : line")
                    # return Error("","6")
            else:
                return Error("syntax", "Syntax error : line")
                # return Error("","7")
        else:
            return Error("syntax", "Syntax error : line")
            # return Error("","8")

    if last == "}":
        ### 앞에 무언가가 있을 떄 에러처리를 해야 하는가???
        if raw_text:
            return Error("syntax", "Syntax error : line")
            # return Error("","5")
        return None
    return result
def make_error(msg):
    print(msg, global_line_num)


def parse_file(path):
    global top
    f = open(path,"r")
    current_line = 0
    for line in f:
        current_line += 1
        line = line.strip("\t").strip(" ").strip("\n")
        if line:
            result = parse_one_line(line.strip(" ").strip("\n"))
            #print("loop start")
            #print(type(result))
            if type(result) == Function:
                if top != 0:
                    return Error("syntax", "Syntax error : line")
                    # make_error("func declaration should be outest")
                    # return Error("","9")
                result.first.line = current_line
                currentStack.append(result)
                top += 1
            elif type(result) in [ForLoop,IfCondition]:
                if top == 0:
                    return Error("syntax", "Syntax error : line")
                    # make_error("(for or if) should be in func")
                    # return
                currentStack.append(result)
                result.first.line = current_line
                if type(result) == ForLoop:
                    result.third.line = current_line
                top += 1
            if type(result) == Node:
                if top == 0:
                    return Error("syntax", "Syntax error : line")
                    # make_error("statement should be in func")
                    # return
                result.line = current_line
                currentStack[top-1].link_last(result)
            if not result:
                if line.strip("\t").strip(" "):
                    if top == 0:
                        return Error("syntax", "Syntax error : line")
                        # make_error("no function!!!!")
                        # return
                    context = currentStack.pop()
                    top -= 1
                    if type(context) == Function:
                        new_node = Node("line","")
                        new_node.line = current_line
                        context.link_last(new_node)
                        functionList.append(context)
                    elif type(context) == ForLoop:
                        currentStack[top-1].link_last(context.first)
                        context.first.node_next.node_false_next = context.third.line_next
                        context.first.node_next.line = context.first.line
                        context.link_last(context.third)

                        ### add '}' line
                        new_node = Node("line","")
                        new_node.line = current_line
                        context.link_last(new_node)
                    else:
                        currentStack[top-1].link_last(context.first)
                        new_node = Node("line","")
                        new_node.line = current_line
                        context.link_last(new_node)
                        context.first.node_false_next = new_node
            if type(result) == Error:
                return result.msg + " " + str(current_line)

        else:
            if top > 0:
                new_node = Node("line","")
                new_node.line = current_line
                context = currentStack[top-1].link_last(new_node)
    f.close()
    if top != 0:
        return Error("syntax", "Syntax error : line %d" % (current_line))
        # make_error("no match bracket")
        # return
    #print("SUCCESSFULLY FINISH!!")
    # for function in functionList:
    #     print("-------")
    #     asdf = function.first
    #     print(asdf)
    #     while asdf.line_next:
    #         asdf = asdf.line_next
    #         print(asdf)

def get_function(name):
    for function in functionList:
        if function.name == name:
            return function
    return None

def initiate_function(function,node):
    #print("----START INTERPERT (" + function.name+ ")----")
    scope_stack.addScope(node)
    cur_line = function.first
    while cur_line:
        if cur_line.type == "empty":
            cur_line = cur_line.node_next
        break
    return cur_line
def refresh_everything(arith_node):
    if not arith_node:
        return None
    if arith_node.expr == '#':
        arith_node.var = None
        return arith_node
    return find_everything(arith_node.prev) or find_everything(arith_node.next)
def find_everything(arith_node):
    if not arith_node:
        return None
    if arith_node.expr == '#' and not symbol_table.find(arith_node):
        return arith_node
    return find_everything(arith_node.prev) or find_everything(arith_node.next)
def pre_interpreter(line):
    arith_node = find_everything(line.tree)
    while arith_node:
        if arith_node.expr == '#' and not symbol_table.find(arith_node):
              func_name = arith_node.prev.expr
              function = get_function(func_name)
              param_list = arith_node.next.expr
              i = 0
              for param in param_list.split(","):
                 param = param.strip(" ")
                 x = symbol_table.find(param)
                 if x and "*" in x.type:
                    #symbol_table.add(SymbolEntry(x.symbol_name,x.type,x.state_type,x.current_value,x.length,x.trace))
                    cur_type = x.type
                 else:
                    param = eval_ast(parse_cond_arith(param))
                    if type(param) == float:
                        cur_type = 'float'
                    elif type(param) == int:
                        cur_type = 'int'
                    else:
                        return Error("", "Run-time error : line")
                        # return Error("","invalid type")
                 if cur_type != function.param_list[i][0]:
                    if not (cur_type in ['int','float'] and function.param_list[i][0] in ['int','float']):
                        return Error("", "Run-time error : line")
                        # return Error("","invalid type")
                 if "*" in function.param_list[i][0]:
                    symbol_table.add(SymbolEntry(function.param_list[i][1],x.type,x.current_value,x.length,x.trace,scope_stack.getScope()+1))
                 else:
                    symbol_table.add(SymbolEntry(function.param_list[i][1],cur_type,param,None,[[[param,function.first.line]]],scope_stack.getScope()+1))
                 i += 1
              if i != function.num_of_params:
                  return Error("", "Run-time error : line")
                 # return Error("","no match num of params")
              result = iterate_function(function)
              if type(result) == int:
                symbol_table.add(SymbolEntry(arith_node,"int",result,None,[[]],scope_stack.getScope()))
              if type(result) == float:
                symbol_table.add(SymbolEntry(arith_node,"float",result,None,[[]],scope_stack.getScope()))
              if function.return_type == "int":
                 result = int(result)
              if function.return_type == "float":
                 result = float(result)

              #arith_node.expr = str(result)
        arith_node = find_everything(line.tree)
    return line
def interpret_one_line(line):
    aaa =  pre_interpreter(line)
    result = interpreter(line)
    return result
def get_next_line(line):
    line = line.node_next
    while line:
        if not line.line:
            line = line.node_next
        break
    return line
endFlag = False
def iterate_function(function):
    global global_line_num, endFlag
    pasdf = re.compile("next [1-9][0-9]*")
    pgggg = re.compile("print [a-zA-Z_][a-zA-Z_0-9]*")
    pqwer = re.compile("trace [a-zA-Z_][a-zA-Z_0-9]*")
    cur_line = initiate_function(function,None)
    while True:
        if global_line_num > 0:
            global_line_num -= 1
            if endFlag:
                global_line_num = 0
                print("End of Program")
                continue
            if not cur_line:
                endFlag = True
                continue
            result = interpret_one_line(cur_line)
            if type(result) == Error:
                print("Run-time error: line %d" % (cur_line.line))
                # print(result.msg)
                return result
            if result == "empty":
                cur_line += 1
            if type(result) in [int,float]:
                return result
            if result == 'False':
                cur_line = cur_line.node_false_next
            else:
                cur_line = get_next_line(cur_line)
            continue
        key_input = input(">> ")
        if key_input.strip(" ") == "next":
            global_line_num += 1
            continue
        if key_input[0:5] == "next ":
            if check_match(pasdf, key_input.strip(" ")): # next command used with natural number argument
                line_num = int(key_input.strip(" ").split(" ")[1])
                global_line_num += line_num
                continue
            else:
                print("Incorrect command usage : try 'next 5'")
                continue
        if pgggg.match(key_input.strip(" ")):
            print_variable(key_input.strip(" ").split(" ")[1])
            continue
        if pqwer.match(key_input.strip(" ")):
            trace_variable(key_input.strip(" ").split(" ")[1])
            continue
        if key_input.strip(" ") == "exit()":
            break
        print("command should be in (next, trace, print)")

def check_match(p,expr):
    return p.match(expr) and p.match(expr).end() == len(expr)
p_arr = re.compile('[a-zA-Z_][a-zA-Z_0-9]*[[][0-9][0-9]*[]]')
def print_variable(s):
    if check_match(p_arr,s):
        curr_symbol = symbol_table.find(s.split("[")[0])
        curr_index = int(s.split("[")[1][:-1])
        if curr_symbol == None:
            print("Invalid typing of the variable name")
            #print("Symbol is undecleared")
        elif curr_index >= curr_symbol.length:
            print("Invalid typing of the variable name")
            # print("Index is out of range")
        elif curr_symbol.current_value[curr_index] == None:
            print("N/A")
        else:
            print(curr_symbol.current_value[curr_index])
    else:
        curr_symbol = symbol_table.find(s)
        if curr_symbol == None: # not in symbol table
            print("Invisible variable")
            #print("Symbol is undecleared")
        elif curr_symbol.length != None:
            print("Invalid typing of the variable name")
            # print("Please type index")
        elif curr_symbol.current_value == None:
            print("N/A")
        else:
            print(curr_symbol.current_value)

def trace_variable(s):
    if check_match(p_arr,s):
        curr_symbol = symbol_table.find(s.split("[")[0])
        curr_index = int(s.split("[")[1][:-1])
        if curr_symbol == None: # not in symbol table
            print("Invisible variable")
            # print("Symbol is undecleared")
        elif curr_index >= curr_symbol.length:
            print("Invalid typing of the variable name")
            # print("Index is out of range")
        else:
            for i in range(0, len(curr_symbol.trace[curr_index])):
                if curr_symbol.trace[curr_index][i][0] == None:
                    print(s + " =" + "N/A" + " at line " + str(curr_symbol.trace[curr_index][i][1]))
                else:
                    print(s + " =" + str(curr_symbol.trace[curr_index][i][0]) + " at line " + str(curr_symbol.trace[curr_index][i][1]))
    else:
        curr_symbol = symbol_table.find(s)
        if curr_symbol == None: # not in symbol table
            print("Invisible variable")
            # print("Symbol is undecleared")
        elif curr_symbol.length != None:
            print("Invalid typing of the variable name")
            # print("Please type index")
        else:
            for i in range(0, len(curr_symbol.trace[0])):
                if curr_symbol.trace[0][i][0] == None:
                    print(s + " = "  + "N/A" + " at line " + str(curr_symbol.trace[0][i][1]))
                else:
                    print(s + " = "  + str(curr_symbol.trace[0][i][0]) + " at line " + str(curr_symbol.trace[0][i][1]))
def main():
    error = parse_file("input.txt")
    if error:
        print(error)
        return
    main_func = get_function("main")
    if not main_func:
        print("There are no main functions!")
        return
    iterate_function(main_func)


main()