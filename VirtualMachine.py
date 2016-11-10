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


import Stack             as Stack
import MemoryManager     as MemoryManager
import FunctionDirectory as FunctionDirectory
import QuadrupleManager  as QuadrupleManager
import SemanticCube      as SemanticCube

from copy import deepcopy

class VirtualMachineClass:

     def __init__(self):
          self.FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
          self.QuadrupleManager  = QuadrupleManager.QuadrupleManager().Instance
          self.MemoryManager     = MemoryManager.MemoryManager().Instance
          self.SemanticCube      = SemanticCube.SemanticCube().Instance

          self.Operations = self.QuadrupleManager.Operations

          self.actualQuadruple = []

          self.instructionPointer = 0
          self.iPS = Stack.Stack()

          self.contextStack      = Stack.Stack()
          self.localTypeCounters = Stack.Stack()

          self.returnValues      = Stack.Stack()
          

     def updateActualQuadruple(self):
          self.actualQuadruple = self.QuadrupleManager.QuadrupleList[self.instructionPointer]
          self.Op = self.Operations[self.actualQuadruple[0]]
          self.V1 = self.actualQuadruple[1]
          self.V2 = self.actualQuadruple[2]
          self.R  = self.actualQuadruple[3]
          return True

     def translateVirtualToAbsolute(self, virDir):
          if virDir >= self.MemoryManager.getLocalStart():
               actualCounters = self.localTypeCounters.peek()
               virDirType = self.MemoryManager.getEntryTypeId(virDir)
               offSet = virDir - self.MemoryManager.getInitialIndexType(virDirType)
               dirAbs = actualCounters[virDirType] + offSet
               return dirAbs
          return virDir

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
           
     def run(self):

          self.updateActualQuadruple()
          while (self.Op != 'end'):
               if self.Op == '<>':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    V2_ABS = self.translateVirtualToAbsolute(self.V2)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)

                    result = self.MemoryManager.getEntryValue(V1_ABS) != self.MemoryManager.getEntryValue(V2_ABS)
                    self.MemoryManager.setEntryValue(R_ABS, result)

               elif self.Op == '&':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    V2_ABS = self.translateVirtualToAbsolute(self.V2)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)

                    result = self.MemoryManager.getEntryValue(V1_ABS) and self.MemoryManager.getEntryValue(V2_ABS)
                    self.MemoryManager.setEntryValue(R_ABS, result)

               elif self.Op == '|':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    V2_ABS = self.translateVirtualToAbsolute(self.V2)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)

                    result = self.MemoryManager.getEntryValue(V1_ABS) or self.MemoryManager.getEntryValue(V2_ABS)
                    self.MemoryManager.setEntryValue(R_ABS, result)

               elif self.actualQuadruple[0] < len(self.SemanticCube.Operations):
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    V2_ABS = self.translateVirtualToAbsolute(self.V2)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)

                    result = eval(str(self.MemoryManager.getEntryValue(V1_ABS)) + self.Op + str(self.MemoryManager.getEntryValue(V2_ABS)))
                    self.MemoryManager.setEntryValue(R_ABS, result)


               elif self.Op == '=':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)
                    
                    result = self.MemoryManager.getEntryValue(V1_ABS)
                    self.MemoryManager.setEntryValue(R_ABS, result)

               elif self.Op == 'print':
                    R_ABS  = self.translateVirtualToAbsolute(self.R)
                    result = self.MemoryManager.getEntryValue(R_ABS)
                    print(result)

               # Read
               elif self.Op == 'read':
                    pass

               # dieferente contexto
               elif self.Op == 'params':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    R_ABS  = self.translateVirtualToAbsolute(self.R)
                    
                    result = self.MemoryManager.getEntryValue(V1_ABS)
                    self.MemoryManager.setEntryValue(R_ABS, result)

               # return <- tengo el valor en la pila, pero que hago con el?
               elif self.Op == 'return':
                    if self.R != None:
                         R_ABS  = self.translateVirtualToAbsolute(self.R)
                         result = self.MemoryManager.getEntryValue(R_ABS)
                         self.returnValues.push(result) # <- Deep???
                    self.deleteLocalVars()
                    self.instructionPointer = self.iPS.pop()
                    self.contextStack.pop()
                    
               # era
               elif self.Op == 'era':
                    self.addToContextStack(self.R)
                    self.addToCountersStack()
                    self.loadFunction()

               # gosub
               elif self.Op == 'goSub':
                    self.iPS.push(self.instructionPointer)
                    self.instructionPointer = self.R - 1

               elif self.Op == 'goto':
                    self.instructionPointer = self.R - 1

               elif self.Op == 'gotoT':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    condition = self.MemoryManager.getEntryValue(V1_ABS)
                    
                    if condition:
                         self.instructionPointer = self.R - 1
                         
               elif self.Op == 'gotoF':
                    V1_ABS = self.translateVirtualToAbsolute(self.V1)
                    condition = self.MemoryManager.getEntryValue(V1_ABS)
                    
                    if not condition:
                         self.instructionPointer = self.R - 1
               
               self.instructionPointer += 1
               self.updateActualQuadruple()

          #self.deleteLocalVars()


class VirtualMachine:
     Instance = VirtualMachineClass()
     
     def __init__(self):
          pass