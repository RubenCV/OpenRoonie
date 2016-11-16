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

import Enums as Enums

class SemanticCubeClass:

     def __init__(self):
          self.Enums       =  Enums.Enums().Instance
          self.DataTypes   =  self.Enums.DataTypes
          self.Operations  =  self.Enums.Operations
          self.initCube()

     def initCube(self):
                              # int
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
             self.Cube =     [[[ 0,  0,  0,  0,  3,  3,  3,  3,  3,  3, -1, -1,  0],     # int
                               [ 1,  1,  1,  1,  3,  3,  3,  3,  3,  3, -1, -1,  1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],    # void
                              # float
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
                              [[ 1,  1,  1,  1,  3,  3,  3,  3,  3,  3, -1, -1, -1],     # int
                               [ 1,  1,  1,  1,  3,  3,  3,  3,  3,  3, -1, -1,  1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],    # void
                              # char
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
                              [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # int
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1,  3,  3, -1, -1,  2],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],    # void
                              # bool
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
                              [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # int
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1,  3,  3,  3,  3,  3],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],    # void
                              # string
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
                              [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # int
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1,  3,  3, -1, -1,  4],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]],    # void
                              # void
                              #  +   -   *   /   >   <  >=  <=  <>  ==   |   &   =
                              [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # int
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # float
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # char
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # bool
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],     # string
                               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]]    # void
             return True
	
     def getResultingType(self, tipo1, tipo2, operacion):
          try:
               IndexTipo1 = self.DataTypes[tipo1]
               IndexTipo2 = self.DataTypes[tipo2]
               IndexOperacion = self.Operations[operacion]

          except ValueError:
               IndexTipo1 = -1
               IndexTipo2 = -1
               IndexOperacion = -1
          
          if IndexTipo1 > -1 and IndexTipo2 > -1 and IndexOperacion > -1 and IndexOperacion <= len(self.Cube[0][0]):
               ResType = self.Cube[IndexTipo1][IndexTipo2][IndexOperacion]
               if ResType < 0 :
                    print("\nERROR TYPE MISMATCH. Los tipos:", tipo1, "y", tipo2, "no son compatibles con la operacion:", operacion)
                    return None
               else :
                    return list(self.DataTypes.keys())[list(self.DataTypes.values()).index(ResType)]
          else :
               print("\nERROR. Tipos de datos:", tipo1, ",", tipo2, "y/o operacion:", operacion, "desconocidos")
               return None

class SemanticCube:
     Instance = SemanticCubeClass()
     
     def __init__(self):
          pass
