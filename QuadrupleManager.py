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
        self.Operations = self.SemanticCube.Operations + ['=', 'print', 'read','gotoT', 'gotoF', 'goto']
        self.ResetQuadruples()

    def ResetQuadruples(self):
        self.QuadrupleList = []
        return True

    def ShowQuadruples(self):
        print("\nCuadruplos: ")
        for Quadruple in self.QuadrupleList:
            print(Quadruple)
        return True

    def AddQuadruple(self, Op, VirDir1, VirDir2):
        try:
            IndexOP = self.Operations.index(Op)
        except ValueError:
            print("\nERROR. Operacion no reconocida: ", Op)
            return None
        
        Type1 = self.MemoryManager.GetEntryType(VirDir1) if VirDir1 != None else None
        Type2 = self.MemoryManager.GetEntryType(VirDir2) if VirDir2 != None else None

        # Operacion Artimetica / Logica
        if IndexOP < len(self.SemanticCube.Operations):
            ResultingType = self.SemanticCube.GetResultingType(Type1, Type2, Op)

            if ResultingType != None :
                ResultVirDir =  self.FunctionDirectory.addTemporalVariable(None, ResultingType)
                self.QuadrupleList.append([IndexOP, VirDir1, VirDir2, ResultVirDir])
                return ResultVirDir

        # Asignacion (A = b -> [= , b, None, A])
        elif IndexOP == len(self.SemanticCube.Operations):
            if Type1 == Type2:
                self.QuadrupleList.append([IndexOP, VirDir1, None, VirDir2])
                return True
            else:
                print("\nERROR. Tipo de dato:", Type1,'no puede ser asignado a una variable de tipo:', Type2)
                return None
            
        # Print (print(A) -> [print , None, None, A])
        elif IndexOP == len(self.SemanticCube.Operations)+1:
            self.QuadrupleList.append([IndexOP, None, None, VirDir1])
            return True
            
        # Read
        elif IndexOP == len(self.SemanticCube.Operations)+2:
            return None
            
        # gotoT or gotoF
        elif (IndexOP == len(self.SemanticCube.Operations)+3) or (IndexOP == len(self.SemanticCube.Operations)+4):
            if (Type1 == 'bool'):
                self.QuadrupleList.append([IndexOP, VirDir1, None, None])
                return len(self.QuadrupleList)-1

        # goto
        elif IndexOP == len(self.SemanticCube.Operations)+5:
            self.QuadrupleList.append([IndexOP, None, None, None])
            return len(self.QuadrupleList)-1

    def UpdateReturnReference(self, index, quadIndex):
        if index < len(self.QuadrupleList):
            if self.QuadrupleList[index][0] in [15, 16, 17]:
                 self.QuadrupleList[index][3] = quadIndex;
                 return True
            else:
                print("\nERROR. El cuadruplo que intentas modificar no es un gotoX.")
                return None
        else:
            print("\nERROR. Index out of bounds.")
            return None

    def GetQuadrupleLength(self):
        return len(self.QuadrupleList)


class QuadrupleManager:
     Instance = QuadrupleManagerClass()
     
     def __init__(self):
          pass
