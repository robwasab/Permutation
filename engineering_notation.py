import math

suffixes = ['f', 'p', 'n', 'u', 'm', '', 'k', 'M', 'G', 'T'] 
def zero_index():
   for i in range(0, len(suffixes)):
      if suffixes[i] == '':
         return i
   raise ValueError('couldnt find zero power in suffixes array')
   
def to_eng_notation(num, d_places = 3):
   num = float(num)
   power = int(math.floor(math.log10(math.fabs(num))))
   power_index = power // 3
   
   #no need to do anything
   if power_index == 0:
      return str(round(num, d_places))
   
   power_index += zero_index()   
   
   num /= math.pow(10, (power // 3) * 3)
   num  = str(round(num, d_places))
   num += suffixes[power_index]
   return num 
