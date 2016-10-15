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
import QuadrupleManager as QuadrupleManager

TypeStack = Stack.Stack()
FunctionStack = Stack.Stack()
FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
QuadrupleManager = QuadrupleManager.QuadrupleManager().Instance

# Semantica y Generacion de Cuadruplos
POper = Stack.Stack()
PilaO = Stack.Stack()
def AgregarPilasCtes(t, tipo):
    PilaO.push(FunctionDirectory.addConstant(t, tipo))

def AgregarPilasID(function, nombre):
    DirVir = FunctionDirectory.getVariableVirtualDirection(function, nombre)
    PilaO.push(DirVir)

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
t_CTESTRING = r'\"([^\\\n]|(\\.))*?\"'
t_CTECHAR = r'(L)?\'([^\\\n]|(\\.))*?\''

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
    print("ERROR LEXICO. Caracter illegal: '%s'" % t.value[0])
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
    # Todo lo que se decalre afuera de las funciones es global.
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
                  | ctestring masprint'''

def p_masprint(t):
    '''masprint : COMMA listaprint
                | empty'''

def p_asignacion(t):
    '''asignacion : ID EQUALS expresion SEMICOLON
                  | ID LSQBRACKET RSQBRACKET EQUALS LSQBRACKET expresion comaexpresion RSQBRACKET SEMICOLON'''

def p_factor(t):
    '''factor : leftparen expresion rightparen
              | varcte
              | varid'''

def p_leftparen(t):
    'leftparen : LPAREN'
    POper.push('Fake')

def p_rightparen(t):
    'rightparen : RPAREN'
    POper.pop()

def p_varid(t):
    'varid : ID arr'
    AgregarPilasID(FunctionStack.peek(), t[1])
    
def p_arr(t):
    '''arr : LSQBRACKET RSQBRACKET
           | empty'''
    
def p_exp(t):
    'exp : termino masexp addquadrupleplusminus' # masexp <-> addquadrupleplusminus

def p_addquadrupleplusminus(t):
    'addquadrupleplusminus : empty'
    if POper.peek() in ['+', '-']:
        VirDir2 = PilaO.pop()
        VirDir1 = PilaO.pop()
        Operacion = POper.pop()
        PilaO.push(QuadrupleManager.AddQuadruple(Operacion, VirDir1, VirDir2))
        
def p_masexp(t):
    '''masexp : PLUS exp
              | MINUS exp
              | empty'''
    if len(t) > 2:
        POper.push(t[1])

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
    'termino : factor masterminos addquadrupletimesdivide' # masterminos <-> addquadrupletimesdivide

def p_addquadrupletimesdivide(t):
    'addquadrupletimesdivide : empty'
    if POper.peek() in ['*', '/']:
        VirDir2 = PilaO.pop()
        VirDir1 = PilaO.pop()
        Operacion = POper.pop()
        PilaO.push(QuadrupleManager.AddQuadruple(Operacion, VirDir1, VirDir2))

def p_masterminos(t):
    '''masterminos : TIMES termino
                   | DIVIDE termino
                   | empty'''
    if len(t) > 2:
        POper.push(t[1])

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

# Identifiar tipo de constantes y agregarlas a memoria.
def p_varcte(t):
    '''varcte : cteint
              | ctefloat
              | ctechar
              | ctestring
              | ctebool'''

def p_cteint(t):
    '''cteint : CTEINT'''
    AgregarPilasCtes(t[1], "int")

def p_ctefloat(t):
    '''ctefloat : CTEFLOAT'''
    AgregarPilasCtes(t[1], "float")

def p_ctechar(t):
    '''ctechar : CTECHAR'''
    AgregarPilasCtes(t[1], "char")

def p_ctestring(t):
    '''ctestring : CTESTRING'''
    AgregarPilasCtes(t[1], "string")

def p_ctebool(t):
    '''ctebool : TRUE
               | FALSE'''
    AgregarPilasCtes(t[1], "bool")
# Termino de identificar tipo de constantes y agregarlas a memoria.
    
def p_error(t):
    print("\nERROR SINTAXIS. Token: '%s'" % t.value)

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
        print("\nCompilacion terminada.")

        # Imprimir
        FunctionDirectory.showDirectory()
        QuadrupleManager.ShowQuadruples()

        # Resetear para el siguiente archivo
        FunctionDirectory.resetDirectory()
        QuadrupleManager.ResetQuadruples()
    
    except EOFError:
        break
    except IOError:
        print("\nERROR IO. Verifica que el nombre del archivo sea el correcto.")
    print('')
