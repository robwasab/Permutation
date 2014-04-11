#! /usr/bin/python
import sys
import extractValues

#def binarySearch(list, target):
#   length = len(list)
#   length /= 2
#   length = int(length)
   
   #sample the first item of the list
   
#   if type(list[0]) is extractValues.Component:
      #print 'List of components switching target...'
      
#      target = extractValues.Component(target)
   
#   return binarySearchRecurse(list, target, length, length)

#def binarySearchRecurse(list, target, width, curr):
   
#   if width == 0:
#      return list[curr]
   
#   difference = list[curr] - target
#   if difference < 0:
#      curr += int(width/2)
#   else:
#      curr -= int(width/2)
            
#   return binarySearchRecurse(list, target, int(width/2), curr) 

def printComponents(comp):
   print('-----------------')
   for c in comp:
      print(str(c))
   print('-----------------')
   return 

def abss(x):
   if(x < 0):
     return x * -1
   return x   
   
def binarySearch(seq, target):
   if type(seq[0]) is extractValues.Component:
      target = extractValues.Component(target)
   mini = 0
   maxi = len(seq) - 1
   while True:
      m = (mini + maxi) // 2

      if maxi < mini:
         return wrap_up(seq, m, target)
       
      if seq[m] < target:
         mini = m + 1
      elif seq[m] > target:
         maxi = m - 1
      else:
         return m

def wrap_up(seq, m, target):
   #check tolerances 
   diff = lambda x,y : abss(float(x)-float(y))
   
   min_diff_index = m
   min_diff = diff(target, seq[m])
   
   for i in range(m-1, m+2):
      try:
         if diff(target, seq[i]) < min_diff:
            min_diff = diff(target, seq[i])
            min_diff_index = i
      except IndexError as ie:
         continue 
   return min_diff_index
       
def main():

   rValues =   extractValues.resistorValues()
   seriesR    = extractValues.getComponentCombinations(rValues, 1, extractValues.rSeries, 'R Series')
   for r in seriesR:
      print(r)
    
   print(binarySearch(list(range(0,19)), 10))   
   
   print(binarySearch(seriesR, 68001.0))   
   return

if __name__ == '__main__':
   main()
