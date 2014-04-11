from engineering_notation import to_eng_notation

def rParallel(lis):
   try:
      invert = 0.0
      for val in lis:
         invert += 1.0/float(val)

      ret = 1.0/invert
   except ZeroDivisionError as zde:
      print(lis)
      print(zde)
   return ret

def rSeries(lis):
   s = 0
   for val in lis:
      s += float(val)
   return s

def cParallel(lis):
   return rSeries(lis)

def cSeries(lis):
   return rParallel(lis)
   
def defaultOperation(lis):
   return 
      
class Component (object):
   VALUE = 0
   COMPONENTS = 1
   OPERATION = 2
   LABEL = 3
   
   def __init__(self, components, operation = None , label = '', value = None):
      if operation != None:
         #if value wasn't specified...
         #caluclate the value
         if value == None:
            self.parts = (operation(components), components, operation, label)
         #else, save yourself the time
         else:
            self.parts = (value, components, operation, label)     
      #if the operation was None,
      #then you got a single component       
      else:
         single_val = float(components)
         self.parts = (single_val, [single_val], None, label)
      return
         
   def getOperation(self):
      return self.parts[self.OPERATION]
   
   def getValue(self):
      return self.parts[self.VALUE]
      
   def monte_carlo_value(self):
   
      vals = self.parts[self.COMPONENTS]
     
      if len(vals) == 1:
         return float(vals[0])
      
      op = self.parts[self.OPERATION]
      
      value = op(vals)
      
      return value
   
      
   def getParts(self):
      return self.parts[self.COMPONENTS]
      
   def __str__(self):
      eng_val = to_eng_notation(self.parts[self.VALUE])

      if len(self.parts[self.COMPONENTS]) <= 1:
         return eng_val + '(single)'

      label = self.parts[self.LABEL] 
      compList = []
      
      for component in self.parts[self.COMPONENTS]:
         if type(component) == float: 
            eng_str = to_eng_notation(component)
            compList.append(eng_str)
         else:
            compList.append(str(component))
      return eng_val + " = " + label + " " + str(compList)
   
   def toSaveStr(self):
      className = self.__class__.__name__          
      comps = self.parts[self.COMPONENTS]
      label = self.parts[self.LABEL     ]
      val   = self.parts[self.VALUE     ]
      op    = self.parts[self.OPERATION ]
      
      #if the operation was 'None' then the component 
      #was a SINGLE
      #therefore, you need to save the 'component' variable
      #AS a FLOAT
      if op == None:
         op = 'None'
         comps = float(comps[0])
         comps = str(comps)
      else:
         op = get_qualified_name(op)
         ret = []
         for comp in comps:
            if type(comp) == Component:
               ret.append(comp.toSaveStr())
            else:
               ret.append(str(comp))
         comps = list_to_string(ret)
         
      python_str = className + '(' + comps + ',' + op + ',\'' \
      + label + '\',' + str(val) + ')' 
      return python_str
            
   def __eq__(self, intVal):
      return self.parts[self.VALUE] == intVal
   
   def __add__(self, other):
      return self.getValue() + float(other)
      
   def __sub__(self, other):
      return self.getValue() - float(other)
      
   def __mul__(self, other):
      return self.getValue() * float(other)
      
   def __div__(self, other):
      return self.getValue() / float(other)
   
   def __lt__(self, other):
      return self.getValue() < float(other)
   
   def __gt__(self, other):
      return self.getValue() > float(other)
      
   def __float__(self):
      return self.getValue()


def get_qualified_name(func):
   return func.__module__ + '.' + func.__name__


def list_to_string(l):
   ret = '['
   for thing in l:
      ret += thing
      ret += ', '
   ret = ret[0:-2]
   ret += ']'
   return ret 
   
#wrapper classes
class PairedComponent(Component):

   def __init__(self, *args, **kwargs):
   
      Component.__init__(self, *args, **kwargs)
      
      return


class Resistor(Component):

   def __init__(self, *args, **kwargs):
   
      Component.__init__(self, *args, **kwargs)
      
      return

class Capacitor(Component):

   def __init__(self, *args, **kwargs):
   
      Component.__init__(self, *args, **kwargs)
      
      return   
