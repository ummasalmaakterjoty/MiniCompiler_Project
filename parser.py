import ply.lex as lex
import ply.yacc as yacc
import sys



# reserved keywords
reserved = {
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT'
}

# token list
tokens = [
    'ID', 'NUM',
    'EQ', 'NE', 'GE', 'LE', 'GT', 'LT',
    'ASSIGN', 'SEMI', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PLUS', 'MINUS', 'MUL', 'DIV',
    'COMMENT'
] + list(reserved.values())

# token regexes
t_EQ     = r'=='
t_NE     = r'!='
t_GE     = r'>='
t_LE     = r'<='
t_GT     = r'>'
t_LT     = r'<'
t_ASSIGN = r'='
t_SEMI   = r';'
t_COMMA  = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'


t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT_SINGLE(t):
    r'//.*'  
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def make_lexer():
    return lex.lex()

def categorize_tokens(source_text):
    lx = make_lexer()
    lx.input(source_text)

    categories = {
        'Keyword': [],
        'Identifier': [],
        'Constant': [],
        'Operator': [],
        'Punctuation': [],
        'Comment': []
    }

    while True:
        tok = lx.token()
        if not tok:
            break
        if tok.type in ['INT', 'IF', 'ELSE', 'WHILE', 'PRINT']:
            categories['Keyword'].append(tok.value)
        elif tok.type == 'ID':
            categories['Identifier'].append(tok.value)
        elif tok.type == 'NUM':
            categories['Constant'].append(tok.value)
        elif tok.type in ['PLUS', 'MINUS', 'MUL', 'DIV', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT', 'ASSIGN']:
            categories['Operator'].append(tok.value)
        elif tok.type in ['SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE']:
            categories['Punctuation'].append(tok.value)
        elif tok.type == 'COMMENT':
            categories['Comment'].append(tok.value)

    print("\n--- LEXICAL ANALYSIS ---")
    for cat, items in categories.items():
        display = ', '.join(map(str, items))
        print(f"{cat} ({len(items)}): {display}")

symbol_table = {}      
tac = []               
_temp_count = 0
_label_count = 0

def new_temp():
    global _temp_count
    _temp_count += 1
    return f"t{_temp_count}"

def new_label():
    global _label_count
    _label_count += 1
    return f"L{_label_count}"


lexer_for_parser = make_lexer()


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)

def p_program(p):
    'program : statement_list'
    print("\n✅ Parsing completed successfully!")
    
    print("\n--- SYMBOL TABLE ---")
    for name, val in symbol_table.items():
        print(f"{name} = {val}")
    
    print("\n--- THREE ADDRESS CODE ---")
    for line in tac:
        print(line)
    
    print("\n--- ASSEMBLY-LIKE CODE ---")
    assembly = tac_to_assembly(tac)
    for a in assembly:
        print(a)

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | if_else_statement
                 | while_statement
                 | print_statement'''
    
def p_declaration(p):
    'declaration : INT ID ASSIGN expression SEMI'
    var = p[2]
    expr_val = p[4]

    symbol_table[var] = expr_val
    
    tac.append(f"{var} = {expr_val}")
    print(f"Declared {var} = {expr_val}")

def p_assignment(p):
    'assignment : ID ASSIGN expression SEMI'
    var = p[1]
    expr_val = p[3]
    symbol_table[var] = expr_val
    tac.append(f"{var} = {expr_val}")
    print(f"Assigned {var} = {expr_val}")

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMI'
    val = p[3]
    tac.append(f"PRINT {val}")
    print(f"Print statement executed: {val}")

def p_if_statement(p):
    'if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE'
    cond = p[3]
    
    label = new_label()
    tac.append(f"IF {cond} GOTO {label}")
    tac.append(f"{label}:")
    print(f"If condition checked: {cond}")

def p_if_else_statement(p):
    'if_else_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'
    cond = p[3]
    Lelse = new_label()
    Lend  = new_label()

    tac.append(f"IF_FALSE {cond} GOTO {Lelse}")
    tac.append(f"GOTO {Lend}")
    tac.append(f"{Lelse}:")
    tac.append(f"{Lend}:")
    print(f"If-Else condition checked: {cond}")

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE'
    cond = p[3]
    start = new_label()
    end = new_label()
    tac.append(f"LABEL {start}")
    tac.append(f"IF_FALSE {cond} GOTO {end}")
    tac.append(f"GOTO {start}")
    tac.append(f"{end}:")
    print(f"While loop condition checked: {cond}")

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
    left = p[1]
    op = p[2]
    right = p[3]
    temp = new_temp()
    tac.append(f"{temp} = {left} {op} {right}")
    p[0] = temp

def p_expression_num(p):
    'expression : NUM'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = symbol_table.get(p[1], p[1])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
        parser.errok()
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def tac_to_assembly(tac_list):
    asm = []
    for line in tac_list:
        if not line or line.strip() == '':
            continue
        line = line.strip()

        if line.endswith(':'):
            asm.append(line)
            continue
        if line.startswith('LABEL '):
            asm.append(line.replace('LABEL ', ''))
            continue

        if line.startswith('PRINT '):
            _, val = line.split(maxsplit=1)
            asm.append(f"LOAD {val}")
            asm.append("PRINT")
            continue

        if line.startswith('IF_FALSE '):
            parts = line.split()

            if len(parts) >= 4 and parts[-2] == 'GOTO':
                cond = ' '.join(parts[1:-2])
                label = parts[-1]
                
                asm.append(f"LOAD {cond}")
                asm.append(f"JZ {label}")   
            else:
                asm.append(f"; UNHANDLED {line}")
            continue

        if line.startswith('IF '):
            parts = line.split()
    
            if len(parts) >= 4 and parts[-2] == 'GOTO':
                cond = ' '.join(parts[1:-2])
                label = parts[-1]
                asm.append(f"LOAD {cond}")
                asm.append(f"JNZ {label}")  
            else:
                asm.append(f"; UNHANDLED {line}")
            continue
    
        if line.startswith('GOTO '):
            label = line.split()[1]
            asm.append(f"JMP {label}")
            continue

        if '=' in line:
            dest, expr = line.split('=', 1)
            dest = dest.strip()
            expr = expr.strip()

            if ' + ' in expr:
                a, b = expr.split(' + ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"ADD {b.strip()}")
                asm.append(f"STORE {dest}")
            elif ' - ' in expr:
                a, b = expr.split(' - ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"SUB {b.strip()}")
                asm.append(f"STORE {dest}")
            elif ' * ' in expr:
                a, b = expr.split(' * ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"MUL {b.strip()}")
                asm.append(f"STORE {dest}")
            elif ' / ' in expr:
                a, b = expr.split(' / ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"DIV {b.strip()}")
                asm.append(f"STORE {dest}")
            elif ' > ' in expr:
                a, b = expr.split(' > ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"LOAD {b.strip()}")
                asm.append("CMPGT")
                asm.append(f"STORE {dest}")
            elif ' < ' in expr:
                a, b = expr.split(' < ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"LOAD {b.strip()}")
                asm.append("CMPLT")
                asm.append(f"STORE {dest}")
            elif ' == ' in expr:
                a, b = expr.split(' == ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"LOAD {b.strip()}")
                asm.append("CMPEQ")
                asm.append(f"STORE {dest}")
            elif ' != ' in expr:
                a, b = expr.split(' != ')
                asm.append(f"LOAD {a.strip()}")
                asm.append(f"LOAD {b.strip()}")
                asm.append("CMPNE")
                asm.append(f"STORE {dest}")
            else:
                asm.append(f"LOAD {expr}")
                asm.append(f"STORE {dest}")
            continue
        asm.append(f"; {line}")

    return asm

def main():
    data = sys.stdin.read()

    if not data.strip():
        print("No input provided. Please provide source code in input.txt or via stdin.")
        return
    categorize_tokens(data)

    global parser
    parser.parse(data, lexer=make_lexer())

if __name__ == '__main__':
    main()
