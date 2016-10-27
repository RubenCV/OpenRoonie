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
from copy import deepcopy

# Directory de funciones y controlador de cuadruplos.
FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
QuadrupleManager  = QuadrupleManager.QuadrupleManager().Instance

# Sintaxis y Semantica basica
TypeStack      = Stack.Stack()
FunctionStack  = Stack.Stack()
ParamTypeList  = []

# Generacion de Cuadruplos y Semantica
PSaltos = Stack.Stack()
POper   = Stack.Stack()
PilaO   = Stack.Stack()

# Funciones necesarias para la generacion de Cuadruplos
def addCtePilaO(cte, tipo):
    PilaO.push(FunctionDirectory.addConstant(cte, tipo))
    TypeStack.push(tipo)
    return True

def addIDPilaO(nombreFunc, nombreVar):
    PilaO.push(FunctionDirectory.getVariableVirtualDirection(nombreFunc, nombreVar))
    return True

def addPOper(op):
    POper.push(op)
    return True

def addQuadruple(ops):
    NoneParemeterQuadrupleOps = ['goto']
    OneParameterQuadrupleOps = NoneParemeterQuadrupleOps + ['print', 'read', 'gotoT', 'gotoF']
    if POper.peek() in ops:
        VirDir2 = PilaO.pop() if ops[0] not in OneParameterQuadrupleOps else None
        VirDir1 = PilaO.pop() if ops[0] not in NoneParemeterQuadrupleOps else None
        Operacion = POper.pop()
        Result = QuadrupleManager.addQuadruple(Operacion, VirDir1, VirDir2)
        if Result != None :
            # Genere el cuadruplo existosamente, su resultado es almacenado en PilaO.
            # (Un resultado temporal de alguna operacion aritmetica o logica)
            if Result != True :
                PilaO.push(Result)
                return True
            # Genere el cuadruplo exitosamente, y su resultado no es necesario almacenarlo en PilaO.
            else:
                return True
        # Algo sucedio que me impidio crear el cuadruplo, la clase 'QuadrupleManager' me dibio tirar un mensaje de error mas detallado.
        else :
            print("\nERROR. No se pudo generar el cuadruplo con operacion:", Operacion)
            return None
    # Aun no genero el cuadruplo porque sigo pendiente a mas ops.
    else:
        return False

def checkVoid():
    if TypeStack.peek() == 'void':
        print("ERROR SEMANTICA. El tipo de dato 'void' solo se puede utilizar en declaracion de funciones.")
        return False
    return True

# Tokens: palabras reservadas.
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'var' : 'VAR',
   'program' : 'PROGRAM',
   'void' : 'VOID',
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
   'return' : 'RETURN',
}

# Lista de Tokens.
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

# Definicion de Tokens con ERs.
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
    
    # Generar cuadruplo goto main
    addPOper('goto')
    addQuadruple(['goto'])
    PSaltos.push(0)

def p_main(t):
    'main : MAIN'
    FunctionDirectory.addFunction(t[1], None, QuadrupleManager.getQuadrupleListLength())
    FunctionStack.push(t[1])

    # Updatear cuadruplo 0 -> a CuadruploActual+1
    QuadrupleManager.updateReturnReference(PSaltos.pop(), FunctionDirectory.getFunctionStartQuadrupleIndex(t[1]))

def p_condicion(t):
    'condicion : IF LPAREN expresion RPAREN gotoF bloque masbloque'
    QuadrupleManager.updateReturnReference(PSaltos.pop(), QuadrupleManager.getQuadrupleListLength())

def p_gotoF(t):
    'gotoF : empty'
    addPOper('gotoF')
    addQuadruple(['gotoF'])
    PSaltos.push(QuadrupleManager.getQuadrupleListLength()-1)


def p_bloque(t):
    'bloque : LBRACKET masestatuto RBRACKET'

def p_masbloque(t):
    '''masbloque : ELSE goto bloque
                 | empty'''
def p_goto(t):
    'goto : empty'
    addPOper('goto')
    addQuadruple(['goto'])
    QuadrupleManager.updateReturnReference(PSaltos.pop(), QuadrupleManager.getQuadrupleListLength())
    PSaltos.push(QuadrupleManager.getQuadrupleListLength()-1)

def p_ciclo(t):
    'ciclo : while LPAREN expresion RPAREN gotoF bloque goto'
    PSaltos.pop()
    QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, PSaltos.pop())

def p_while(t):
    'while : WHILE'
    PSaltos.push(QuadrupleManager.getQuadrupleListLength())

def p_escritura(t):
    'escritura : print LPAREN listaprint RPAREN SEMICOLON'

def p_print(t):
    'print : PRINT'
    addPOper('print')

def p_listaprint(t):
    '''listaprint : expresion masprint
                  | ctestring masprint'''
    addQuadruple(['print'])

def p_masprint(t):
    '''masprint : addQPP listaprint
                | empty'''

def p_addQPP(t):
    'addQPP : COMMA'
    addQuadruple(['print'])
    addPOper('print')

def p_asignacion(t):
    '''asignacion : ID EQUALS expresion SEMICOLON
                  | ID LSQBRACKET RSQBRACKET EQUALS LSQBRACKET expresion comaexpresion RSQBRACKET SEMICOLON
                  | ID EQUALS llamafunc'''
    addIDPilaO(FunctionStack.peek(), t[1])
    addPOper('=')
    addQuadruple(['='])

def p_factor(t):
    '''factor : leftparen expresion rightparen
              | varcte
              | varid'''

def p_leftparen(t):
    'leftparen : LPAREN'
    addPOper('Fake')

def p_rightparen(t):
    'rightparen : RPAREN'
    POper.pop()

def p_varid(t):
    'varid : ID arr'
    addIDPilaO(FunctionStack.peek(), t[1])
    
def p_arr(t):
    '''arr : LSQBRACKET RSQBRACKET
           | empty'''
    
def p_exp(t):
    'exp : termino masexp' # masexp <-> addquadrupleplusminus
        
def p_masexp(t):
    '''masexp : addQPPM exp
              | empty'''
    addQuadruple(['+', '-'])

def p_addQPPM(t):
    '''addQPPM : PLUS 
               | MINUS '''
    addQuadruple(['+', '-'])
    addPOper(t[1])
    
def p_comaexpresion(t):
    '''comaexpresion : COMMA expresion comaexpresion
                     | empty'''
            
def p_expresion(t):
    'expresion : expcomp masexpresion'

def p_addQPAO(t):
    '''addQPAO : AND
               | OR'''
    addQuadruple(['&', '|'])
    addPOper(t[1])

def p_masexpresion(t):
    '''masexpresion : addQPAO expresion
                    | empty'''
    addQuadruple(['&', '|'])

def p_termino(t):
    'termino : factor masterminos' # masterminos <-> addquadrupletimesdivide

def p_addQTD(t):
    '''addQTD : TIMES 
              | DIVIDE '''
    addQuadruple(['*', '/'])
    addPOper(t[1])

def p_masterminos(t):
    '''masterminos : addQTD termino
                   | empty'''
    addQuadruple(['*', '/'])

def p_expcomp(t):
    'expcomp : exp expcompcontinuo'

def p_addQPComp(t):
    '''addQPComp : MORETHAN
                 | LESSTHAN
                 | NOTEQUAL
                 | ISEQUALTO
                 | MORETHANEQUAL
                 | LESSTHANEQUAL'''
    addQuadruple(['<', '>', '<>', '==','<=', '>='])
    addPOper(t[1])

def p_expcompcontinuo(t):
    '''expcompcontinuo : addQPComp expcomp
                       | empty'''
    addQuadruple(['<', '>', '<>', '==','<=', '>='])

def p_estatuto(t):
    '''estatuto : asignacion
                | condicion
                | ciclo
                | escritura
                | vars
                | retorno
                | llamafunc'''

def p_llamafunc(t):
    'llamafunc : idfunc LPAREN funcargs RPAREN SEMICOLON'

def p_idfunc(t):
    'idfunc : ID'
    ParamTypeList.append(deepcopy(FunctionDirectory.getParameterTypeList(t[1])))

def p_funcargs(t):
    '''funcargs : expresion listafuncargs
                | empty'''

def p_listafuncargs(t):
    '''listafuncargs : COMMA expresion listafuncargs checarparams
                     | empty'''

def p_checarparams(t):
    'checarparams : empty'
    actualParamType = ParamTypeList[len(ParamTypeList)-1]
    for x in range(0, len(actualParamType)):
        recentType = TypeStack.pop()
        if actualParamType[x] == recentType:
            print('paso:', recentType)
        else:
            print('ERROR. Tipo de argumentos invalidos:', actualParamType[x], recentType)
    
        
def p_retorno(t):
    '''retorno : RETURN exp SEMICOLON
               | RETURN SEMICOLON '''

def p_masestatuto(t):
    '''masestatuto : estatuto masestatuto
                   | empty'''

def p_vars(t):
    '''vars : VAR tipo listaid SEMICOLON vars
            | empty'''
    
def p_listaid(t):
    'listaid : ID masid'
    if checkVoid():
        FunctionDirectory.addVariable(FunctionStack.peek(),t[1],TypeStack.peek())
        TypeStack.peek()

def p_masid(t):
    '''masid : COMMA listaid
             | empty'''

def p_funcs(t):
    '''funcs : FUNCTION funcaux LPAREN args RPAREN bloque funcs
             | empty'''


def p_funcaux(t):
    'funcaux : tipo ID'
    FunctionDirectory.addFunction(t[2], TypeStack.peek(), QuadrupleManager.getQuadrupleListLength())
    FunctionStack.push(t[2])

def p_args(t):
    '''args : tipo ID masargs
            | empty'''
    if checkVoid():
        FunctionDirectory.addParameterType(FunctionStack.peek(), TypeStack.peek())
        FunctionDirectory.addVariable(FunctionStack.peek(),t[2],TypeStack.peek())
    
def p_masargs(t):
    '''masargs : COMMA args
               | empty'''

def p_tipo(t):
    '''tipo : INT
            | FLOAT
            | CHAR
            | BOOL
            | STRING
            | VOID'''
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
    addCtePilaO(t[1], "int")

def p_ctefloat(t):
    '''ctefloat : CTEFLOAT'''
    addCtePilaO(t[1], "float")

def p_ctechar(t):
    '''ctechar : CTECHAR'''
    addCtePilaO(t[1], "char")

def p_ctestring(t):
    '''ctestring : CTESTRING'''
    addCtePilaO(t[1], "string")

def p_ctebool(t):
    '''ctebool : TRUE
               | FALSE'''
    addCtePilaO(t[1], "bool")
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
        QuadrupleManager.showQuadruples()

        # Resetear para el siguiente archivo
        FunctionDirectory.resetDirectory()
        QuadrupleManager.resetQuadruples()
    
    except EOFError:
        break
    except IOError:
        print("\nERROR IO. Verifica que el nombre del archivo sea el correcto.")
    print('')
