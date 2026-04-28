import ply.lex as lex
import ply.yacc as yacc


keywords = {
    'while': 'WHILE',
    'if': 'IF',
}

tokens = [
    'INTLIT',
    'ID',
    'FLOATLIT',
    'LE',
    'GE',
    'EQ',
    'NEQ',
    'STR'
] + list(keywords.values())

t_ignore = ' \t\n'

t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NEQ = r'!='

literals = '!+*-(){},;='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords.keys():
        t.type = keywords[t.value]
    return t

def t_FLOATLIT(t):
    r'\d(_?\d)*\.\d(_?\d)*'
    t.value = float(t.value)
    return t

def t_INTLIT(t):
    r'[0-9](_?[0-9])*'
    t.value = int(t.value)
    return t   

lexer = lex.lex()

# lexer.input("3.14 * r * r")

# while True:
#     t = lexer.token()
#     print(t)
#     if t == None:
#         break

def p_Term(p):
    """
    Term : Factor
         | Term '*' Factor
    """

def p_MulOp(p):
    """
    MulOp : '*'
        | '/'
            
    """
    return p    

def p_Factor(p):
    """
    Factor : '!' Primary
           | Primary
    """

def p_Primary(p):
    """
    Primary : ID
            | INTLIT
            | FLOATLIT
            | '(' Factor ')'
    """
    
program = """
!(3.1415)
"""
    
parser = yacc.yacc()
print(parser.parse(program))