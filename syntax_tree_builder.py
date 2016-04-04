import re

f1 = open("output.txt")
text = f1.read()
text_array = text.split("\n")
token_array = []
symbol_table_array = []
input_output_detected = False

for line in text_array:
    if input_output_detected:
        input_output_detected = False
        continue
    if re.match(r'entry:', line):
        symbol = line.split("symbol:")[1].strip()
        symbol_table_array.append(symbol)
    if not re.match(r'Token:', line):
        continue
    elif re.match(r'Token: <PREPROCESSOR', line) or re.match(r'Token: <COMMENT', line):
        continue
    elif re.match(r'Token: <INPUT_OUTPUT', line):
        input_output_detected = True
        continue
    x = line.split(": <")[1].split(",")[0].strip()
    y = line.split(",")[1].split(">")[0].strip()
    if x == 'CONDITIONAL_OPERATOR' and y == '':
        y = '>'
    if x == 'SPECIAL_SYMBOL' and y == '':
        y = ','
    if y == 'else if':
        token_array.append((x, 'else'))
        y = 'if'
    token_array.append((x, y))

node_list = []
num_list = []
for i in range(5000, 0, -1):
    num_list.append(i)


class Node:
    def __init__(self, initdata, initname, parent_num):
        self.num = initdata
        self.name = initname
        self.child_num_list = []
        self.parent_num = parent_num
        node_list.append(self)

    def get_num(self):
        return self.num

    def get_name(self):
        return self.name

    def get_parent_num(self):
        return self.parent_num

    def get_child_num_list(self):
        return self.child_num_list

    def add_child_num(self, num):
        self.child_num_list.append(num)

# building syntax tree
start_node = Node(num_list.pop(), "program", 0)


# function takes token_array stream as input, outputs nodes and recursive function
# rule_num is the grammar rule to be followed and node is the LHS of the rule
def builder(array, in_braces_count, rule_num, node):
    parenthesis_count = in_braces_count
    # program -> declaration_list
    if rule_num == 1:
        temp_node = Node(num_list.pop(), "declaration_list", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(array, in_braces_count, 2, temp_node)
        return 1
    # declaration_list -> declaration_list declaration | declaration
    if rule_num == 2:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            temp_array2.append(array[i])
            if array[i][0] == 'OPEN_PARENTHESIS':
                parenthesis_count += 1
            if array[i][0] == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1

            if (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i == (len(array) - 1) and parenthesis_count == in_braces_count:
                if not temp_array1:
                    temp_node2 = Node(num_list.pop(), "declaration", node.get_num())
                    node.add_child_num(temp_node2.get_num())
                    builder(temp_array2, parenthesis_count, 3, temp_node2)
                    return 2
                temp_node1 = Node(num_list.pop(), "declaration_list", node.get_num())
                node.add_child_num(temp_node1.get_num())
                builder(temp_array1, parenthesis_count, 2, temp_node1)
                temp_node2 = Node(num_list.pop(), "declaration", node.get_num())
                node.add_child_num(temp_node2.get_num())
                builder(temp_array2, parenthesis_count, 3, temp_node2)
                return 2
            elif (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i < (len(array) - 1) and parenthesis_count == in_braces_count:
                temp_array1 += temp_array2
                temp_array2 = []
    # declaration -> var_declaration | fun_declaration
    if rule_num == 3:
        if array[len(array) - 1][0] == 'SEMI' and not array[len(array) - 2][0] == 'BRACKET':
            temp_node = Node(num_list.pop(), "var_declaration", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(array, in_braces_count, 4, temp_node)
        # if array[len(array) - 1][0] == 'CLOSE_PARENTHESIS':
        else:
            temp_node = Node(num_list.pop(), "fun_declaration", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(array, in_braces_count, 9, temp_node)
        return 3
    # var_declaration -> type_specifier var_declaration_list ';'
    if rule_num == 4:
        temp_array = [array[0]]
        temp_node = Node(num_list.pop(), "type_specifier", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 8, temp_node)

        temp_array = []
        for i in range(1, len(array) - 1, 1):
            temp_array.append(array[i])
        temp_node = Node(num_list.pop(), "var_declaration_list", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 5, temp_node)

        temp_node = Node(num_list.pop(), "SEMI", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node2 = Node(num_list.pop(), ";", node.get_num())
        temp_node.add_child_num(temp_node2.get_num())
        return 4
    # var_declaration_list -> var_declaration_list ',' var_declaration_initialize | var_declaration_initialize
    if rule_num == 5:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            if array[i] == ',':
                temp_array1 += temp_array2
                temp_array2 = []
            temp_array2.append(array[i])
        if not temp_array1:
            temp_node2 = Node(num_list.pop(), "var_declaration_initialize", node.get_num())
            node.add_child_num(temp_node2.get_num())
            builder(temp_array2, parenthesis_count, 6, temp_node2)
            return 5
        temp_node1 = Node(num_list.pop(), "var_declaration_list", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_array1.pop()
        temp_node = Node(num_list.pop(), "COMMA", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), ",", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())
        builder(temp_array1, parenthesis_count, 5, temp_node1)
        temp_node2 = Node(num_list.pop(), "var_declaration_initialize", node.get_num())
        node.add_child_num(temp_node2.get_num())
        builder(temp_array2, parenthesis_count, 6, temp_node2)
        return 5
    # var_declaration_initialize -> var_declaration_id | var_declaration_id '=' expression
    if rule_num == 6:
        temp_array = [array[0]]
        temp_node = Node(num_list.pop(), "var_declaration_id", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 7, temp_node)
        if len(array) == 1:
            return 6

        if array[1][1] == '=':
            temp_node = Node(num_list.pop(), "ASSIGNMENT_OPERATOR", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node2 = Node(num_list.pop(), "=", node.get_num())
            temp_node.add_child_num(temp_node2.get_num())

            temp_array = array
            if array[len(array) - 1][1] == ',':
                temp_array.pop()
            temp_node = Node(num_list.pop(), "expression", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(temp_array, in_braces_count, 19, temp_node)

        if array[len(array) - 1][1] == ',':
            temp_node = Node(num_list.pop(), "COMMA", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), ",", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
        return 6
    # var_declaration_id -> IDENTIFIER
    if rule_num == 7:
        temp_node1 = Node(num_list.pop(), "IDENTIFIER", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_node2 = Node(num_list.pop(), str(symbol_table_array[int(array[0][1])]), node.get_num())
        temp_node1.add_child_num(temp_node2.get_num())
        return 7
    # type_specifier	-> VOID | INT
    if rule_num == 8:
        if array[0][1] == 'void':
            temp_node = Node(num_list.pop(), "VOID", node.get_num())
            node.add_child_num(temp_node.get_num())
        # if array[0][1] == 'int':
        else:
            temp_node = Node(num_list.pop(), "INT", node.get_num())
            node.add_child_num(temp_node.get_num())
        return 8
    # fun_declaration -> type_specifier fun_declarator compound_statement | type_specifier fun_declarator ';'
    if rule_num == 9:
        temp_array = [array[0]]
        temp_node = Node(num_list.pop(), "type_specifier", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 8, temp_node)

        temp_array = []
        temp_array2 = []
        temp_array2_started = False
        for temp in array:
            if temp[1] == '{' or temp_array2_started:
                temp_array2_started = True
                temp_array2.append(temp)
            else:
                temp_array.append(temp)
        temp_array.pop(0)
        temp_node = Node(num_list.pop(), "fun_declarator", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 10, temp_node)

        if not temp_array2:
            temp_node = Node(num_list.pop(), "SEMI", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), ";", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
        if temp_array2:
            temp_node = Node(num_list.pop(), "compound_statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(temp_array2, in_braces_count, 15, temp_node)
        return 9
    # fun_declarator -> IDENTIFIER '(' parameter_list ')'| IDENTIFIER '(' ')'
    if rule_num == 10:
        if array[0][1] == 'main':
            temp_node1 = Node(num_list.pop(), "MAIN_FUNCTION", node.get_num())
            node.add_child_num(temp_node1.get_num())
            temp_node1 = Node(num_list.pop(), "main", node.get_num())
            node.add_child_num(temp_node1.get_num())
        else:
            temp_node1 = Node(num_list.pop(), "IDENTIFIER", node.get_num())
            node.add_child_num(temp_node1.get_num())
            temp_node2 = Node(num_list.pop(), str(symbol_table_array[int(array[0][1])]), node.get_num())
            temp_node1.add_child_num(temp_node2.get_num())

        temp_node = Node(num_list.pop(), "BRACKET", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), "(", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())

        if len(array) > 3:
            temp_array = array
            temp_array.pop()
            temp_array.pop(0)
            temp_array.pop(0)
            temp_node2 = Node(num_list.pop(), "parameter_list", node.get_num())
            node.add_child_num(temp_node2.get_num())
            builder(temp_array, parenthesis_count, 11, temp_node2)

        temp_node = Node(num_list.pop(), "BRACKET", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), ")", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())
        return 10
    # parameter_list -> parameter_declaration | parameter_list ',' parameter_declaration
    if rule_num == 11:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            if array[i] == ',':
                temp_array1 += temp_array2
                temp_array2 = []
            temp_array2.append(array[i])
        if not temp_array1:
            temp_node2 = Node(num_list.pop(), "parameter_declaration", node.get_num())
            node.add_child_num(temp_node2.get_num())
            builder(temp_array2, parenthesis_count, 12, temp_node2)
            return 11
        temp_node1 = Node(num_list.pop(), "parameter_list", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_array1.pop()
        temp_node = Node(num_list.pop(), "COMMA", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), ",", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())
        builder(temp_array1, parenthesis_count, 11, temp_node1)
        temp_node2 = Node(num_list.pop(), "parameter_declaration", node.get_num())
        node.add_child_num(temp_node2.get_num())
        builder(temp_array2, parenthesis_count, 12, temp_node2)
        return 11
    # parameter_declaration -> type_specifier declarator
    if rule_num == 12:
        temp_array1 = [array[0]]
        temp_array2 = [array[1]]
        temp_node = Node(num_list.pop(), "type_specifier", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array1, in_braces_count, 8, temp_node)
        temp_node = Node(num_list.pop(), "declarator", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array2, in_braces_count, 13, temp_node)
        return 12
    # declarator -> IDENTIFIER
    if rule_num == 13:
        temp_node1 = Node(num_list.pop(), "IDENTIFIER", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_node2 = Node(num_list.pop(), str(symbol_table_array[int(array[0][1])]), node.get_num())
        temp_node1.add_child_num(temp_node2.get_num())
        return 13
    # constant_expression -> INT_CONSTANT
    if rule_num == 14:
        temp_node1 = Node(num_list.pop(), "constant_expression", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_node2 = Node(num_list.pop(), str(array[0][1]), node.get_num())
        temp_node1.add_child_num(temp_node2.get_num())
        return 14
    # compound_statement -> '{' '}' | '{' statement_list '}'  | '{' declaration_list statement_list '}' | ';'
    if rule_num == 15:
        if len(array) == 1:
            temp_node = Node(num_list.pop(), "SEMI", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), ";", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
        elif len(array) == 2:
            temp_node = Node(num_list.pop(), "OPEN_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "{", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

            temp_node = Node(num_list.pop(), "CLOSE_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "}", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
        else:
            temp_node = Node(num_list.pop(), "OPEN_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "{", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

            decl = False
            decl_array = []
            stat_array = []
            for i in range(1, len(array) - 1, 1):
                if array[i][0] == 'DATATYPE':
                    decl = True
                if array[i][0] == 'SEMI' and decl:
                    decl_array.append(array[i])
                    decl = False
                    continue
                if array[i][0] == 'OPEN_PARENTHESIS':
                    parenthesis_count += 1
                if array[i][0] == 'CLOSE_PARENTHESIS':
                    parenthesis_count -= 1
                if decl and parenthesis_count == in_braces_count:
                    decl_array.append(array[i])
                elif parenthesis_count == in_braces_count:
                    stat_array.append(array[i])
            if decl_array:
                temp_node = Node(num_list.pop(), "declaration_list", node.get_num())
                node.add_child_num(temp_node.get_num())
                builder(decl_array, in_braces_count + 1, 33, temp_node)
            if stat_array:
                temp_node = Node(num_list.pop(), "statement_list", node.get_num())
                node.add_child_num(temp_node.get_num())
                builder(stat_array, in_braces_count + 1, 16, temp_node)

            temp_node = Node(num_list.pop(), "CLOSE_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "}", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

        return 15
    # statement_list -> statement | statement_list statement
    if rule_num == 16:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            temp_array2.append(array[i])
            if array[i][0] == 'OPEN_PARENTHESIS':
                parenthesis_count += 1
            if array[i][0] == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1

            if parenthesis_count == in_braces_count:
                if (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i == (len(array) - 1):
                    if not temp_array1:
                        temp_node2 = Node(num_list.pop(), "statement", node.get_num())
                        node.add_child_num(temp_node2.get_num())
                        builder(temp_array2, parenthesis_count, 17, temp_node2)
                        return 16

                    if temp_array1:
                        temp_node1 = Node(num_list.pop(), "statement_list", node.get_num())
                        node.add_child_num(temp_node1.get_num())
                        builder(temp_array1, parenthesis_count, 16, temp_node1)
                    if temp_array2:
                        temp_node2 = Node(num_list.pop(), "statement", node.get_num())
                        node.add_child_num(temp_node2.get_num())
                        builder(temp_array2, parenthesis_count, 17, temp_node2)
                    return 16
                elif (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i < (len(array) - 1):
                    if not array[i + 1][1] == 'else if' and not array[i + 1][1] == 'else':
                        temp_array1 += temp_array2
                        temp_array2 = []
        return 16
    # statement -> '{' statement_list '}'  //a solution to the local decl problem
    #   | selection_statement | iteration_statement | assignment_statement | RETURN expression ';'
    if rule_num == 17:
        if array[0][1] == '{' and array[len(array) - 1][1] == '}':
            temp_node = Node(num_list.pop(), "OPEN_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "{", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

            temp_array = array
            temp_array.pop()
            temp_array.pop(0)
            temp_node = Node(num_list.pop(), "statement_list", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(temp_array, in_braces_count + 1, 16, temp_node)

            temp_node = Node(num_list.pop(), "CLOSE_PARENTHESIS", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "}", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
            return 17
        elif array[0][1] == 'if':
            temp_node = Node(num_list.pop(), "selection_statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(array, in_braces_count, 31, temp_node)
            return 17
        elif array[0][1] == 'while':
            temp_node = Node(num_list.pop(), "iteration_statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(array, in_braces_count, 32, temp_node)
            return 17
        elif array[0][1] == 'return':
            temp_node = Node(num_list.pop(), "RETURN_statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "return", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

            temp_array = array
            temp_array.pop()
            temp_array.pop(0)
            temp_node = Node(num_list.pop(), "expression", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(temp_array, in_braces_count, 19, temp_node)

            temp_node = Node(num_list.pop(), "SEMI", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), ";", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())
            return 17
        else:
            temp_node = Node(num_list.pop(), "assignment_statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(array, in_braces_count, 18, temp_node)
        return 17
    # assignment_statement -> ';' |  l_expression '=' expression ';'
    if rule_num == 18:

        return 18
    # expression -> logical_and_expression | expression OR_OP logical_and_expression
    if rule_num == 19:
        return 19

    # logical_and_expression ->  equality_expression   | logical_and_expression AND_OP equality_expression
    if rule_num == 20:
        return 20
    # equality_expression ->  relational_expression  | equality_expression EQ_OP relational_expression
    # | equality_expression NE_OP relational_expression
    if rule_num == 21:
        return 21
    # relational_expression ->  additive_expression  | relational_expression '<' additive_expression
    # | relational_expression '>' additive_expression| relational_expression LE_OP additive_expression
    # | relational_expression GE_OP additive_expression
    if rule_num == 22:
        return 22
    # additive_expression ->    multiplicative_expression | additive_expression '+' multiplicative_expression
    # | additive_expression '-' multiplicative_expression
    if rule_num == 23:
        return 23
    # multiplicative_expression -> unary_expression | multiplicative_expression '*' unary_expression
    # | multiplicative_expression '/' unary_expression
    if rule_num == 24:
        return 24
    # unary_expression ->   postfix_expression | unary_operator postfix_expression
    if rule_num == 25:
        return 25
    # postfix_expression ->  primary_expression | IDENTIFIER '(' ')'
    # | IDENTIFIER '(' expression_list ')'| l_expression INC_OP
    if rule_num == 26:
        return 26
    # primary_expression -> l_expression | l_expression '=' expression | INT_CONSTANT | FLOAT_CONSTANT
    # | STRING_LITERAL| '(' expression ')'
    if rule_num == 27:
        return 27
    # l_expression -> IDENTIFIER | l_expression '[' expression ']'
    if rule_num == 28:
        return 28
    # expression_list ->  expression  | expression_list ',' expression
    if rule_num == 29:
        return 29
    # unary_operator -> '-' | '!'
    if rule_num == 30:
        return 30
    # selection_statement -> IF '(' expression ')' statement ELSE statement | IF '(' expression ')' statement
    if rule_num == 31:
        temp_node = Node(num_list.pop(), "IF", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), "if", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())

        temp_node = Node(num_list.pop(), "BRACKET", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), "(", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())

        temp_array = []
        temp_array1 = []
        temp_array2 = []
        exp = True
        else_found = False
        bracket_count = 1
        for i in range(2, len(array), 1):
            if array[i][1] == '(':
                bracket_count += 1
            if array[i][1] == ')':
                bracket_count -= 1
            if exp:
                temp_array.append(array[i])
            if bracket_count == 0 and array[i][1] == ')' and exp:
                exp = False
            if not exp and else_found:
                temp_array2.append(array[i])
            if not exp and not else_found:
                temp_array1.append(array[i])
            if array[i][1] == 'else':
                else_found = True
                temp_array1.pop()

        temp_array.pop()
        temp_array1.pop(0)

        temp_node = Node(num_list.pop(), "expression", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 19, temp_node)

        temp_node = Node(num_list.pop(), "BRACKET", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), ")", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())

        temp_node = Node(num_list.pop(), "statement", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array1, in_braces_count, 100, temp_node)

        if else_found and temp_array2:
            temp_node = Node(num_list.pop(), "ELSE", node.get_num())
            node.add_child_num(temp_node.get_num())
            temp_node1 = Node(num_list.pop(), "else", node.get_num())
            temp_node.add_child_num(temp_node1.get_num())

            temp_node = Node(num_list.pop(), "statement", node.get_num())
            node.add_child_num(temp_node.get_num())
            builder(temp_array2, in_braces_count, 17, temp_node)

        return 31
    # iteration_statement ->  WHILE '(' expression ')' statement
    # | FOR '(' expression ';' expression ';' expression ')' statement
    if rule_num == 32:
        return 32
    # declaration_list -> declaration  | declaration_list declaration
    if rule_num == 33:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            temp_array2.append(array[i])
            if array[i][0] == 'OPEN_PARENTHESIS':
                parenthesis_count += 1
            if array[i][0] == 'CLOSE_PARENTHESIS':
                parenthesis_count -= 1

            if (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i == (len(array) - 1) and parenthesis_count == in_braces_count:
                if not temp_array1:
                    temp_node2 = Node(num_list.pop(), "declaration", node.get_num())
                    node.add_child_num(temp_node2.get_num())
                    builder(temp_array2, parenthesis_count, 34, temp_node2)
                    return 33
                temp_node1 = Node(num_list.pop(), "declaration_list", node.get_num())
                node.add_child_num(temp_node1.get_num())
                builder(temp_array1, parenthesis_count, 33, temp_node1)
                temp_node2 = Node(num_list.pop(), "declaration", node.get_num())
                node.add_child_num(temp_node2.get_num())
                builder(temp_array2, parenthesis_count, 34, temp_node2)
                return 33
            elif (array[i][0] == 'SEMI' or array[i][0] == 'CLOSE_PARENTHESIS') and i < (len(array) - 1) and parenthesis_count == in_braces_count:
                temp_array1 += temp_array2
                temp_array2 = []
        return 33
    # declaration -> type_specifier declarator_list';'
    if rule_num == 34:
        temp_array = [array[0]]
        temp_node = Node(num_list.pop(), "type_specifier", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 8, temp_node)

        temp_array = []
        for i in range(1, len(array) - 1, 1):
            temp_array.append(array[i])
        temp_node = Node(num_list.pop(), "declarator_list", node.get_num())
        node.add_child_num(temp_node.get_num())
        builder(temp_array, in_braces_count, 35, temp_node)

        temp_node = Node(num_list.pop(), "SEMI", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node2 = Node(num_list.pop(), ";", node.get_num())
        temp_node.add_child_num(temp_node2.get_num())
        return 34
    # declarator_list -> declarator | declarator_list ',' declarator
    if rule_num == 35:
        temp_array1 = []
        temp_array2 = []
        for i in range(0, len(array), 1):
            if array[i] == ',':
                temp_array1 += temp_array2
                temp_array2 = []
            temp_array2.append(array[i])
        if not temp_array1:
            temp_node2 = Node(num_list.pop(), "declarator", node.get_num())
            node.add_child_num(temp_node2.get_num())
            builder(temp_array2, parenthesis_count, 6, temp_node2)
            return 35
        temp_node1 = Node(num_list.pop(), "declarator_list", node.get_num())
        node.add_child_num(temp_node1.get_num())
        temp_array1.pop()
        temp_node = Node(num_list.pop(), "COMMA", node.get_num())
        node.add_child_num(temp_node.get_num())
        temp_node1 = Node(num_list.pop(), ",", node.get_num())
        temp_node.add_child_num(temp_node1.get_num())
        builder(temp_array1, parenthesis_count, 5, temp_node1)
        temp_node2 = Node(num_list.pop(), "declarator", node.get_num())
        node.add_child_num(temp_node2.get_num())
        builder(temp_array2, parenthesis_count, 6, temp_node2)
        return 35

builder(token_array, 0, 1, start_node)


# get child from child_number
def get_child(num):
    for node in node_list:
        if node.get_num() == num:
            return node


# display
def display(node, tab_num):
    tab_string = ''
    for i in range(0, tab_num, 1):
        tab_string += '|   '
    if not node.get_child_num_list():
        print tab_string + " " + node.get_name()
    else:
        print tab_string + str(node.get_num()) + " " + node.get_name() + " -> "
    for child_num in node.get_child_num_list():
        display(get_child(child_num), tab_num + 1)

display(start_node, 0)
