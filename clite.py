import ply.lex as lex
import ply.yacc as yacc


keywords = {
    'int': 'INT',
    'bool': 'BOOL',
    'float': 'FLOAT',
    'char': 'CHAR',
    'main': 'MAIN',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
}

tokens = [
    'INTLIT',
    'FLOATLIT',
    'ID',
    'LE',
    'GE',
    'EQ',
    'NEQ',
    'AND',
    'OR',
] + list(keywords.values())

t_ignore = ' \t\r'

t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_AND = r'&&'
t_OR = r'\|\|'

literals = '+-*/%(){};=<>!'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lineno}")

lexer = lex.lex()

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
)

def p_Program(p):
    """
    Program : INT MAIN '(' ')' '{' Declarations Statements '}'
    """
    p[0] = ('program', p[6], p[7])

def p_EPSILON(p):
    """
    EPSILON :
    """
    p[0] = None

def p_Declarations(p):
    """
    Declarations : EPSILON
                 | Declarations Declaration
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_Declaration(p):
    """
    Declaration : Type ID ';'
    """
    p[0] = ('decl', p[1], p[2])

def p_Type(p):
    """
    Type : INT
         | BOOL
         | FLOAT
         | CHAR
    """
    p[0] = p[1]

def p_Statements(p):
    """
    Statements : EPSILON
               | Statements Statement
    """
    if p[1] is None:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_Statement(p):
    """
    Statement : ';'
              | Block
              | Assignment
              | IfStatement
              | WhileStatement
    """
    if p.slice[1].type == ';':
        p[0] = ('empty',)
    else:
        p[0] = p[1]

def p_Block(p):
    """
    Block : '{' Statements '}'
    """
    p[0] = ('block', p[2])

def p_Assignment(p):
    """
    Assignment : ID '=' Expression ';'
    """
    p[0] = ('assign', p[1], p[3])

def p_IfStatement(p):
    """
    IfStatement : IF '(' Expression ')' Statement ElsePart
    """
    p[0] = ('if', p[3], p[5], p[6])

def p_ElsePart(p):
    """
    ElsePart : EPSILON %prec IFX
             | ELSE Statement
    """
    if p[1] is None:
        p[0] = None
    else:
        p[0] = p[2]

def p_WhileStatement(p):
    """
    WhileStatement : WHILE '(' Expression ')' Statement
    """
    p[0] = ('while', p[3], p[5])

def p_Expression(p):
    """
    Expression : Conjunction
               | Expression OR Conjunction
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('or', p[1], p[3])

def p_Conjunction(p):
    """
    Conjunction : Equality
                | Conjunction AND Equality
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('and', p[1], p[3])

def p_Equality(p):
    """
    Equality : Relation
             | Relation EquOp Relation
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_EquOp(p):
    """
    EquOp : EQ
          | NEQ
    """
    p[0] = p[1]

def p_Relation(p):
    """
    Relation : Addition
             | Addition RelOp Addition
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_RelOp(p):
    """
    RelOp : '<'
          | LE
          | '>'
          | GE
    """
    p[0] = p[1]

def p_Addition(p):
    """
    Addition : Term
             | Addition AddOp Term
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_AddOp(p):
    """
    AddOp : '+'
          | '-'
    """
    p[0] = p[1]

def p_Term(p):
    """
    Term : Factor
         | Term MulOp Factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_MulOp(p):
    """
    MulOp : '*'
          | '/'
          | '%'
    """
    p[0] = p[1]

def p_Factor(p):
    """
    Factor : Primary
           | UnaryOp Primary
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('unary' + p[1], p[2])

def p_UnaryOp(p):
    """
    UnaryOp : '-'
            | '!'
    """
    p[0] = p[1]

def p_Primary(p):
    """
    Primary : ID
            | INTLIT
            | FLOATLIT
            | '(' Expression ')'
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_error(p):
    if p is None:
        raise SyntaxError("Unexpected end of input")
    raise SyntaxError(f"Syntax error at token {p.type} ({p.value!r}) line {p.lineno}")

parser = yacc.yacc(start='Program')

if __name__ == '__main__':
    program = """
    int main() {
        int x;
        float y;
        x = 5;
        if (x > 0) y = 3.14;
        while (x != 0) x = x - 1;
    }
    """
    print(parser.parse(program, lexer=lexer))
