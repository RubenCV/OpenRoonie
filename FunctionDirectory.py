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

import MemoryManager as MemoryManager
import pprint

class FunctionDirectory:

     #####---- Directory's Methods ----#####

     # Constructor del directorio de funciones.
     def __init__(self):
          self.resetDirectory()

     # Borra / Resetea todo el diccionario y directorio de funciones.
     def resetDirectory(self):
          self.MemoryManager = MemoryManager.MemoryManager()
          self.functionRow = []
          self.functionDictionary = {}
          return True

     # Cantidad de funciones almacenadas en el directorio (+ Scope Global).
     def size(self):
         return len(self.functionRow)

     # Impresion del diccionario y directorio de funciones.
     def showDirectory(self):
          print("\nFunction Dictionary: ")
          pprint.pprint(self.functionDictionary)
          print("\nFunction Directory: ")
          pprint.pprint(self.functionRow)
          print("\nMemory: ")
          pprint.pprint(self.MemoryManager.Dictionary)
          return True

     #####---- Function's Methods ----#####

     # Agrega una funcion a el directorio de funciones, se crean tuplas con esta forma:
     # [{nombreFunc : id}[nombreFunc, tipo, {nombreVar : id}, [[nombreVar, tipo, valor, direccion virtual]]]]
     def addFunction(self, nombre, tipo):
          if not nombre in self.functionDictionary.keys() :
               # Calculo mi futuro indice y lo asocio en mi diccionario.
               index = self.size()
               self.functionDictionary[nombre] = index
               # Agrego el Row con todos sus valores.
               self.functionRow.append([])
               self.functionRow[index].append(nombre)
               self.functionRow[index].append(tipo)
               # Lista de Variables
               self.functionRow[index].append({})
               self.functionRow[index].append([])          
               return self.functionRow[index]
          else :
               print("\nERROR SEMANTICA. En este programa ya existe una funcion con nombre:", nombre)
               return None

     # Retorna la tupla: [nombreFunc, tipo, {nombreVar : id}, [[nombreVar, tipo, direccion virtual]]]
     def getFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               return self.functionRow[index]
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     # Borra toda la tupla de la funcion en el directorio de funciones.
     def deleteFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               self.functionRow.pop(index)
               del self.functionDictionary[nombre]
               return True
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     #####---- Variables's Methods ----#####

     # Agregar una variable al renglon de la funcion correspondiente, de tal manera que quede una tupla:
     # [nombreVar, tipo, valor, direccion virtual]    
     def addVariable(self, function, nombre, tipo):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               if not nombre in self.functionRow[index][2].keys() :
                    indexVar = len(self.functionRow[index][2])
                    self.functionRow[index][2][nombre] = indexVar
                    self.functionRow[index][3].append([])
                    self.functionRow[index][3][indexVar].append(nombre)
                    self.functionRow[index][3][indexVar].append(tipo)
                    self.functionRow[index][3][indexVar].append(self.MemoryManager.AddEntry(index, tipo, None))
                    return self.functionRow[index][3][indexVar]
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "ya existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     # Borra la tupla de la variable dada del renglon de la funcion correspondiente en el directorio de funciones.
     def deleteVariable(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    virDir = self.functionRow[index][3][indexVar][2]
                    self.MemoryManager.DeleteEntry(virDir)
                    self.functionRow[index][3][nombre].pop(indexVar)
                    del self.functionRow[index][2][nombre]
                    return True
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     # Retorna la tupla: [nombreVar, tipo, direccion virtual], para la funcion y variable dadas como argumento.
     def getVariable(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    return self.functionRow[index][3][indexVar]
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    return self.functionRow[0][3][indexVar]
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     # Retorna el tipo de dato al que pertenece la variable de la funcion dada como argumento.
     def getVariableType(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    return self.functionRow[index][3][indexVar][1]
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    return self.functionRow[0][3][indexVar][1]
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     # Retorna el valor que contiene la variable de la funcion dada como argumento.
     def getVariableValue(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    virDir = self.functionRow[index][3][indexVar][2]
                    return self.MemoryManager.GetEntryValue(virDir)
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    virDir = self.functionRow[0][3][indexVar][2]
                    return self.MemoryManager.GetEntryValue(virDir)
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None
          
     # Retorna la direccion virtual donde esta contenida la variable de la funcion dada como argumento.
     def getVariableVirtualDirection(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    return self.functionRow[index][3][indexVar][2]
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    return self.functionRow[0][3][indexVar][2]
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     # Sirve para establecer o modificar el valor que contiene la variable de la funcion dada como argumento.
     def setVariableValue(self, function, nombre, valor):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion               
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    virDir = self.functionRow[index][3][indexVar][2]
                    self.MemoryManager.SetEntryValue(virDir, valor)
                    return True
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    virDir = self.functionRow[0][3][indexVar][2]
                    self.MemoryManager.SetEntryValue(virDir, valor)
                    return True
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None
