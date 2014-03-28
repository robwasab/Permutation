#! /usr/bin/python

import re
import sys
import math
import copy

def capacitorValues(fileName = 'rawCapData1.txt'):
   
   f = open(fileName, 'r')
   print('Opened ', fileName)
   
   text = f.read()
   f.close()
   
   matches = re.findall(r'[\d.#]+[\w\s]',text)

   if not matches:
      print('no matches found')
      sys.exit(1)
      
   capValues = []
   
   for match in matches:
      #ignore the ones prefixed with #
      ignore = re.search(r'#.+', match)
      if ignore:
      #   print 'ignoring: C', ignore.group()
         continue
      power = 0
      capValue = 0
      si_suffix_match = re.search(r'\d+([munp])', match)
      
      if si_suffix_match:
         #is the si suffix m, u, n, p ?
         suffix = si_suffix_match.group(1)
         if suffix == 'm':
            power = -3
         elif suffix == 'u':
            power = -6
         elif suffix == 'n':
            power = -9
         elif suffix == 'p':
            power = -12
         else:
            print('unknown suffix: ', match)   
            continue 
         capValue = re.sub(r'(\d+)([munp])' , r'\1', match)
         #print match, '~> ', capValue
         
      else:
         #no si suffix
         power = 0
         capValue = match
         
      value = float(capValue) * math.pow(10, power)
      #print match, '->', value
      capValues.append(value)
   return capValues
   
def resistorValues(filename = 'rawResistorData.txt'):
   
   f = open(filename, 'r')
   print('Opened ', filename)
   
   text = f.read()
   f.close()
   
   #look for <td>pF</td>
   matches = re.findall(r'[\d.#]+[\w\s]',text)

   if not matches:
      print('no matches found')
      sys.exit(1)
      
   rValues = []
   
   for match in matches:
      #ignore the ones prefixed with #
      ignore = re.search(r'#.+', match)
      if ignore:
      #   print 'ignoring: R', ignore.group()
         continue

      power = 0
      rValue = ''
      si_suffix_match = re.search(r'[\d]+([kKM])', match)
      
      if si_suffix_match:
         #is the si suffix k K M?
         suffix = si_suffix_match.group(1)
         if suffix == 'k' or suffix == 'K':
            power = 3
         elif suffix == 'M':
            power = 6
         else:
            print('unknown suffix: ', match)   
            continue 
         rValue = re.sub(r'(\d+)([kKM])' , r'\1', match)
         #print match, '~> ', capValue
         
      else:
         #no si suffix
         power = 0
         rValue = match
         
      value = float(rValue) * math.pow(10, power)
      #print match, '->', value
      rValues.append(value)
   return rValues

def ratio(list):
   return list[0]/list[1]

def rParallel(list):
   try:
      invert = 0
      for val in list:
         invert += 1.0/val

      ret = 1.0/invert
   except ZeroDivisionError as zde:
      print(list)
      print(zde)
   return ret

def rSeries(list):
   sum = 0
   for val in list:
      sum += val
   return sum

def cParallel(list):
   return rSeries(list)

def cSeries(list):
   return rParallel(list)
   
holder = []

def defaultOperation(list):
   return 

def combination(array, r):
    data = list(range(0, r))
    holder = []    
    combinationUtil(array, data, 0, len(array)-1, 0, r);
    return

def combinationUtil(array, data, start, end, index, r):

    if index == r:
        #print data
        holder.append(copy.deepcopy(data))
        return 
 
    i = start
    while (i <= end) and (end-i+1) >= (r-index):
       
        data[index] = array[i];
        combinationUtil(array, data, i+1, end, index+1, r);
        i += 1    
    return

def getComponentCombinations(componentList, numComponentsInGroup, operation, operationName = '?', addOriginalComponents = True):
    
    combinations = []
 
    if numComponentsInGroup > 1:
       combination(componentList, numComponentsInGroup)   
    
       for thing in holder:
          group = Component(thing, operation, operationName)
          combinations.append(group)
    
    #Add the single, non permuted values
    if addOriginalComponents:
       for component in componentList:
          c = Component(component)
          combinations.append(c)
    
    #sort the return list
    combinations.sort(key=lambda x: x.getValue())
    
    return combinations

def main():
    rValues = resistorValues()
    combination(rValues, 3)
    
    rs = []
    for combo in holder:
       r = Component(combo, rSeries, 'Series')
       rs.append(r)
    
    for rValue in rValues:
       r = Component(rValue)
       rs.append(r)
    
    for r in rs:
       print(r)
       print(type(r.__str__()))
       
class Component (object):
   VALUE = 0
   COMPONENTS = 1
   OPERATION = 2
   OPERATION_NAME = 3
   
   def __init__(self, components, operation = None , operationName = '?'):
      if operation != None:
         self.parts = (operation(components), components, operation, operationName)
      else:
         single_val = components
         self.parts = (single_val, [single_val], None, operationName)
         
   def getOperation(self):
      return self.parts[self.OPERATION]
      
   def getValue(self):
      return self.parts[self.VALUE]
      
   def getParts(self):
      return self.parts[self.COMPONENTS]
      
   def __str__(self):
      value = str(self.parts[self.VALUE]) 
      
      if len(self.parts[self.COMPONENTS]) <= 1:
         return str(self.parts[self.VALUE]) + '(single)'

      opName = self.parts[self.OPERATION_NAME] 
      compList = []
      
      for component in self.parts[self.COMPONENTS]:
         compList.append("{:.3e}".format(component))
      
      return '{:.3e}'.format(self.parts[self.VALUE]) + " using: " + opName + " " + str(compList)
         
   def __eq__(self, intVal):
      return self.parts[self.VALUE] == intVal
   
   def __add__(self, other):
      return self.getValue() + other.getValue()
      
   def __sub__(self, other):
      return self.getValue() - other.getValue()
      
   def __mul__(self, other):
      return self.getValue() * other.getValue()
      
   def __div__(self, other):
      return self.getValue() / other.getValue()
   
   def __lt__(self, other):
      return self.getValue() < other.getValue()
   
   def __gt__(self, other):
      return self.getValue() > other.getValue()
      
if __name__ == '__main__':
   main()
   
   
      
