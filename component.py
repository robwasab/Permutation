from engineering_notation import to_eng_notation
from random import random
from random import randint
from math import fabs

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
   
   def __init__(self, components, operation = None , label = '', value = None, tolerance = 0):
   
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
         
      self.tolerance = tolerance
      
      self.monte_callable = False
      
      self.monte_carlo_flag = False
      
      if tolerance > 0:
      
         self.monte_callable = True
      
      else:
      
         for c in self.parts[1]:
      
            if isinstance(c, Component):
            
               if c.tolerance > 0:
           
                  self.monte_callable = True
               
                  break
            
      return
   
   def isMonteCallable(self):
      return self.monte_callable
   
   def getTolerance(self):
      return self.tolerance
         
   def getOperation(self):
      return self.parts[self.OPERATION]
   
   def getValue(self):
      return self.parts[self.VALUE]
   
   def getRandomValue(self):
      
      tol = 2 * tol * self.getValue() * (random() - 0.5)

      return self.getValue() + tol
   
   
   def monte_carlo_value(self):

      vals = self.parts[self.COMPONENTS]

      if len(vals) == 1:
         
         if self.tolerance > 0:
         
            return self.getRandomValue()
         
         else:
         
            return self.getValue()
   
      op = self.parts[self.OPERATION]
      
      for val in vals: 
         
         if isinstance(val, Component):
            
            val.monte_carlo_flag = True
      
      value = op(vals)

      for val in vals: 
         
         if isinstance(val, Component):
            
            val.monte_carlo_flag = False

      return value
      
   def monteCarloAnalysis(self):
      
      print('Nominal Value: ' + str(self.getValue()))
      
      avg = 0
      
      for i in range(0, 100):
      
         avg += self.monte_carlo_value()
         
      avg /= float(100)
      
      print(avg)
         
      return
   
      
   def getParts(self):
      return self.parts[self.COMPONENTS]
      
   def __str__(self):
   
      prefix = self.__class__.__name__[0]
   
      eng_val = to_eng_notation(self.parts[self.VALUE])

      if len(self.parts[self.COMPONENTS]) <= 1:
         return prefix + eng_val

      label = self.parts[self.LABEL] 
      
      comp_str = ''
      
      for component in self.parts[self.COMPONENTS]:
         if type(component) == float: 
            eng_str = to_eng_notation(component)
            
            comp_str = comp_str + eng_str
            
         else:
         
            foobar = ''
            
            if len(component) > 1:
            
               foobar = '(' + str(component) + ')'
            
            else:
               
               foobar = str(component)
               
            comp_str = comp_str + foobar   
            
         comp_str = comp_str + label
      
      #remove the last appended label...
      comp_str = comp_str[0:len(comp_str) - len(label)]
         
      return prefix + eng_val + " = " + comp_str
   
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
            if isinstance(comp, Component):
               ret.append(comp.toSaveStr())
            else:
               ret.append(str(comp))
         comps = list_to_string(ret)
         
      python_str = className + '(' + comps + ',' + op + ',\'' \
      + label + '\',' + str(val) + ',' + str(self.tolerance) +')' 
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
   
      if self.monte_carlo_flag:
      
         return self.monte_carlo_value()
         
      else:
      
         return self.getValue()

   def __len__(self):
      return len(self.getParts())

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

   tol_ranges = (0.1, 0.05, 0.02, 0.01, 0.005, 0.0025, 0.001, 0.0005, 0)

   def __init__(self, *args, **kwargs):
   
      Component.__init__(self, *args, **kwargs)
   
      return

   def getRandomValue(self):
   
      tol = self.tolerance
      
      tol_ranges = self.tol_ranges
      
      try:
      
         next_tol = tol_ranges[tol_ranges.index(tol) + 1]
         
         tol_width = tol - next_tol
                  
         shift = (tol + next_tol) / 2.0
         
         tol = (random() - 0.5) * tol_width

         if randint(0,1) == 0:
         
            tol += shift
            
         else:
         
            tol -= shift
         
         if fabs(tol) > self.tolerance or fabs(tol) < next_tol:
            print('********************')
            print('Original: ' + str(self.tolerance * 100))
            print('from: ' + str(next_tol * 100) + ' to: ' + str(self.tolerance * 100))
            print('using tolerance: ' + str(tol * 100))
            
         
         return tol * self.getValue() + self.getValue()
         
      except ValueError as ve:
         
         print(str(tol) + ': ditching custom get value in Resistor!')
         
         return Component.getRandomValue(self)
         
class Capacitor(Component):

   def __init__(self, *args, **kwargs):
   
      Component.__init__(self, *args, **kwargs)
      
      return   
