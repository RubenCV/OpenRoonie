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

class StackedQueue:
     def __init__(self):
         self.Stack = []

     def isEmpty(self):
         return self.Stack == []

     def pushNewQueue(self, item):
          newQueue = [item]
          return self.Stack.append(newQueue)

     def pushIntoLastQueue(self, item):
          if self.isEmpty():
               return None
          elif len(self.Stack[self.size()-1]) == 0:
               return None
          else:
               return self.Stack[self.size()-1].append(item)

     def popFromLastQueue(self):
          if self.isEmpty():
               return None
          elif len(self.Stack[self.size()-1]) == 0:
               return None
          else:
               lastQueue = self.Stack[self.size()-1]
               returnV = self.Stack[self.size()-1].pop(0)
               if(len(self.Stack[self.size()-1]) == 0):
                    self.popLastQueue()
               return returnV

     def popLastQueue(self):
          if self.size() > 0 :
              return self.Stack.pop()
          else :
               return None
          
     def peekLastQueue(self):
          if self.isEmpty():
               return None
          else:
               return self.Stack[self.size()-1]

     def peekFromLastQueue(self):
          if self.isEmpty():
               return None
          elif len(self.Stack[self.size()-1]) == 0:
               return None
          else:
               lastQueue = self.Stack[self.size()-1]
               return lastQueue[0]
          
     def size(self):
         return len(self.Stack)
     
