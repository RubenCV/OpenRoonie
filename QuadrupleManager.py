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

import Enums             as Enums
import SemanticCube      as SemanticCube
import MemoryManager     as MemoryManager
import FunctionDirectory as FunctionDirectory

class QuadrupleManagerClass:

    def __init__(self):
        # import objs
        self.Enums              = Enums.Enums().Instance
        self.SemanticCube       = SemanticCube.SemanticCube().Instance
        self.MemoryManager      = MemoryManager.MemoryManager().Instance
        self.FunctionDirectory  = FunctionDirectory.FunctionDirectory().Instance

        # Dict
        self.Operations         = self.Enums.Operations
        self.Functions          = self.Enums.FunctionsQuadruples

        # Reset
        self.resetQuadruples()

    def resetQuadruples(self):
        self.QuadrupleList = []
        return True

    def showQuadruples(self):
        print('')
        print('{0: <4}'.format('#'),
              '{0: <7}'.format('Name'),
              '{0: >21}'.format('Quadruple'))
        
        for i in range(0, len(self.QuadrupleList)):
            print('{0: <4}'.format(str(i)),
                  '{0: <7}'.format(str(list(self.Operations.keys())[list(self.Operations.values()).index(self.QuadrupleList[i][0])])), '[',
                  '{0: >3}'.format(str(self.QuadrupleList[i][0])),
                  '{0: >7}'.format(str(self.QuadrupleList[i][1])),
                  '{0: >7}'.format(str(self.QuadrupleList[i][2])),
                  '{0: >7}'.format(str(self.QuadrupleList[i][3])), ']')
        return True

    def addQuadruple(self, Op, VirDir1, VirDir2, FuncName):
        try:
            IndexOP = self.Operations[Op]
        except ValueError:
            print("\nERROR SINTAXIS / SEMANTICA. Operacion no reconocida: ", Op)
            return None

        if str(VirDir1).startswith('*'): Type1 = 'int'
        else: Type1 = self.MemoryManager.getEntryType(VirDir1) if VirDir1 != None else None

        if str(VirDir2).startswith('*'): Type2 = 'int'
        else: Type2 = self.MemoryManager.getEntryType(VirDir2) if VirDir2 != None else None
        
        return eval("self."+self.Functions[IndexOP])(Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName)

    # + - * / > < >= <= <> == | &
    def literalOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        ResultingType = self.SemanticCube.getResultingType(Type1, Type2, Op)
        if ResultingType != None :
            ResultVirDir =  self.FunctionDirectory.addTemporalVariable(FuncName, None, ResultingType, [])
            self.QuadrupleList.append([IndexOP, VirDir1, VirDir2, ResultVirDir])
            return ResultVirDir

    # Asignacion (A = b -> [= , b, None, A])
    def assignOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        ResultingType = self.SemanticCube.getResultingType(Type1, Type2, '=')
        if ResultingType != None :
            self.QuadrupleList.append([IndexOP, VirDir1, None, VirDir2])
            return True
        else:
            print("\nERROR SEMANTICA. Tipo de dato:", Type1,'no puede ser asignado a una variable de tipo:', Type2)
            return None
            
    # Print (print(A) -> [print , None, None, A])
    def printOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, VirDir1])
        return True
            
    # Read
    def readOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, VirDir1])
        return True
            
    # gotoT -> [gotoT, BoolVirDir, None, Pendiente]
    def gotoTOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        if (Type1 == 'bool'):
            self.QuadrupleList.append([IndexOP, VirDir1, None, None])
            return len(self.QuadrupleList)-1
        else:
            print("\nERROR SEMANTICA. La condicion en un if o un ciclo debe ser de tipo bool.")
            return None

    # gotoF -> [gotoF, BoolVirDir, None, Pendiente]
    def gotoFOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        if (Type1 == 'bool'):
            self.QuadrupleList.append([IndexOP, VirDir1, None, None])
            return len(self.QuadrupleList)-1
        else:
            print("\nERROR SEMANTICA. La condicion en un if o un ciclo debe ser de tipo bool.")
            return None

    # goto -> (goto, None, None, Pendiente)
    def gotoOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, None])
        return len(self.QuadrupleList)-1

    # goSub -> (goto, None, None, #CuadruploDeLaSubrutina)
    def goSubOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, None])
        return len(self.QuadrupleList)-1

    # Params (A = b -> [= , b, None, A])
    def paramsOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        ResultingType = self.SemanticCube.getResultingType(Type1, Type2, '=')
        if ResultingType != None :
            self.QuadrupleList.append([IndexOP, VirDir1, None, VirDir2])
            return True
        else:
            print("\nERROR SEMANTICA. Tipo de dato:", Type1,'no puede ser asignado a una variable de tipo:', Type2)
            return None
        
    # return
    def returnOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, None])
        return True

    # era
    def eraOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, None])
        return True

    # verify
    def verifyOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, VirDir1, 0, None])
        return True
        
    # end
    def endOp(self, Op, IndexOP, VirDir1, VirDir2, Type1, Type2, FuncName):
        self.QuadrupleList.append([IndexOP, None, None, None])
        return True

    def updateReturnReference(self, index, quadIndex):
        if index < len(self.QuadrupleList):
            Op = list(self.Operations.keys())[list(self.Operations.values()).index(self.QuadrupleList[index][0])]
            if Op in ['gotoT', 'gotoF', 'goto', 'goSub', 'era', 'return', 'verify']:
                 self.QuadrupleList[index][3] = quadIndex;
                 return True
            else:
                print("\nERROR. El cuadruplo que intentas modificar no es un gotoX.")
                return None
        else:
            print("\nERROR. Indice de Cuadruplo fuera de los limites.")
            return None

    def getQuadrupleListLength(self):
        return len(self.QuadrupleList)


class QuadrupleManager:
     Instance = QuadrupleManagerClass()
     
     def __init__(self):
          pass
