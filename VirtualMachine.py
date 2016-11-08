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


class VirtualMachineClass:

     def __init__(self):
          self.FunctionDirectory = FunctionDirectory.FunctionDirectory().Instance
          self.QuadrupleManager  = QuadrupleManager.QuadrupleManager().Instance
          self.MemoryManager     = MemoryManager.MemoryManager().Instance

          actualQuadruple = []
          instructionPointer = 0
          iPS = Stack.Stack()

     def run(self):
          actualQuadruple = self.QuadrupleManager.QuadrupleList[instructionPointer]

          

          instructionPointer += 1


class VirtualMachine:
     Instance = VirtualMachineClass()
     
     def __init__(self):
          pass
