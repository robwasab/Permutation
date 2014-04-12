#! /usr/bin/python

import re
import sys
import math
import copy
from engineering_notation import to_eng_notation
from component import *
import copy 

capacitor_suffixes = {'m': -3, 'u': -6, 'n':-9, 'p':-12}

resistor_suffixes = {'k':3, 'K':3, 'M': 6, 'G': 9}

resistor_tolerances = \
{'brown':0.01,  'red':0.02, 'green':0.005,\
 'blue':0.0025, 'violet':0.001,\
 'grey':0.0005, 'gold':0.05, 'silver':0.1}

def read_file_values(fileName, component_maker, suffix_dict, tolerance_dict = None):
   
   f = open(fileName, 'r')
   print('Opened ', fileName)
   
   text = f.read()
   f.close()

   suffix_keys = suffix_dict.keys()
      
   valid_suffixes = ''
      
   for key in suffix_keys: valid_suffixes = valid_suffixes + key
   
   valid_suffixes = valid_suffixes
   
   search_expr = r'([\d.#]+)([' + valid_suffixes + ']?)([\+/-]*)([\w%]*)\s'
   
   matches = re.findall(search_expr,text)

   if not matches:
      print('no matches found')
      sys.exit(1)
      
   values = []
   
   for match in matches:
      #ignore the ones prefixed with #
      
      value = match[0]
      
      suffix = match[1]
      
      tolerance_exp = match[2]
      
      tolerance = match[3]
      
      if value[0] == '#':
      
         continue
      
      power = 0
      
      if suffix:
         #is the si suffix m, u, n, p ?
         
         try:
            
            power = suffix_dict[suffix]
         
         except KeyError as ke:
         
            print('unknown suffix: ' + suffix)   
            
            continue 
         
      else:
         #no si suffix
         power = 0
         
      value = float(value) * math.pow(10, power)
      
      if not tolerance or not tolerance_exp:
      
         values.append(component_maker(value))
         
         continue
      
      #Find tolerances? Quantity?
      
      if tolerance_exp.find('+/-') == -1:
      
         print('Disregarding: ' + tolerance_exp)
         
         continue
      
      tolerance = tolerance.lower()
         
      #check to see if the tolerance value matches with 
      #a particular tolerance key
      
      done = False
      
      if tolerance_dict:
         
         for key in tolerance_dict:
            
            if tolerance.find(key) != -1:
            
               tolerance = tolerance_dict[key]
               
               values.append(component_maker(value, tolerance = tolerance))
               
               done = True
               
               break
               
      if done:
      
         continue
         
      #did find a tolerance value that matches a key
      #try to force the tolerance value into a number
      #look for 5%
      match = re.search(r'([\d\.]+)%', tolerance)
      
      if match:
      
         tolerance = float(match.group(1)) / 100.0
         
         values.append(component_maker(value, tolerance = tolerance))
         
         continue
      #look for just a fraction: 0.05
      try:
      
         tolerance = float(tolerance)
         
         values.append(component_maker(value, tolerance = tolerance))

      except ValueError as ve:
      
         pass
                        
      #the for loop ends right here
      
   return values

def strip_suffix(string, suffixes):

   for suffix in suffixes:
   
      indx = string.find(suffix)
      
      if indx != -1:
      
         return string[0:indx]

   return string
    
def capacitorValues(filename = 'rawCapData1.txt'):
   
   component_maker = lambda *args, **kwargs: Capacitor(*args, **kwargs)
   
   return read_file_values(filename, component_maker, capacitor_suffixes)
      
   
def resistorValues(filename = 'rawResistorData.txt'):
   
   component_maker = lambda *args, **kwargs: Resistor(*args, **kwargs)
   
   return read_file_values(filename, component_maker, resistor_suffixes, resistor_tolerances)


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
                                        op = None, operationName = '?'     , \
                     addOriginalComponents = True, componentType = 'component'):
    
    componentType = componentType.lower()
    
    make_comp = None
                     
    if componentType == 'component':
    
       make_comp = lambda *args, **kwargs: Component(*args, **kwargs)
       
    elif componentType == 'resistor':
    
       make_comp = lambda *args, **kwargs: Resistor(*args, **kwargs)
       
    elif componentType == 'capacitor':
    
       make_comp = lambda *args, **kwargs: Capacitor(*args, **kwargs)
       
    else:

       make_comp = lambda *args, **kwargs: Component(*args, **kwargs)       
    
    #Component(self, components, operation = None , label = '', value = None):
          
    combinations = []
     
    if numComponentsInGroup > 1:
    
       #SCRAMBLE the components
    
       combination(componentList, numComponentsInGroup)   
       
       for thing in holder:
          
          should_add = True
          
          group = make_comp(thing, operation = op, label = operationName)
          
          res = group.getValue()
          
          res = int(res * 10000)
          
          for val in thing:
          
             val = int(val * 10000)
             
             if res == val:
             
                should_add = False
                
                break
          
          if should_add:
          
             combinations.append(group)
    
    #account for combinations of itself...
    for component in componentList:
    
       copies = [copy.deepcopy(component)]
       
       for i in range(1, numComponentsInGroup):
       
          copies.append(copy.deepcopy(component))
          
          c = make_comp(copy.deepcopy(copies), operation = op, label = operationName)
          
          combinations.append(c)
    
    #Add the single, non permuted values
    if addOriginalComponents:
    
       for component in componentList:
       
          c = None
          
          if type(component) == int or type(component) == float:
          
             c = make_comp(component)
          else:
             c = component;
                
          combinations.append(c)
    
    #sort the return list
    combinations.sort(key=lambda x: x.getValue())
    
    return combinations

def main():
    rValues = resistorValues('test_tolerances.txt')
    
    for rValue in rValues:
    
       print(rValue)
         
if __name__ == '__main__':
   main()
   
   
      
