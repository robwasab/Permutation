#!/usr/bin/python

import sys
import re
import math 
import extractValues

def multiply(a,b):
   return a * b

def divide(a,b):
   return a/b

def add(a,b):
   return a + b

def findBestPairs(list1, list2, operation, tolerance, target):
   while True:
      bestPairs = iterateListsReturnArray(list1, list2, operation, tolerance, target)
      if len(bestPairs) == 0:
         tolerance *= 10
         continue
      break
      
   return bestPairs
   
def iterateListsReturnArray(listX, listY, operation, tolerance, target):
  
   ret = [] 
   
   for x in range(0, len(listX)):
      
      for y in range(0, len(listY)):
         
         if (math.fabs(operation(listX[x] ,listY[y]) - target) <= tolerance):
            thing = (listX[x], listY[y], operation(listX[x] ,listY[y]), tolerance)
            
            ret.append(thing)
   
   return ret

   
BEST_VALUE_1 = 0
BEST_VALUE_2 = 1
RESULT = 2
BEST_TOLERANCE = 3
 
def main():
   capValues = extractValues.capacitorValues()
   newCapValues = extractValues.getComponentCombinations(capValues, 2, extractValues.cSeries, 'C Series')
   
   rValues = extractValues.resistorValues()
   newRValues = extractValues.getComponentCombinations(rValues, 2, extractValues.rSeries, 'R Series')
   
   TOLERANCE = 0.00000000001
   
   target = 1020
   
   print('*** findBestPairs TEST ***')
   
   bestPairs = findBestPairs(capValues, rValues, multiply, TOLERANCE, target)
   for bestPair in bestPairs:
      res = bestPair
      capValue = res[0]
      rValue = res[1]
      result = res[2]
      tolerance = res[3]
      print('C: ', capValue, ' R: ', rValue, ' res: ', result, ' target: ', target, ' tolerance: ', tolerance)  

   print('*** USING PERMUTATIONS ***')
   
   bestPairs = findBestPairs(newCapValues, newRValues, multiply, TOLERANCE, target)
   for bestPair in bestPairs:
      res = bestPair
      capValue = res[0]
      rValue = res[1]
      result = res[2]
      tolerance = res[3]
      print('C: ', capValue, ' R: ', rValue, ' res: ', result, ' target: ', target, ' tolerance: ', tolerance)  
   
   
   
if __name__ == '__main__':
   main()
