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
import Stack             as Stack
import FunctionDirectory as FunctionDirectory
import QuadrupleManager  as QuadrupleManager
import VirtualMachine    as VirtualMachine

# Directory de funciones, controlador de cuadruplos y maquina virtual
FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
QuadrupleManager  = QuadrupleManager.QuadrupleManager().Instance
VirtualMachine    = VirtualMachine.VirtualMachine().Instance

# Sintaxis y Semantica
DimsList       = []
ParamsList     = []
ArrayIDList    = []
ParamTypeList  = []
FCStack        = Stack.Stack()
TypeStack      = Stack.Stack()
FunctionStack  = Stack.Stack()
PilasDimensionadas = Stack.Stack()

# Generacion de Cuadruplos
POper   = Stack.Stack()
PilaO   = Stack.Stack()
PSaltos = Stack.Stack()

# Tokens: palabras reservadas.
reserved = {
   'if'       :  'IF',
   'else'     :  'ELSE',
   'var'      :  'VAR',
   'program'  :  'PROGRAM',
   'void'     :  'VOID',
   'int'      :  'INT',
   'float'    :  'FLOAT',
   'char'     :  'CHAR',
   'bool'     :  'BOOL',
   'True'     :  'TRUE',
   'False'    :  'FALSE',
   'string'   :  'STRING',
   'read'     :  'READ',
   'print'    :  'PRINT',
   'function' :  'FUNCTION',
   'main'     :  'MAIN',
   'while'    :  'WHILE',
   'return'   :  'RETURN'
}

# Lista de Tokens.
tokens = [
           'CTEINT',    'CTEFLOAT',   'CTESTRING',     'CTECHAR',
           'ID',        'EQUALS',     'ISEQUALTO',     'NOTEQUAL',
           'MORETHAN',  'LESSTHAN',   'MORETHANEQUAL', 'LESSTHANEQUAL',
           'SEMICOLON', 'COMMA',      'OR',            'AND',
           'PLUS',      'MINUS',      'TIMES',         'DIVIDE',
           'LPAREN',    'RPAREN',     'LBRACKET',      'RBRACKET',
           'LSQBRACKET','RSQBRACKET', 'COMMENT',       'CPPCOMMENT'
         ] + list(reserved.values())

# Definicion de Tokens con ERs.
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_EQUALS        = r'='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\{'
t_RBRACKET      = r'\}'
t_LSQBRACKET    = r'\['
t_RSQBRACKET    = r'\]'
t_SEMICOLON     = r';'
t_COMMA         = r','
t_MORETHAN      = r'>'
t_LESSTHAN      = r'<'
t_NOTEQUAL      = r'<>'
t_MORETHANEQUAL = r'>='
t_LESSTHANEQUAL = r'<='
t_ISEQUALTO     = r'=='
t_OR            = r'\|'
t_AND           = r'\&'
t_CTEINT        = r'-?[0-9][0-9]*'
t_CTEFLOAT      = r'-?[0-9]+\.[0-9]+'
t_CTESTRING     = r'\"([^\\\n]|(\\.))*?\"'
t_CTECHAR       = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

# Comment (C++-Style)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t

# IDs, con verificacion de que no sea una palabra reservada
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Caracteres ignorados
t_ignore = " \t"

# Salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error lexico    
def t_error(t):
    print("ERROR LEXICO. Caracter illegal: '%s'" % t.value[0])
    t.lexer.skip(1)

# Funciones utilizadas a lo largo de la compilacion
def resetRoonie():
    DimsList       = []
    ParamsList     = []
    ArrayIDList    = []
    ParamTypeList  = []
    POper          = Stack.Stack()
    PilaO          = Stack.Stack()
    PSaltos        = Stack.Stack()
    FCStack        = Stack.Stack()
    TypeStack      = Stack.Stack()
    FunctionStack  = Stack.Stack()
    FunctionDirectory.resetDirectory()
    QuadrupleManager.resetQuadruples()
    VirtualMachine.resetVirtualMachine()

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
    NoneParemeterQuadrupleOps = ['goto', 'goSub']
    OneParameterQuadrupleOps = NoneParemeterQuadrupleOps + ['print', 'read', 'gotoT', 'gotoF']
    if POper.peek() in ops:
        VirDir2 = PilaO.pop() if ops[0] not in OneParameterQuadrupleOps else None
        VirDir1 = PilaO.pop() if ops[0] not in NoneParemeterQuadrupleOps else None
        Operacion = POper.pop()
        Result = QuadrupleManager.addQuadruple(Operacion, VirDir1, VirDir2, FunctionStack.peek())
        if Result != None :
            # Genere el cuadruplo existosamente, su resultado es almacenado en PilaO.
            # (Un resultado temporal de alguna operacion aritmetica o logica)
            if Result != True and ops[0] not in OneParameterQuadrupleOps:
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
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

def p_programa(t):
    'programa : prog ID SEMICOLON vars eramain funcs main bloque'
    FunctionDirectory.resetLocalMemory()
    # fin de programa
    QuadrupleManager.addQuadruple('end', None, None, FunctionStack.peek())

def p_prog(t):
    'prog : PROGRAM'
    # Todo lo que se decalre afuera de las funciones es global.
    FunctionStack.push('global')

def p_eramain(t):
    'eramain : empty'
    # Comienza 'era' de main
    FunctionDirectory.addFunction('main', None, None)
    QuadrupleManager.addQuadruple('era', None, None, FunctionStack.peek())
    QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, FunctionDirectory.getFunctionIndex('main'))
    
    # Generar cuadruplo goto main
    addPOper('goSub')
    addQuadruple(['goSub'])
    PSaltos.push(QuadrupleManager.getQuadrupleListLength()-1)
    
def p_main(t):
    'main : MAIN'
    FunctionStack.push(t[1])
    FunctionDirectory.setFunctionStartQuadrupleIndex(t[1], QuadrupleManager.getQuadrupleListLength())
    QuadrupleManager.updateReturnReference(PSaltos.pop(), FunctionDirectory.getFunctionStartQuadrupleIndex(FunctionStack.peek()))

def p_condicion(t):
    'condicion : IF LPAREN expresion RPAREN gotoF estatutobloque masbloque'
    QuadrupleManager.updateReturnReference(PSaltos.pop(), QuadrupleManager.getQuadrupleListLength())

def p_estatutobloque(t):
    '''estatutobloque : estatuto
                      | bloque'''

def p_gotoF(t):
    'gotoF : empty'
    addPOper('gotoF')
    addQuadruple(['gotoF'])
    PSaltos.push(QuadrupleManager.getQuadrupleListLength()-1)

def p_bloque(t):
    'bloque : LBRACKET masestatuto RBRACKET'

def p_masbloque(t):
    '''masbloque : ELSE goto estatutobloque
                 | empty'''
    
def p_goto(t):
    'goto : empty'
    addPOper('goto')
    addQuadruple(['goto'])
    QuadrupleManager.updateReturnReference(PSaltos.pop(), QuadrupleManager.getQuadrupleListLength())
    PSaltos.push(QuadrupleManager.getQuadrupleListLength()-1)

def p_ciclo(t):
    'ciclo : while LPAREN expresion RPAREN gotoF estatutobloque goto'
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
    'listaprint : expresion masprint'
    addQuadruple(['print'])

def p_masprint(t):
    '''masprint : addQPP listaprint
                | empty'''

def p_addQPP(t):
    'addQPP : COMMA'
    addPOper('print')
    addQuadruple(['print'])
    
def p_asignacion(t):
    '''asignacion : ID EQUALS expresion SEMICOLON
                  | idarray LSQBRACKET dimsvar RSQBRACKET EQUALS expresion SEMICOLON'''
    # Si es una var normal
    if t[2] == '=':
        addIDPilaO(FunctionStack.peek(), t[1])

    # Si es una var vector    
    else:
        aux1 = PilaO.pop()
        aux2 = PilaO.pop()

        PilaO.push(aux1)
        PilaO.push(aux2)
        
        ArrayIDList.pop()
        for i in range(0, PilasDimensionadas.size()):
            PilasDimensionadas.pop()
            
    addPOper('=')
    addQuadruple(['='])

def p_factor(t):
    '''factor : leftparen expresion rightparen
              | varcte
              | varid
              | llamafunc'''

def p_leftparen(t):
    'leftparen : LPAREN'
    addPOper('Fake')

def p_rightparen(t):
    'rightparen : RPAREN'
    POper.pop()

def p_varid(t):
    '''varid : ID
             | idarray LSQBRACKET dimsvar RSQBRACKET'''
    if len(t) > 2:
        ArrayIDList.pop()
        for i in range(0, PilasDimensionadas.size()):
            PilasDimensionadas.pop()
    else:
        addIDPilaO(FunctionStack.peek(), t[1])
    
def p_idarray(t):
    'idarray : ID'
    ArrayIDList.append(t[1])
    
def p_dimsvar(t):
    'dimsvar : expdimvar masdimsvar'

def p_expdimvar(t):
    'expdimvar : expresion'
    # El resultado de la exp debe ser un entero
    if TypeStack.peek() == 'int':

        vID = ArrayIDList[len(ArrayIDList)-1]
        # Si la var es dimensionada
        if len(FunctionDirectory.getVariableDimSize(FunctionStack.peek(), vID)) > 0:

            if PilasDimensionadas.peek() == None:
                DIM = 1
                PilasDimensionadas.push([vID, DIM])
                POper.push('Fake')
        else :
            print("No es array\n")

        # Verificamos que el resultado de la exp este entre 0 y upperLimit
        DIM_ID = PilasDimensionadas.peek()[0]
        DIM    = PilasDimensionadas.peek()[1]
        
        listDIMsVar = FunctionDirectory.getVariableDimSize(FunctionStack.peek(), ArrayIDList[len(ArrayIDList)-1])
        upperLimit = listDIMsVar[DIM - 1]
        
        QuadrupleManager.addQuadruple('verify', PilaO.peek(), None, FunctionStack.peek())
        QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, upperLimit)

        Offset = FunctionDirectory.getVariableOffset(FunctionStack.peek(), DIM_ID)[DIM - 1]
        dirOffset = FunctionDirectory.addConstant(str(Offset), 'int') 
        PilaO.push(QuadrupleManager.addQuadruple('*', PilaO.pop(), dirOffset, FunctionStack.peek()))
            
        if DIM > 1 :
            PilaO.push(QuadrupleManager.addQuadruple('+', PilaO.pop(), PilaO.pop(), FunctionStack.peek()))

        auxPD = PilasDimensionadas.pop()
        auxPD[1] += 1
        PilasDimensionadas.push(auxPD)

        if len(listDIMsVar) == DIM:
            dirBase = FunctionDirectory.getVariableVirtualDirection(FunctionStack.peek(), DIM_ID)
            dirdirBase = FunctionDirectory.addConstant(str(dirBase), 'int')
            PilaO.push('*'+str(QuadrupleManager.addQuadruple('+', PilaO.pop(), dirdirBase, FunctionStack.peek())))
            POper.pop()

def p_masdimsvar(t):
    '''masdimsvar : COMMA dimsvar
                  | empty'''
  
def p_exp(t):
    'exp : termino masexp'
        
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
    '''expresion : expcomp masexpresion'''

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
    'termino : factor masterminos'

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
                | lectura
                | vars
                | llamafunc SEMICOLON
                | COMMENT
                | CPPCOMMENT'''

def p_lectura(t):
    'lectura : READ LPAREN ID RPAREN SEMICOLON'
    QuadrupleManager.addQuadruple('read', FunctionDirectory.getVariableVirtualDirection(FunctionStack.peek(), t[3]), None, FunctionStack.peek())

def p_llamafunc(t):
    'llamafunc : idfunc LPAREN funcargs RPAREN'
    FunctionStack.push(FCStack.peek())
    QuadrupleManager.addQuadruple('goSub', None, None, FunctionStack.peek())
    QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, FunctionDirectory.getFunctionStartQuadrupleIndex(FunctionStack.pop()))
    
    # Si la funcion llamada no es Void, igualar la variable temporal que la representa con el valor almacenado en el quad return 
    if FunctionDirectory.getFunctionType(FCStack.peek()) != 'void':
        QuadrupleManager.addQuadruple('=', FunctionDirectory.getVariableVirtualDirection('global', '_'+FCStack.peek()), PilaO.peek(), FunctionStack.peek())

    FCStack.pop()
    POper.pop()
    
def p_idfunc(t):
    'idfunc : ID'
    # Comienza 'era' de esta funcion
    FCStack.push(t[1])
    QuadrupleManager.addQuadruple('era', None, None, FCStack.peek())
    QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, FunctionDirectory.getFunctionIndex(FCStack.peek()))

    # Si la funcion llamada no es Void, agrego una temporal al contexto actual para almacenar su valor de retorno
    if FunctionDirectory.getFunctionType(FCStack.peek()) != 'void':
        PilaO.push(FunctionDirectory.addTemporalVariable(FunctionStack.peek(), None, FunctionDirectory.getFunctionType(FCStack.peek()), []))
    
    ParamTypeList.append(FunctionDirectory.getParameterTypeList(FCStack.peek()))
    for i in range(0, len(FunctionDirectory.getParameterTypeList(FCStack.peek()))):
        ParamsList.append(FunctionDirectory.getFunction(FCStack.peek())[3][i][2])
    addPOper('Fake')

def p_funcargs(t):
    '''funcargs : expresion listafuncargs checarparams
                | empty'''
    funcParamType = ParamTypeList.pop()

def p_listafuncargs(t):
    '''listafuncargs : COMMA expresion listafuncargs
                     | empty'''

def p_checarparams(t):
    'checarparams : empty'
    funcParamType = ParamTypeList[len(ParamTypeList)-1]
    for i in range(len(funcParamType)-1, -1, -1):
        if len(ParamsList) > 0 and PilaO.size() > 0:
            PilaO_Index      = PilaO.size()       - (i + 1)
            ParamsList_Index = len(funcParamType) - (i + 1)
            QuadrupleManager.addQuadruple('params', PilaO.items.pop(PilaO_Index), ParamsList[ParamsList_Index], FCStack.peek())
    del ParamsList[:]
 
def p_masestatuto(t):
    '''masestatuto : estatuto masestatuto
                   | empty'''

def p_vars(t):
    '''vars : VAR tipo listaid SEMICOLON vars 
            | empty'''
    
def p_listaid(t):
    'listaid : initvar masid'

def p_initvar(t):
    '''initvar : ID EQUALS expresion 
               | ID LSQBRACKET dims RSQBRACKET
               | ID '''
    if checkVoid():

        # Si estoy declarando un array
        if len(t) > 4:
            FunctionDirectory.addVariable(FunctionStack.peek(), t[1], TypeStack.peek(), DimsList)
            for i in range(0, len(DimsList)):
                DimsList.pop()
        
        # Si estoy declarando e inicializando
        elif len(t) > 3:
            FunctionDirectory.addVariable(FunctionStack.peek(), t[1], TypeStack.pop(), [])
            if checkVoid():
                QuadrupleManager.addQuadruple('=', PilaO.pop(), FunctionDirectory.getVariableVirtualDirection(FunctionStack.peek(), t[1]), FunctionStack.peek())
        
        # Si solo estoy declarando
        else:
            FunctionDirectory.addVariable(FunctionStack.peek(), t[1], TypeStack.peek(), [])

def p_dims(t):
    'dims : CTEINT masdims'
    DimsList.append(eval(t[1]))

def p_masdims(t):
    '''masdims : COMMA dims
               | empty'''

def p_masid(t):
    '''masid : COMMA listaid
             | empty'''

def p_funcs(t):
    '''funcs : FUNCTION funcaux LPAREN args masargs RPAREN bloquefunc funcs
             | FUNCTION funcaux LPAREN RPAREN bloquefunc funcs
             | empty'''

def p_bloquefunc(t):
    'bloquefunc : LBRACKET masestatuto retorno RBRACKET'

def p_retorno(t):
    '''retorno : RETURN expresion SEMICOLON
               | RETURN SEMICOLON '''
    # Funcion Void
    if FunctionDirectory.getFunctionType(FunctionStack.peek()) == 'void' and len(t) == 3:
        QuadrupleManager.addQuadruple('return', None, None, FunctionStack.peek())
        FunctionDirectory.resetLocalMemory()
        
    # Funcion que si retorna un valor
    elif FunctionDirectory.getFunctionType(FunctionStack.peek()) != 'void' and len(t) == 4:
        returnDir = FunctionDirectory.getVariableVirtualDirection('global', '_'+FunctionStack.peek())
        QuadrupleManager.addQuadruple('=', PilaO.pop(), returnDir, FunctionStack.peek())
        QuadrupleManager.addQuadruple('return', None, None, FunctionStack.peek())
        QuadrupleManager.updateReturnReference(QuadrupleManager.getQuadrupleListLength()-1, returnDir)      
        FunctionDirectory.resetLocalMemory()

    # Si es Void y me estan retornado un valor
    elif FunctionDirectory.getFunctionType(FunctionStack.peek()) == 'void' and len(t) == 4:
        print("ERROR SEMANTICA. Las funciones de tipo void no deben retornar ningun valor")

    # Si no es Void y no me dan valor de retorno
    elif FunctionDirectory.getFunctionType(FunctionStack.peek()) != 'void' and len(t) == 3:
        print("ERROR SEMANTICA. Las funciones de tipo", FunctionDirectory.getFunctionType(FunctionStack.peek()), "deben retornar un valor")
    
def p_funcaux(t):
    'funcaux : tipo ID'
    FunctionStack.push(t[2])
    FunctionDirectory.addFunction(FunctionStack.peek(), TypeStack.peek(), QuadrupleManager.getQuadrupleListLength())

    # Si la funcion no es Void, creo una variable global que me sirve como avail para el retorno de la funcion
    if FunctionDirectory.getFunctionType(FunctionStack.peek()) != 'void':
        FunctionDirectory.addVariable('global', '_'+FunctionStack.peek(), TypeStack.peek(), [])

def p_args(t):
    '''args : tipo ID 
            | empty'''
    if len(t) > 2 :
        if checkVoid():
            FunctionDirectory.addParameterType(FunctionStack.peek(), TypeStack.peek())
            FunctionDirectory.addVariable(FunctionStack.peek(), t[2], TypeStack.peek(), [])
    
def p_masargs(t):
    '''masargs : COMMA args masargs
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

print('\nTry: loadFile() or loadCode()')

def loadFile():
    resetRoonie()
    try:
        fn = input('Source Code File > ')
        file = open(fn+'.roonie', 'r')
        s = file.read()
        parser.parse(s)
        printDireAndQuads()

    except (EOFError, IOError):
        print("\nERROR IO. Verifica que el nombre del archivo sea el correcto.")
    except:
        print("\nERROR COMPILACION. No se pudo compilar tu programa, verifica los errores marcados anteriormente.")
        resetRoonie()
        return
    
def loadCode():
    resetRoonie()
    try:
        code = input('Source Code > ')
        parser.parse(code)
        printDireAndQuads()
        
    except:
        print("\nERROR COMPILACION. No se pudo compilar tu programa, verifica los errores marcados anteriormente.")
        resetRoonie()

def printDireAndQuads():
    # Prints
    print("\nCompilacion terminada.")
    FunctionDirectory.showDirectory()
    QuadrupleManager.showQuadruples()

def runLoadedCode():
    try:
        # Execution
        print('\n---Start-Execution---\n')
        VirtualMachine.run()
        print('\n----End-Execution----')

    except:
        print("\nERROR RUNTIME. No se pudo ejecutar tu programa, verifica los errores marcados anteriormente")
        # Resetear para el siguiente archivo
        resetRoonie()

def cleanConsole():
    print('\n' * 100)

def loadAll():
    while True:
        loadFile()
        runLoadedCode()
        print('')
