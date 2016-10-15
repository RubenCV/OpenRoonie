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

import math

class MemoryManagerClass:
     
     def __init__(self):
          self.ResetMemory()

     def ResetMemory(self):
          # Nombres de los diferentes scopes que existen en el mapa de memoria
          self.MemoryScopes = ['global','temp','const','local']
          # Nombres de tipos de datos validos
          self.DataTypes = ['int', 'float', 'char', 'bool', 'string']
          # Tamaño del buffer por cada tipo de variable, para cada contexto
          self.MaxVarsPerType = 1000
          
          # Crear / Borrar contenido del diccionario de memoria.
          self.Dictionary = {}
          # Crear / Borrar contenido del array de los contadores.
          self.Counters = []
          # Asignar los valores iniciales a los contadores de memoria.
          for i in range(1,  ((len(self.DataTypes)) * len(self.MemoryScopes)) + 1):
               self.Counters.append(self.MaxVarsPerType * i)
          return True
		
     def TranslateToCounterIndex(self, scope, tipo):
          try:
               IndexType = self.DataTypes.index(tipo)       
          except ValueError:
               print("\nERROR DATA TYPE. No existe el tipo de dato: ", tipo)
               return None
          IndexScope = 3 if scope > 2 else scope
          return len(self.DataTypes) * IndexScope + IndexType
   

     def AddEntry(self, scope, tipo, valor):
          # Obtengo el indice del arreglo de contadores de vars/consts, segun el tipo de dato y su scope
          Index = self.TranslateToCounterIndex(scope, tipo)
          if Index == None:
               print("\nMEMORY ERROR. No se pudo agregar una variable a memoria")
               return None
          VirtualMemoryIndex = self.Counters[Index]
          self.Dictionary[VirtualMemoryIndex] = valor
          self.Counters[Index] = VirtualMemoryIndex + 1
          return VirtualMemoryIndex

     def GetEntryType (self, virDir) :
          if virDir in self.Dictionary.keys() :
               TypeIndex = ((math.floor(virDir / self.MaxVarsPerType)) % len(self.DataTypes)) - 1
               return self.DataTypes[TypeIndex]
          
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def GetEntryValue(self, virDir):
          if virDir in self.Dictionary.keys() :
               return self.Dictionary[virDir];
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def SetEntryValue(self, virDir, valor):
          if virDir in self.Dictionary.keys() :
               self.Dictionary[virDir] = valor
               return True
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def DeleteEntry(self, virDir):
          if virDir in self.Dictionary.keys() :
               del self.Dictionary[virDir]
               return True
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

class MemoryManager:
     Instance = MemoryManagerClass()
     
     def __init__(self):
          pass
