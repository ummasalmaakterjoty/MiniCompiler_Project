import ply.lex as lex

# Reserved words mapping
reserved = {
    'int'   : 'INT',
    'if'    : 'IF',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'print' : 'PRINT'
}

# Token names
tokens = [
    'ID', 'NUM',
    'EQ', 'NE', 'GE', 'LE', 'GT', 'LT',
    'ASSIGN', 'SEMI', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PLUS', 'MINUS', 'MUL', 'DIV'
] + list(reserved.values())

# Symbols
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

# ID and NUM
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # check for reserved words
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
