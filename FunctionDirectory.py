class FunctionDirectory:
     def __init__(self):
         self.functionRow = []
         self.functionDictionary = {}

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
               print("Ya existe una funcion con ese nombre en este programa.")
               return None

     def getFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               return self.functionRow[index]
          else :
               print("No existe una funcion con ese nombre en este programa.")
               return None

     def deleteFunction(self, nombre):
          if nombre in self.functionDictionary.keys() :
               index = self.functionDictionary[nombre]
               self.functionRow.pop(index)
               del self.functionDictionary[nombre]
               return True
          else :
               print("No existe una funcion con ese nombre en este programa.")
               return None
          
     def addVariable(self, function, nombre, tipo):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               if not nombre in self.functionRow[index][2].keys() :
                    indexVar = len(self.functionRow[index][2])
                    self.functionRow[index][2][nombre] = indexVar
                    self.functionRow[index][3].append([])
                    self.functionRow[index][3][indexVar].append(nombre)
                    self.functionRow[index][3][indexVar].append(tipo)
                    self.functionRow[index][3][indexVar].append(None)
                    # Place Holder de Direccion Virtual
                    self.functionRow[index][3][indexVar].append(0)
                    return self.functionRow[index][3][indexVar]
               else :
                    print("Ya existe una variable en este scope.")
                    return None
          else :
               print("No existe una funcion con ese nombre en este programa.")
               return None

     def getVariable(self, function, nombre):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    return self.functionRow[index][3][indexVar][2]
               else :
                    print("No existe una variable en este scope con ese nombre.")
                    return None
          else :
               print("No existe una funcion con ese nombre en este programa.")
               return None
          
     def setVariable(self, function, nombre, valor):
          if function in self.functionDictionary.keys() :
               index = self.functionDictionary[function]
               if nombre in self.functionRow[index][2].keys() :
                    indexVar = self.functionRow[index][2][nombre]
                    self.functionRow[index][3][indexVar][2] = valor
                    return self.functionRow[index][3][indexVar][2]
               else :
                    print("No existe una variable en este scope con ese nombre.")
                    return None
          else :
               print("No existe una funcion con ese nombre en este programa.")
               return None

     def size(self):
         return len(self.functionRow)

     def showDirectory(self):
          print("Dictionary: ")
          print(self.functionDictionary)
          print("\nDirectory: ")
          print(self.functionRow)
          return
