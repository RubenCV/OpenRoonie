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
import pprint

class MemoryManagerClass:
     
     def __init__(self):
          self.resetMemory()

     def resetMemory(self):
          # Nombres de los diferentes scopes que existen en el mapa de memoria
          self.MemoryScopes = ['global','const','local']
          
          # Nombres de tipos de datos validos
          self.DataTypes = ['int', 'float', 'char', 'bool', 'string', 'void']
          
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

     def showMemory(self):
          print("\nMemory: ")
          pprint.pprint(self.Dictionary)
          return True

     def resetLocalMemory(self):     
          for i in range(0,  len(self.DataTypes)):
               indexInicial = self.getInitialIndexType(i)
               indexFinal = self.translateToCounterIndex(2, self.DataTypes[i])
               self.Counters[len(self.DataTypes) * 2 + i] = indexInicial
               for j in range(0, indexFinal - indexInicial):
                    self.deleteEntry(indexInicial + j)
          return True

     def translateToCounterIndex(self, scope, tipo):
          try:
               IndexType = self.DataTypes.index(tipo)       
          except ValueError:
               print("\nERROR DATA TYPE. No existe el tipo de dato: ", tipo)
               return None
          IndexScope = 2 if scope > 1 else scope
          return len(self.DataTypes) * IndexScope + IndexType
   
     def addEntry(self, scope, tipo, valor):
          # Obtengo el indice del arreglo de contadores de vars/consts, segun el tipo de dato y su scope
          Index = self.translateToCounterIndex(scope, tipo)
          if Index == None:
               print("\nMEMORY ERROR. No se pudo agregar una variable a memoria")
               return None
          VirtualMemoryIndex = self.Counters[Index]
          self.Dictionary[VirtualMemoryIndex] = valor
          self.Counters[Index] = VirtualMemoryIndex + 1
          return VirtualMemoryIndex

     def getEntryType (self, virDir) :
          if virDir in self.Dictionary.keys() :
               TypeIndex = ((math.floor(virDir / self.MaxVarsPerType)) % len(self.DataTypes)) - 1
               return self.DataTypes[TypeIndex]
          
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def getEntryTypeId (self, virDir) :
          if virDir in self.Dictionary.keys() :
               TypeIndex = ((math.floor(virDir / self.MaxVarsPerType)) % len(self.DataTypes)) - 1
               return TypeIndex
          
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def getInitialIndexType(self, typeId):
          indexInicial = (len(self.DataTypes) * 2 * self.MaxVarsPerType) + (typeId * self.MaxVarsPerType) + self.MaxVarsPerType
          return indexInicial

     def getLocalStart(self):
          return (len(self.DataTypes) * 2 * self.MaxVarsPerType) + self.MaxVarsPerType

     def getLocalIndexList(self):
          indexInicialList = []
          for i in range(0,  len(self.DataTypes)):
               indexInicialList.append(self.Counters[(len(self.DataTypes) * 2) + i])
          return indexInicialList
          
     def getEntryValue(self, virDir):
          if virDir in self.Dictionary.keys() :
               return self.Dictionary[virDir];
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def setEntryValue(self, virDir, valor):
          if virDir in self.Dictionary.keys() :
               self.Dictionary[virDir] = valor
               return True
          else :
               print("\nERROR MEMORIA. Direccion de memoria invalida. Direccion: ", virDir)
               return None

     def deleteVarsByBounds(self, oldCounters, newCounters):
          for i in range(0,  len(self.DataTypes)):
               for j in range(0, newCounters[i] - oldCounters[i]):
                    self.deleteEntry(oldCounters[i]+j)
               self.Counters[len(self.DataTypes) * 2 + i] = oldCounters[i]
          return True

     def deleteEntry(self, virDir):
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
