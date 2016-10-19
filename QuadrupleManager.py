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
        self.Operations = self.SemanticCube.Operations + ['=', 'print', 'gotoT', 'gotoF', 'goto']
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

        Type1 = self.MemoryManager.GetEntryType(VirDir1)
        Type2 = self.MemoryManager.GetEntryType(VirDir2)

        # Operacion Artimetica / Logica
        if IndexOP < len(self.SemanticCube.Operations):
            ResultingType = self.SemanticCube.GetResultingType(Type1, Type2, Op)

            if ResultingType != None :
                ResultVirDir =  self.FunctionDirectory.addTemporalVariable(None, ResultingType)
                self.QuadrupleList.append([IndexOP, VirDir1, VirDir2, ResultVirDir])
                return ResultVirDir

        # Condicion / Ciclo / Saltos / Print / Read / etc
        else:
            return None

class QuadrupleManager:
     Instance = QuadrupleManagerClass()
     
     def __init__(self):
          pass
