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

class EnumsClass:
     def __init__(self):
          self.DataTypes  =  {'int'       :    0,
                              'float'     :    1,
                              'char'      :    2,
                              'bool'      :    3,
                              'string'    :    4,
                              'void'      :    5}

          self.Operations  =  {'+'        :    0,
                               '-'        :    1,
                               '*'        :    2,
                               '/'        :    3,
                               '>'        :    4,
                               '<'        :    5,
                               '>='       :    6,
                               '<='       :    7,
                               '<>'       :    8,
                               '=='       :    9,
                               '|'        :    10,
                               '&'        :    11,
                               '='        :    12,
                               'print'    :    13,
                               'read'     :    14,
                               'gotoT'    :    15,
                               'gotoF'    :    16,
                               'goto'     :    17,
                               'goSub'    :    18,
                               'params'   :    19,
                               'return'   :    20,
                               'era'      :    21,
                               'end'      :    22}
          
          self.FunctionsQuadruples    =     {0      :    'literalOp',
                                             1      :    'literalOp',
                                             2      :    'literalOp',
                                             3      :    'literalOp',
                                             4      :    'literalOp',
                                             5      :    'literalOp',
                                             6      :    'literalOp',
                                             7      :    'literalOp',
                                             8      :    'literalOp',
                                             9      :    'literalOp',
                                             10     :    'literalOp',
                                             11     :    'literalOp',
                                             12     :    'assignOp',
                                             13     :    'printOp',
                                             14     :    'readOp',
                                             15     :    'gotoTOp',
                                             16     :    'gotoFOp',
                                             17     :    'gotoOp',
                                             18     :    'goSubOp',
                                             19     :    'paramsOp',
                                             20     :    'returnOp',
                                             21     :    'eraOp',
                                             22     :    'endOp'}

          self.FunctionsVirtualMachine   =  {0      :    'literalOp',
                                             1      :    'literalOp',
                                             2      :    'literalOp',
                                             3      :    'divisionOp',
                                             4      :    'literalOp',
                                             5      :    'literalOp',
                                             6      :    'literalOp',
                                             7      :    'literalOp',
                                             8      :    'notEqualsOp',
                                             9      :    'literalOp',
                                             10     :    'orOp',
                                             11     :    'andOp',
                                             12     :    'assignOp',
                                             13     :    'printOp',
                                             14     :    'readOp',
                                             15     :    'gotoTOp',
                                             16     :    'gotoFOp',
                                             17     :    'gotoOp',
                                             18     :    'goSubOp',
                                             19     :    'paramsOp',
                                             20     :    'returnOp',
                                             21     :    'eraOp',
                                             22     :    'endOp'}


class Enums:
     Instance = EnumsClass()
     
     def __init__(self):
          pass
