class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         return self.items.append(item)

     def pop(self):
          if self.size() > 0 :
              return self.items.pop()
          else :
               return None

     def peek(self):
          if self.isEmpty():
               return None
          else:
               return self.items[self.size()-1]

     def size(self):
         return len(self.items)
