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

class FunctionDirectoryClass:
     #####---- Directory's Methods ----#####

     # Constructor del directorio de funciones.
     def __init__(self):
          self.MemoryManager = MemoryManager.MemoryManager().Instance
          self.resetDirectory()

     # Borra / Resetea todo el diccionario y directorio de funciones.
     def resetDirectory(self):
          # Reinicializar la memoria.
          self.MemoryManager.resetMemory()
          self.functionRow = []
          self.functionDictionary = {}

          # Scopes Declarados por Default: Global, Temporal, Constant.
          self.addFunction('global', None, None)
          self.addFunction('const', None, None)
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
          return True

     def showMemory(self):
          self.MemoryManager.showMemory()
          return True

     #####---- Function's Methods ----#####

     # Agrega una funcion a el directorio de funciones, se crean tuplas con esta forma:
     # Diccionario: {nombreFunc : id}
     # Directorio:  [nombreFunc, tipo, {nombreVar : id}, [[nombreVar, tipo, direccion virtual]], cuadStart, [paramTypes], [regActivacion]]
     def addFunction(self, nombre, tipo, indiceCuadruplo):
          # Si no existe esta funcion, entonces la agrego
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
               
               # Numero de Cuaruplo primero de esa funcion
               self.functionRow[index].append(indiceCuadruplo)
               
               # Lista con tipos de datos de los parametros
               self.functionRow[index].append([])
               
               # Lista con cantidad de tipos de datos utilizados por la funcion -> ['int', 'float', 'char', 'bool', 'string']
               self.functionRow[index].append([0, 0, 0, 0, 0])

               # Cantidad de Temporales usadas en esta funcion
               self.functionRow[index].append(0)
               
               return self.functionRow[index]

          # Si ya existia una funcion con ese nombre
          else :
               print("\nERROR SEMANTICA. En este programa ya existe una funcion con nombre:", nombre)
               return None

     # Retorna la tupla: [nombreFunc, tipo, {nombreVar : id}, [[nombreVar, tipo, direccion virtual]], cuadStart, [paramTypes], [regActivacion]]
     def getFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               return self.functionRow[index]
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     # Retorna el tipo de dato de retorno de la funcion
     def getFunctionType(self, nombre):
          return self.getFunction(nombre)[1]

     # Retorna el indice de la funcion en el diccionario de funciones
     def getFunctionIndex(self, nombre):
          return self.functionDictionary[nombre]

     # Retorna el id del primer cuadruplo de la funcion
     def getFunctionStartQuadrupleIndex(self, nombre):
          return self.getFunction(nombre)[4]

     # Asigna el id del primer cuadruplo de la funcion
     def setFunctionStartQuadrupleIndex(self, nombre, num):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               self.functionRow[index][4] =  num
               return True
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     # Retorna la lista con los tipos de datos de los parametros
     def getParameterTypeList(self, nombre):
          return self.getFunction(nombre)[5]

     # Agrega un tipo de parametro a la lista de parametros de esa funcion
     def addParameterType(self, nombre, tipo):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               self.functionRow[index][5].append(tipo)
               return True
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     # Borra toda la tupla de la funcion en el diccionario y directorio de funciones
     def deleteFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               self.functionRow.pop(index)
               del self.functionDictionary[nombre]
               return True
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", nombre)
               return None

     def resetLocalMemory(self):
          self.MemoryManager.resetLocalMemory()
          return True

     #####---- Variables's Methods ----#####

     # Agregar una variable al renglon de la funcion correspondiente, de tal manera que quede una tupla:
     # [nombreVar, tipo, direccion virtual]    
     def addVariable(self, function, nombre, tipo):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               if not nombre in self.functionRow[index][2].keys() :
                    indexVar = len(self.functionRow[index][2])
                    self.functionRow[index][2][nombre] = indexVar
                    self.functionRow[index][3].append([])
                    self.functionRow[index][3][indexVar].append(nombre)
                    self.functionRow[index][3][indexVar].append(tipo)
                    self.functionRow[index][3][indexVar].append(self.MemoryManager.addEntry(index, tipo, None))
                    self.functionRow[index][6][self.getIdType(tipo)] += 1
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
                    self.MemoryManager.deleteEntry(virDir)
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
          return self.getVariable(function, nombre)[1]

     # Retorna el valor que contiene la variable de la funcion dada como argumento.
     def getVariableValue(self, function, nombre):
          return self.MemoryManager.getEntryValue(self.getVariableVirtualDirection(function, nombre))
          
     # Retorna la direccion virtual donde esta contenida la variable de la funcion dada como argumento.
     def getVariableVirtualDirection(self, function, nombre):
          return self.getVariable(function, nombre)[2]

     # Sirve para establecer o modificar el valor que contiene la variable de la funcion dada como argumento.
     def setVariableValue(self, function, nombre, valor):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               # Si existe en la variable en el scope de la funcion               
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    virDir = self.functionRow[index][3][indexVar][2]
                    self.MemoryManager.setEntryValue(virDir, valor)
                    return True
               # Si existe en la variable en el scope global
               elif nombre in self.functionRow[0][2].keys() :
                    indexVar = self.functionRow[0][2][nombre]
                    virDir = self.functionRow[0][3][indexVar][2]
                    self.MemoryManager.setEntryValue(virDir, valor)
                    return True
               else :
                    print("\nERROR SEMANTICA. En el scope:", function, "no existe una variable con nombre:", nombre)
                    return None
          else :
               print("\nERROR SEMANTICA. En este programa no existe una funcion con nombre:", function)
               return None

     #####---- Temporal Var's Methods ----#####
          
     def addTemporalVariable(self, nombreFunc, valor, tipo):
          ScopeIndex = self.functionDictionary[nombreFunc]
          VarTempName = '_t' + str(self.getFunction(nombreFunc)[7])
          self.getFunction(nombreFunc)[7] += 1
          self.addVariable(nombreFunc, VarTempName, tipo)
          self.setVariableValue(nombreFunc, VarTempName, valor)
          return self.getTemporalVariableVirtualDirection(nombreFunc, VarTempName)

     def getTemporalVariable(self, nombreFunc, nombre):
          return self.getVariable(nombreFunc, nombre)

     def getTemporalVariableVirtualDirection(self, nombreFunc, nombre):
          return self.getVariableVirtualDirection(nombreFunc, nombre)
     
     def getTemporalVariableValue(self, nombreFunc, nombre):
          return self.getVariableValue(nombreFunc, nombre)
     
     def getTemporalVariableType(self, nombreFunc, nombre):
          return self.getVariableType(nombreFunc, nombre)

     #####---- Constants's Methods ----#####

     # Agregar una constante al scope 'const' de tal manera que quede una tupla:
     # [constante, tipo,  direccion virtual]    
     def addConstant(self, constante, tipo):
          index = self.functionDictionary['const']
          if not constante in self.functionRow[index][2].keys() :
               indexVar = len(self.functionRow[index][2])
               self.functionRow[index][2][constante] = indexVar
               self.functionRow[index][3].append([])
               self.functionRow[index][3][indexVar].append(constante)
               self.functionRow[index][3][indexVar].append(tipo)
               self.functionRow[index][3][indexVar].append(self.MemoryManager.addEntry(index, tipo, eval(constante)))
               return self.getConstantVirtualDirection(constante)
          return self.getConstantVirtualDirection(constante)

     # Retorna la tupla: [constante, tipo,  direccion virtual]
     def getConstant(self, constante):
          return self.getVariable('const', constante)

     # Retorna la direccion virtual en donde esta almacenada la constante.
     def getConstantVirtualDirection(self, constante):
          return self.getVariableVirtualDirection('const', constante)

     #####---- Utilidades ----#####

     def getIdType(self, tipo):
          dataTypes = ['int', 'float', 'char', 'bool', 'string', 'void']
          return dataTypes.index(tipo)

class FunctionDirectory:
     Instance = FunctionDirectoryClass()
     
     def __init__(self):
          pass
