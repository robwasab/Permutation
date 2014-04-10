#! /usr/bin/python

import re
import sys
import math
import copy
from engineering_notation import to_eng_notation
from component import *

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


def combination(array, r):
    data = list(range(0, r))
    global holder 
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

def getComponentCombinations(componentList = []  , numComponentsInGroup = 1, \
                                 operation = None, operationName = '?'     , addOriginalComponents = True):
    
    combinations = []
     
    if numComponentsInGroup > 1:
       combination(componentList, numComponentsInGroup)   
       
       for thing in holder:
          group = Component(thing, operation, operationName)
          combinations.append(group)
    
    #Add the single, non permuted values
    if addOriginalComponents:
       for component in componentList:
          c = 0
          if type(component) == int or type(component) == float:
             c = Component(component)
          else:
             c = component;   
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

         
if __name__ == '__main__':
   main()
   
   
      
