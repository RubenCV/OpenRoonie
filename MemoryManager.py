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

class MemoryManager:
     
     def __init__(self):
          self.MaxVarsPerType = 1000
          self.DataTypes = ['int', 'float', 'char', 'bool', 'string']
          self.Counters = []
          self.Dictionaries = []
          self.ResetMemoryCounters()
          self.ResetMemoryDiccionaries()

     def ResetMemoryCounters(self):
             memoryScopes = 4
             startValues = []
             for i in range(1,  ((len(self.DataTypes)) * memoryScopes) + 1):
                     startValues.append(self.MaxVarsPerType * i)

             # Crear / Asignar los valores iniciales a los contadores de memoria.
             GlobalCounter = [startValues[0], startValues[1], startValues[2], startValues[3], startValues[4]]
             TempCounter = [startValues[5], startValues[6], startValues[7], startValues[8], startValues[9]]
             ConstCounter = [startValues[10], startValues[11], startValues[12], startValues[13], startValues[14]]
             LocalCounter = [startValues[15], startValues[16], startValues[17], startValues[18], startValues[19]]
             self.Counters = [GlobalCounter, TempCounter, ConstCounter, LocalCounter]
             return True
		
     def ResetMemoryDiccionaries(self):
             # Crear / Borrar contenido de los diccionarios de memoria.
             GlobalDictionary = {}
             TempDictionary = {}
             ConstDictionary = {}
             LocalDictionary = {}
             self.Dictionaries = [GlobalDictionary, TempDictionary, ConstDictionary, LocalDictionary]
             return True
		
     def AddEntry(self, scope, tipo, valor):
          try:
               IndexType = self.DataTypes.index(tipo)
          except ValueError:
               IndexType = -1

          if scope > 2 :
               IndexScope = 3
          else :
               IndexScope = scope
             
          # Verificar que sea un tipo valido
          if IndexType > -1:
               VirtualMemoryIndex = self.Counters[IndexScope][IndexType]
               self.Dictionaries[IndexScope][VirtualMemoryIndex] = valor
               self.Counters[IndexScope][IndexType] = VirtualMemoryIndex + 1
               return VirtualMemoryIndex
          else:
               print("\nERROR DATA TYPE. No existe el tipo de dato: ", tipo)
               return None

     def GetEntryValue(self, scope, virDir):
          if scope > 2 :
               IndexScope = 3
          else :
               IndexScope = scope
          if virDir in self.Dictionaries[IndexScope].keys() :
               return self.Dictionaries[IndexScope][VirtualMemoryIndex];
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def SetEntryValue(self, scope, virDir, valor):
          if scope > 2 :
               IndexScope = 3
          else :
               IndexScope = scope
          if virDir in self.Dictionaries[IndexScope].keys() :
               self.Dictionaries[IndexScope][virDir] = valor
               return True
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def DeleteEntry(self, scope, virDir):
          if scope > 2 :
               IndexScope = 3
          else :
               IndexScope = scope
          if virDir in self.Dictionaries[IndexScope].keys() :
               del self.Dictionaries[IndexScope][virDir]
               return True
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None
