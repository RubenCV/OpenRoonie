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
import Stack             as Stack
import MemoryManager     as MemoryManager
import FunctionDirectory as FunctionDirectory
import QuadrupleManager  as QuadrupleManager

from copy import deepcopy

class VirtualMachineClass:

     def __init__(self):
          self.Enums             = Enums.Enums().Instance
          self.MemoryManager     = MemoryManager.MemoryManager().Instance
          self.QuadrupleManager  = QuadrupleManager.QuadrupleManager().Instance
          self.FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
          
          self.Operations        = self.Enums.Operations
          self.Functions         = self.Enums.FunctionsVirtualMachine
          
          self.resetVirtualMachine()

     def resetVirtualMachine(self):
          self.asigningParams     = False
          self.actualQuadruple    = []
          self.instructionPointer = 0
          self.iPS                = Stack.Stack()
          self.contextStack       = Stack.Stack()
          self.localTypeCounters  = Stack.Stack()
          return True

     def updateActualQuadruple(self):
          self.actualQuadruple = self.QuadrupleManager.QuadrupleList[self.instructionPointer]
          self.Op = list(self.Operations.keys())[list(self.Operations.values()).index(self.actualQuadruple[0])]
          
          self.V1 = self.actualQuadruple[1]
          self.V2 = self.actualQuadruple[2]
          self.R  = self.actualQuadruple[3]

          virDirs = [self.V1, self.V2, self.R]
          for i in range(0, 3):
               strVD = str(virDirs[i])
               if strVD.startswith('*'):
                    virDirs[i] = self.MemoryManager.getEntryValue(eval(strVD[1:]))
                    
          self.V1, self.V2, self.R = virDirs
          return True

     def translateVirtualToAbsolute(self, virDir):
          absDir = virDir;
          if self.asigningParams == True:
               actual = self.localTypeCounters.pop()    
          if virDir >= self.MemoryManager.getLocalStart():
               actualCounters = self.localTypeCounters.peek()
               virDirType = self.MemoryManager.getEntryTypeId(virDir)
               offSet = virDir - self.MemoryManager.getInitialIndexType(virDirType)
               absDir = actualCounters[virDirType] + offSet
          if self.asigningParams == True:
               self.localTypeCounters.push(actual)
          return absDir

     def addToCountersStack(self):
          countersList = self.MemoryManager.getLocalIndexList()
          counterList_DP = deepcopy(countersList)
          self.localTypeCounters.push(counterList_DP)
          return True

     def deleteLocalVars(self):
          oldCounters = self.localTypeCounters.pop()
          newCounters = self.MemoryManager.getLocalIndexList()
          self.MemoryManager.deleteVarsByBounds(oldCounters, newCounters)
          return True

     def addToContextStack(self, idFunc):
          functionRow = self.FunctionDirectory.functionRow[idFunc]
          functionRow_DP = deepcopy(functionRow)
          self.contextStack.push(functionRow_DP)
          return True
          
     def loadFunction(self):
          funcVars = self.contextStack.peek()[3]
          for i in range(0,  len(funcVars)):
               self.MemoryManager.addEntry(2, funcVars[i][1], None)
          return True
           
     def run(self):
          self.updateActualQuadruple()
          while (self.Op != 'end'):
               
               IndexOP = self.Operations[self.Op]
               eval("self."+self.Functions[IndexOP])()
               
               self.instructionPointer += 1
               self.updateActualQuadruple()
          
          self.endOp()
          return True

     def literalOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          V2_ABS = self.translateVirtualToAbsolute(self.V2)
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          result = eval(str(self.MemoryManager.getEntryValue(V1_ABS)) + self.Op + str(self.MemoryManager.getEntryValue(V2_ABS)))
          self.MemoryManager.setEntryValue(R_ABS, result)

     def divisionOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          V2_ABS = self.translateVirtualToAbsolute(self.V2)
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          
          resultType = self.MemoryManager.getEntryType(R_ABS)
          if   resultType == 'int'   : division = '//'
          elif resultType == 'float' : division = '/'

          result = eval(str(self.MemoryManager.getEntryValue(V1_ABS)) + division + str(self.MemoryManager.getEntryValue(V2_ABS)))
          self.MemoryManager.setEntryValue(R_ABS, result)

     def notEqualsOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          V2_ABS = self.translateVirtualToAbsolute(self.V2)
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          result = self.MemoryManager.getEntryValue(V1_ABS) != self.MemoryManager.getEntryValue(V2_ABS)
          self.MemoryManager.setEntryValue(R_ABS, result)

     def orOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          V2_ABS = self.translateVirtualToAbsolute(self.V2)
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          result = self.MemoryManager.getEntryValue(V1_ABS) or self.MemoryManager.getEntryValue(V2_ABS)
          self.MemoryManager.setEntryValue(R_ABS, result)
          
     def andOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          V2_ABS = self.translateVirtualToAbsolute(self.V2)
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          result = self.MemoryManager.getEntryValue(V1_ABS) and self.MemoryManager.getEntryValue(V2_ABS)
          self.MemoryManager.setEntryValue(R_ABS, result)

     def assignOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          R_ABS  = self.translateVirtualToAbsolute(self.R) 
          result = self.MemoryManager.getEntryValue(V1_ABS)
          self.MemoryManager.setEntryValue(R_ABS, result)

     def printOp(self):
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          result = self.MemoryManager.getEntryValue(R_ABS)
          print(result, end = "", flush = True)

     def readOp(self):
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          varName = self.FunctionDirectory.getVariableByVirtualDirection(self.contextStack.peek()[0], self.R)
          result = input(varName + " = ")
          self.MemoryManager.setEntryValue(R_ABS, result)
          
     def gotoTOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          condition = self.MemoryManager.getEntryValue(V1_ABS)                  
          if condition:
               self.instructionPointer = self.R - 1
               
     def gotoFOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          condition = self.MemoryManager.getEntryValue(V1_ABS)
          if not condition:
               self.instructionPointer = self.R - 1

     def gotoOp(self):
          self.instructionPointer = self.R - 1

     def goSubOp(self):
          self.asigningParams = False
          self.iPS.push(self.instructionPointer)
          self.instructionPointer = self.R - 1

     def paramsOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          self.asigningParams = False                    
          R_ABS  = self.translateVirtualToAbsolute(self.R)
          self.asigningParams = True
          result = self.MemoryManager.getEntryValue(V1_ABS)
          self.MemoryManager.setEntryValue(R_ABS, result)

     def returnOp(self):
          if self.R != None:
               R_ABS  = self.translateVirtualToAbsolute(self.R)
               result = self.MemoryManager.getEntryValue(R_ABS)
          self.deleteLocalVars()
          self.instructionPointer = self.iPS.pop()
          self.contextStack.pop()
          
     def eraOp(self):
          self.addToContextStack(self.R)
          self.addToCountersStack()
          self.loadFunction()
          self.asigningParams = True

     def verifyOp(self):
          V1_ABS = self.translateVirtualToAbsolute(self.V1)
          Num    = self.MemoryManager.getEntryValue(V1_ABS)
          LimI   = self.V2
          LimS   = self.R
      
          if Num < LimI or Num >= LimS:
               print("ERROR. Array out of bounds.")
          
     def endOp(self):
          pass
          self.MemoryManager.resetMemory()
          self.resetVirtualMachine()

class VirtualMachine:
     Instance = VirtualMachineClass()
     
     def __init__(self):
          pass
