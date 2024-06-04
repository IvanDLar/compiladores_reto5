import ply.lex as lex
import ply.yacc as yacc
from math import pi, pow
import networkx as nx
import matplotlib.pyplot as plt
import functions
import os


# Import custom libraries
from libary import gen_vector, load_image, search_cv2, show_image

class GraphLexer(object):
    tokens = (
        'NUMBER', 'VARIABLE', 'PLUS', 'MINUS', 'TIMES', 'DIV', 'EQUAL', 'EXP',
        'LPAREN', 'RPAREN', 'COMMA', 'CONNECT', "STRING", 'NONE',"GREATER", "LESS", "GREATER_EQUAL", "LESS_EQUAL", "EQUAL_EQUAL", 
        "NOT_EQUAL","OPEN_CURLY","CLOSE_CURLY","IF","ELSE",
         'LBRACK', 'RBRACK'
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIV = r'/'
    t_EQUAL = r'='
    t_EXP = r'\^'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COMMA = r','
    t_CONNECT = r'->'
    t_LBRACK = r'\['
    t_RBRACK = r'\]'

    # For conditionals
    t_GREATER = r'>'
    t_LESS = r'<'
    t_GREATER_EQUAL = r'>='
    t_LESS_EQUAL = r'<='
    t_EQUAL_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_OPEN_CURLY = r'{'
    t_CLOSE_CURLY = r'}'

    def t_IF(self, t):
        r'if'
        return t
    
    def t_ELSE(self, t):
        r'else'
        return t

    def t_NONE(self, t):
        r'None'
        t.value = None
        return t

    def t_NUMBER(self, t):
        r'\d+\.?\d*'
        t.value = int(t.value) if '.' not in t.value else float(t.value)
        return t

    def t_STRING(self, t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t
    
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

class GraphParser(object):
    tokens = GraphLexer.tokens

    def __init__(self):
        self.command_queue = []
        self.lexer = GraphLexer()
        self.parseGraph = None
        self.NODE_COUNTER = 0
        self.symbol_table = {
            "pi": pi,
            "e": 2.718281828459045,
            "myPrint": print,
            "do_nothing": lambda: print("Doing nothing"),
            "sumAB": lambda a, b: a + b,
            "load": load_image,
            "show": show_image,
            "gen_vector": lambda *args: gen_vector(*args),
            "PI": pi,
            "E": 2.718281828459045,
            "execute_file": self.execute_file
, 
        }
        self.parser = yacc.yacc(module=self)

    def execute_file(self, file_path):
        commands = functions.get_file_lines(file_path)
        for command in commands:
            self.command_queue.append(command)

    def add_node(self, attr):
        attr.setdefault("value", "")  # Ensure that 'value' key is always present
        attr["counter"] = self.NODE_COUNTER
        self.parseGraph.add_node(self.NODE_COUNTER, **attr)
        self.NODE_COUNTER += 1
        return self.parseGraph.nodes[self.NODE_COUNTER-1]

    def execute_parse_tree(self, tree):
        root_id = 0
        result = self.visit_node(tree, root_id, -1)
        return result
    
    def compare(self, a, b, op):
        if op == ">":
            return a > b
        if op == "<":
            return a < b
        if op == ">=":
            return a >= b
        if op == "<=":
            return a <= b
        if op == "==":
            return a == b
        if op == "!=":
            return a != b
        
    def resolve_conditional(self, condition, true_branch, false_branch):
        # First check the condition to see if it is true
        print(f"Condition: {condition}")
        print(f"True branch: {true_branch}")
        print(f"False branch: {false_branch}")
        if condition:
            return true_branch
        else:
            if false_branch is None:
                return None
            return false_branch

    def visit_node(self, tree, node_id, from_id):
        children = list(tree.neighbors(node_id))
        res = [self.visit_node(tree, c, node_id) for c in children if c != from_id]
        current_node = tree.nodes[node_id]

        node_type = current_node["type"]
        node_value = current_node["value"]

        if node_type == "INITIAL":
            return res[0]
        if node_type == "ASSIGN":
            self.symbol_table[res[0]] = res[1]
            return res[1]
        if node_type == "NUMBER" or node_type == "STRING" or node_type == "NONE" or node_type == "LIST":
            return node_value
        if node_type == "PENDING_NODE":
            return res[0]
        if node_type == "VARIABLE_ASSIGN":
            return node_value
        if node_type == "VARIABLE":
            return self.symbol_table.get(node_value, 0)
        if node_type in {"FUNCTION_CALL", "FLOW_FUNCTION_CALL"}:
            print(f"Function call: {node_value}")
            func = self.symbol_table.get(node_value, search_cv2(node_value))
            if func is not None:
                return func(*res) if res else func()
            else:
                print(f"Error: Undefined function '{node_value}'")
                return None
        if node_type == "INDEX":
            return res[0][res[1]]["value"]
                # array[0]
        if node_type == "INDEX_ASSIGN":
            var_name = current_node["variable"]
            index = res[1]
            value = res[2]
            if var_name in self.symbol_table and isinstance(self.symbol_table[var_name], list):
                self.symbol_table[var_name][index]["value"] = value
                return self.symbol_table[var_name]
            else:
                raise TypeError(f"Index assignment not supported for {type(self.symbol_table.get(var_name))}")
        # Check for None value before performing operation
        if None in res:
                raise TypeError(f"unsupported operand type(s) on 'NoneType' for {node_type} operation")
        if node_type == "POWER":
            return pow(res[0], res[1])
        if node_type == "PLUS":
            return res[0] + res[1]
        if node_type == "MINUS":
            return res[0] - res[1]
        if node_type == "TIMES":
            return res[0] * res[1]
        if node_type == "DIV":
            return res[0] / res[1]
        if node_type == "GROUP":
            return res[0]
        if node_type == "COMPARISON":
            return self.compare(res[0], res[1], current_node["label"])
        if node_type == "CONDITIONAL":
            second_branch = None
            if len(res) > 2:
                second_branch = res[2]
            return self.resolve_conditional(res[0], res[1], second_branch)
        
    def p_statements_statement(self,p):
        'statements : statement'
        p[0] = p[1]
        
    # Statement options
    def p_statement_assignment(self,p):
        'statement : assignment'
        p[0] = p[1]

    def p_statement_conditional(self,p):
        'statement : conditional'
        p[0] = p[1]
        
    def p_statement_expression(self,p):
        'statement : expression'
        p[0] = p[1]
        
    def p_conditional(self, p):
        """conditional : IF LPAREN comparison RPAREN OPEN_CURLY statements CLOSE_CURLY"""
        node = self.add_node({"type": "CONDITIONAL", "label": "IF", "value": ''})
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        self.parseGraph.add_edge(node["counter"], p[6]["counter"])
        p[0] = node
    def p_conditional_else(self, p):
        """conditional : IF LPAREN comparison RPAREN OPEN_CURLY statements CLOSE_CURLY ELSE OPEN_CURLY statements CLOSE_CURLY"""
        node = self.add_node({"type": "CONDITIONAL", "label": "IF", "value": ''})
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        self.parseGraph.add_edge(node["counter"], p[6]["counter"])
        self.parseGraph.add_edge(node["counter"], p[10]["counter"])
        p[0] = node
        


    def p_index_assignment_assign(self, p):
        """assignment : VARIABLE LBRACK expression RBRACK EQUAL expression"""
        node = self.add_node({"type": "INDEX_ASSIGN", "label": '=', "variable": p[1], "value": ''})
        node_var = self.add_node({"type": "VARIABLE", "label": f'VAR_{p[1]}', "value": p[1]})
        self.parseGraph.add_edge(node["counter"], node_var["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        self.parseGraph.add_edge(node["counter"], p[6]["counter"])
        p[0] = node

    def p_assignment_assign(self, p):
        """assignment : VARIABLE EQUAL expression"""
        node = self.add_node({"type": "ASSIGN", "label": '=', "value": ''})
        node_var = self.add_node({"type": "VARIABLE_ASSIGN", "label": f'VAR_{p[1]}', "value": p[1]})
        self.parseGraph.add_edge(node["counter"], node_var["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_assignment_flow(self, p):
        """assignment : VARIABLE EQUAL flow"""
        node = self.add_node({"type": "ASSIGN", "label": '=', "value": ''})
        node_var = self.add_node({"type": "VARIABLE_ASSIGN", "label": f'VAR_{p[1]}', "value": p[1]})
        self.parseGraph.add_edge(node["counter"], node_var["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node
    


    def p_expression_comparison(self, p):
        """comparison : expression GREATER expression
                      | expression LESS expression
                      | expression GREATER_EQUAL expression
                      | expression LESS_EQUAL expression
                      | expression EQUAL_EQUAL expression
                      | expression NOT_EQUAL expression"""
        node = self.add_node({"type": "COMPARISON", "label": p[2], "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node
            

    def p_flow(self, p):
        """flow : VARIABLE CONNECT flow_functions"""
        connections = list(self.parseGraph.neighbors(p[3][0]["counter"]))
        for c in connections:
            c_node = self.parseGraph.nodes[c]
            if c_node["type"] == "PENDING_NODE":
                c_node["type"] = "VARIABLE"
                c_node["label"] = f"VAR_{p[1]}"
                c_node["value"] = p[1]
                break
        p[0] = p[3][-1]

    def p_flow_functions(self, p):
        """flow_functions : flow_function_call CONNECT flow_functions"""
        connections = list(self.parseGraph.neighbors(p[3][0]["counter"]))
        for c in connections:
            c_node = self.parseGraph.nodes[c]
            if c_node["type"] == "PENDING_NODE":
                self.parseGraph.add_edge(c_node["counter"], p[1]["counter"])
                break
        p[0] = [p[1]] + p[3]

    def p_flow_functions_alone(self, p):
        """flow_functions : flow_function_call"""
        p[0] = [p[1]]

    def p_flow_function_call(self, p):
        """flow_function_call : VARIABLE LPAREN params RPAREN"""
        node = self.add_node({"type": "FLOW_FUNCTION_CALL", "label": f"ff_{p[1]}", "value": p[1]})
        pending_node = self.add_node({"type": "PENDING_NODE", "label": "pending", "value": ""})
        self.parseGraph.add_edge(node["counter"], pending_node["counter"])
        for n in p[3]:
            self.parseGraph.add_edge(node["counter"], n["counter"])
        p[0] = node

    def p_expression_plus(self, p):
        """expression : expression PLUS term"""
        node = self.add_node({"type": "PLUS", "label": '+', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_expression_minus(self, p):
        """expression : expression MINUS term"""
        node = self.add_node({"type": "MINUS", "label": '-', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_expression_term(self, p):
        """expression : term 
                      | string"""
        p[0] = p[1]

    def p_string_def(self, p):
        """string : STRING"""
        p[0] = self.add_node({"type": "STRING", "label": f'STR_{p[1]}', "value": p[1]})

    def p_none_def(self, p):
        """expression : NONE"""
        p[0] = self.add_node({"type": "NONE", "label": 'none', "value": p[1]})

    def p_term_exponent(self, p):
        """term : exponent"""
        p[0] = p[1]

    def p_term_times(self, p):
        """term : term TIMES exponent"""
        node = self.add_node({"type": "TIMES", "label": '*', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_term_div(self, p):
        """term : term DIV exponent"""
        node = self.add_node({"type": "DIV", "label": '/', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_exponent_factor(self, p):
        """exponent : factor"""
        p[0] = p[1]

    def p_exponent_exp(self, p):
        """exponent : factor EXP factor"""
        node = self.add_node({"type": "POWER", "label": 'POW', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[1]["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_factor_number(self, p):
        """factor : NUMBER"""
        p[0] = self.add_node({"type": "NUMBER", "label": f'NUM_{p[1]}', "value": p[1]})

    def p_factor_variable(self, p):
        """factor : VARIABLE"""
        p[0] = self.add_node({"type": "VARIABLE", "label": f'VAR_{p[1]}', "value": p[1]})

    def p_factor_expression(self, p):
        """factor : LPAREN expression RPAREN"""
        node = self.add_node({"type": "GROUP", "label": '( )', "value": ''})
        self.parseGraph.add_edge(node["counter"], p[2]["counter"])
        p[0] = node

    # List implementation methods
    def p_factor_list(self, p):
        """factor : list
                  | list_empty """
        p[0] = p[1]

    def p_list_empty(self, p):
        """list_empty : LBRACK RBRACK"""
        node = self.add_node({"type": "LIST", "label": 'LIST', "value": ""})
        p[0] = node

    def p_list(self, p):
        """list : LBRACK list_elements RBRACK"""
        node = self.add_node({"type": "LIST", "label": 'LIST', "value": p[2]})
        for n in p[2]:
            self.parseGraph.add_edge(node["counter"], n["counter"])
        p[0] = node

    def p_list_elements(self, p):
        """list_elements : list_elements COMMA expression
                         | expression"""
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_expression_index(self, p):
        """index : VARIABLE LBRACK expression RBRACK"""
        node = self.add_node({"type": "INDEX", "label": 'INDEX', "value": ''})
        node_var = self.add_node({"type": "VARIABLE", "label": f'VAR_{p[1]}', "value": p[1]})
        self.parseGraph.add_edge(node["counter"], node_var["counter"])
        self.parseGraph.add_edge(node["counter"], p[3]["counter"])
        p[0] = node

    def p_factor_function_call(self, p):
        """factor : function_call"""
        p[0] = p[1]

    def p_statement_index(self,p):
        'factor : index'
        p[0] = p[1]
        
    def p_function_call_no_params(self, p):
        """function_call : VARIABLE LPAREN RPAREN"""
        p[0] = self.add_node({"type": "FUNCTION_CALL", "label": f'FUNC_{p[1]}', "value": p[1]})

    def p_function_call_params(self, p):
        """function_call : VARIABLE LPAREN params RPAREN"""
        node = self.add_node({'type': 'FUNCTION_CALL', 'label': f'FUN_{p[1]}', 'value': p[1]})
        for n in p[3]:
            self.parseGraph.add_edge(node["counter"], n["counter"])
        p[0] = node

    def p_params(self, p):
        """params : params COMMA expression 
                  | expression"""
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_error(self, p):
        print(f"Syntax error at '{p.value}'")

    def interactive_main(self):
        while True:
            if len(self.command_queue) < 1:
                new_data = input(">")
                self.command_queue.append(new_data)
            data = self.command_queue.pop(0)
            if data == 'exit':
                break
            if data == 'st':
                print(self.symbol_table)
                continue
            self.parseGraph = nx.Graph()
            self.NODE_COUNTER = 0
            root = self.add_node({"type": "INITIAL", "label": "INIT"})
            result = self.parser.parse(data)
            if result:
                self.parseGraph.add_edge(root["counter"], result["counter"])
                labels = nx.get_node_attributes(self.parseGraph, "label")
                nx.draw(self.parseGraph, labels=labels, with_labels=True)
                # plt.show()
                result = self.execute_parse_tree(self.parseGraph)
                print("Result:", result)
            else:
                print("Failed to parse input.")

    def main(self,file):
        """
        Main function to parse the file
        """
        self.execute_file(file)
        line = 0
        results = []
        if len(self.command_queue) < 1:
            new_data = input(">")
            self.command_queue.append(new_data)
        while len(self.command_queue) > 0:
            data = self.command_queue.pop(0)
            self.parseGraph = nx.Graph()
            self.NODE_COUNTER = 0
            root = self.add_node({"type": "INITIAL", "label": "INIT"})
            result = self.parser.parse(data)
            if result:
                self.parseGraph.add_edge(root["counter"], result["counter"])
                result = self.execute_parse_tree(self.parseGraph)
                labels = nx.get_node_attributes(self.parseGraph, "label")
                # Save the file in trees directory
                paths = file.split("/")
                for i in range(1, len(paths)):
                    if not os.path.exists(f"trees/{'/'.join(paths[:i])}"):
                        os.mkdir(f"trees/{'/'.join(paths[:i])}")
                
                nx.draw(self.parseGraph, labels=labels, with_labels=True)
                plt.savefig(f"trees/{file}_{line}.png")
                # Restart tree
                plt.clf()
                results.append(result)
            else:
                raise Exception("Failed to parse input in line " + str(line))
            line += 1
        # save all res to file in one line, results separed by comma ex [1 ,2 ,3 ,4]
        # with open("output.txt", "w") as f:
        #     f.write(str(results).replace("\n", ""))
        return results

