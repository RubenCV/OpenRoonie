# ----------------------------------------------------------- #
#   ____                     _____                   _        #
#  / __ \                   |  __ \                 (_)       #
# | |  | |_ __   ___ _ __   | |__) |___   ___  _ __  _  ___   #
# | |  | | '_ \ / _ \ '_ \  |  _  // _ \ / _ \| '_ \| |/ _ \  #
# | |__| | |_) |  __/ | | | | | \ \ (_) | (_) | | | | |  __/  #
#  \____/| .__/ \___|_| |_| |_|  \_\___/ \___/|_| |_|_|\___|  #
#        | |                                                  #
#        |_|                                                  #
#                                                             #
#       Antonio Carlos Vargas Torres          A00813182       #
#       Rubén Eugenio Cantu Vota              A00814298       #
# ----------------------------------------------------------- #

import os.path
import Stack as Stack
import FunctionDirectory as FunctionDirectory

TypeStack = Stack.Stack()
FunctionStack = Stack.Stack()
FunctionDirectory = FunctionDirectory.FunctionDirectory();

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'var' : 'VAR',
   'program' : 'PROGRAM',
   'int' : 'INT',
   'float' : 'FLOAT',
   'char' : 'CHAR',
   'bool' : 'BOOL',
   'True' : 'TRUE',
   'False' : 'FALSE',
   'string' : 'STRING',
   'print' : 'PRINT',
   'function' : 'FUNCTION',
   'main' : 'MAIN',
   'while' : 'WHILE',
   'execute' : 'EXECUTE',
   'quit' : 'QUIT',
}

tokens = [
    'ID',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'LBRACKET', 'RBRACKET',
    'LSQBRACKET','RSQBRACKET',
    'SEMICOLON', 'COMMA', 'MORETHAN', 'LESSTHAN', 'NOTEQUAL',
    'CTEINT', 'CTEFLOAT', 'CTESTRING', 'CTECHAR',
    'MORETHANEQUAL', 'LESSTHANEQUAL', 'ISEQUALTO',
    'OR', 'AND',
    ] + list(reserved.values())

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_LSQBRACKET  = r'\['
t_RSQBRACKET  = r'\]'
t_SEMICOLON  = r';'
t_COMMA  = r','
t_MORETHAN  = r'>'
t_LESSTHAN  = r'<'
t_NOTEQUAL  = r'<>'
t_MORETHANEQUAL  = r'>='
t_LESSTHANEQUAL  = r'<='
t_ISEQUALTO  = r'=='
t_OR = r'\|'
t_AND = r'\&'
t_CTEINT = r'[0-9][0-9]*'
t_CTEFLOAT = r'[0-9]+.[0-9]+'
t_CTESTRING = r'\"[a-zA-Z_0-9]*\"'
t_CTECHAR = r'\"[a-zA-Z_0-9]\"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

def p_programa(t):
    'programa : prog ID SEMICOLON vars funcs main bloque'

def p_prog(t):
    'prog : PROGRAM'
    # Global Scope
    FunctionDirectory.addFunction('global', None)
    FunctionStack.push('global')

def p_main(t):
    'main : MAIN'
    FunctionDirectory.addFunction(t[1], None)
    FunctionStack.push(t[1])

def p_condicion(t):
    'condicion : IF LPAREN expresion RPAREN bloque masbloque'

def p_bloque(t):
    'bloque : LBRACKET masestatuto RBRACKET'

def p_masbloque(t):
    '''masbloque : ELSE bloque
                 | empty'''

def p_ciclo(t):
    'ciclo : WHILE LPAREN expresion RPAREN bloque'

def p_escritura(t):
    'escritura : PRINT LPAREN listaprint RPAREN SEMICOLON'

def p_listaprint(t):
    '''listaprint : expresion masprint
                  | CTESTRING masprint'''

def p_masprint(t):
    '''masprint : COMMA listaprint
                | empty'''

def p_asignacion(t):
    '''asignacion : ID EQUALS expresion SEMICOLON
                  | ID LSQBRACKET RSQBRACKET EQUALS LSQBRACKET expresion comaexpresion RSQBRACKET SEMICOLON'''

def p_factor(t):
    '''factor : LPAREN expresion RPAREN
              | varcte
              | ID'''

def p_exp(t):
    'exp : termino masexp'

def p_masexp(t):
    '''masexp : PLUS exp
              | MINUS exp
              | empty'''

def p_comaexpresion(t):
    '''comaexpresion : COMMA expresion comaexpresion
                     | empty'''
            
def p_expresion(t):
    'expresion : expcomp masexpresion'

def p_masexpresion(t):
    '''masexpresion : AND expcomp
                    | OR expcomp
                    | empty'''

def p_termino(t):
    'termino : factor masterminos'

def p_masterminos(t):
    '''masterminos : TIMES exp
                   | DIVIDE exp
                   | empty'''

def p_expcomp(t):
    'expcomp : exp expcompcontinuo'

def p_expcompcontinuo(t):
    '''expcompcontinuo : MORETHAN exp
                       | LESSTHAN exp
                       | NOTEQUAL exp
                       | ISEQUALTO exp
                       | MORETHANEQUAL exp
                       | LESSTHANEQUAL exp
                       | empty'''

def p_estatuto(t):
    '''estatuto : asignacion
                | condicion
                | ciclo
                | escritura
                | vars'''

def p_masestatuto(t):
    '''masestatuto : estatuto masestatuto
                   | empty'''

def p_vars(t):
    '''vars : VAR tipo listaid SEMICOLON vars
            | empty'''
    
def p_listaid(t):
    'listaid : ID masid'
    FunctionDirectory.addVariable(FunctionStack.peek(),t[1],TypeStack.pop())

def p_masid(t):
    '''masid : COMMA listaid
             | empty'''
    if len(t) > 1 :
        TypeStack.push(TypeStack.peek())

def p_funcs(t):
    '''funcs : FUNCTION funcaux LPAREN args RPAREN bloque funcs
             | empty''' 

def p_funcaux(t):
    'funcaux : tipo ID'
    FunctionDirectory.addFunction(t[2], TypeStack.pop())
    FunctionStack.push(t[2])

def p_args(t):
    '''args : tipo ID masargs
            | empty'''
    FunctionDirectory.addVariable(FunctionStack.peek(),t[2],TypeStack.pop())
    
def p_masargs(t):
    '''masargs : COMMA args
               | empty'''

def p_tipo(t):
    '''tipo : INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING'''
    TypeStack.push(t[1])

def p_varcte(t):
    '''varcte : ID arr
              | CTEINT
              | CTEFLOAT
              | CTECHAR
              | CTESTRING
              | ctebool'''

def p_ctebool(t):
    '''ctebool : TRUE
               | FALSE'''

def p_arr(t):
    '''arr : LSQBRACKET RSQBRACKET
           | empty'''

def p_error(t):
    print("ERROR de sintaxis en: '%s'" % t.value)

def p_empty(t):
    'empty : '
    pass

import ply.yacc as yacc
parser = yacc.yacc()

# Main
print("Escribe el nombre del archivo con el codigo fuente o 'exit' para salir: ")
while True:
    try:
        fn = input('OpenRoonie > ')
        if fn == 'exit' :
            break
        file = open(fn, 'r')
        s = file.read()
        parser.parse(s)
        print("\nSi no hay mensajes de error, ¡Felicidades! El lexico, sintaxis y semantica de tu programa son correctos.\nEn caso contrario, verifica tu codigo.")
        FunctionDirectory.showDirectory();
        FunctionDirectory.resetDirectory();
    except EOFError:
        break
    except IOError:
        print("\nERROR IO. Verifica que el nombre del archivo sea el correcto.")
    print('')
