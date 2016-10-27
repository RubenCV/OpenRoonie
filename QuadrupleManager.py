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

import SemanticCube as SemanticCube
import MemoryManager as MemoryManager
import FunctionDirectory as FunctionDirectory

class QuadrupleManagerClass:

    def __init__(self):
        self.SemanticCube = SemanticCube.SemanticCube().Instance
        self.MemoryManager = MemoryManager.MemoryManager().Instance
        self.FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
        self.Operations = self.SemanticCube.Operations + ['=', 'print', 'read','gotoT', 'gotoF', 'goto', 'params', 'return']
        self.resetQuadruples()

    def resetQuadruples(self):
        self.QuadrupleList = []
        return True

    def showQuadruples(self):
        print("\nQuadruples: ")
        for Quadruple in self.QuadrupleList:
            print(Quadruple)
        return True

    def addQuadruple(self, Op, VirDir1, VirDir2):
        try:
            IndexOP = self.Operations.index(Op)
        except ValueError:
            print("\nERROR SINTAXIS / SEMANTICA. Operacion no reconocida: ", Op)
            return None
        
        Type1 = self.MemoryManager.getEntryType(VirDir1) if VirDir1 != None else None
        Type2 = self.MemoryManager.getEntryType(VirDir2) if VirDir2 != None else None

        # Operacion Artimetica / Logica
        if IndexOP < len(self.SemanticCube.Operations):
            ResultingType = self.SemanticCube.getResultingType(Type1, Type2, Op)

            if ResultingType != None :
                ResultVirDir =  self.FunctionDirectory.addTemporalVariable(None, ResultingType)
                self.QuadrupleList.append([IndexOP, VirDir1, VirDir2, ResultVirDir])
                return ResultVirDir

        # Asignacion (A = b -> [= , b, None, A])
        elif Op == '=':
            if Type1 == Type2:
                self.QuadrupleList.append([IndexOP, VirDir1, None, VirDir2])
                return True
            else:
                print("\nERROR SEMANTICA. Tipo de dato:", Type1,'no puede ser asignado a una variable de tipo:', Type2)
                return None
            
        # Print (print(A) -> [print , None, None, A])
        elif Op == 'print':
            self.QuadrupleList.append([IndexOP, None, None, VirDir1])
            return True
            
        # Read
        elif Op == 'read':
            return None
            
        # gotoT or gotoF -> (gotoX, BoolVirDir, None, Pendiente)
        elif Op in ['gotoT', 'gotoF']:
            if (Type1 == 'bool'):
                self.QuadrupleList.append([IndexOP, VirDir1, None, None])
                return len(self.QuadrupleList)-1
            else:
                print("\nERROR SEMANTICA. La condicion en un if o un ciclo debe ser de tipo bool.")
                return None

        # goto -> (goto, None, None, Pendiente)
        elif Op == 'goto':
            self.QuadrupleList.append([IndexOP, None, None, None])
            return len(self.QuadrupleList)-1

        elif Op == 'params':
            if Type1 == Type2:
                self.QuadrupleList.append([IndexOP, VirDir1, None, VirDir2])
                return True
            else:
                print("\nERROR SEMANTICA. Tipo de dato:", Type1,'no puede ser asignado a una variable de tipo:', Type2)
                return None

    def updateReturnReference(self, index, quadIndex):
        if index < len(self.QuadrupleList):
            Op = self.Operations[self.QuadrupleList[index][0]]
            if Op in ['gotoT', 'gotoF', 'goto']:
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
