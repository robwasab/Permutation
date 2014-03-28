#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys

if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk

class ResistorFrame(ttk.Frame):

   def __init__(self, value = 0, *args, **kwargs):
      ttk.Frame.__init__(self, *args, **kwargs)         
      c = Canvas(master = self)
      c.grid(row = 0, column = 0)    
      self.c = c  
      self.r_width = 50
      self.r_height = 100
      self.origin_x = 10
      self.origin_y = 10
      x0 = self.origin_x
      y0 = self.origin_y
      x1 = self.origin_x + self.r_width
      y1 = self.origin_y + self.r_height 
      self.rect_cordinates = (x0, y0, x1, y1)
      
      c['width'] = 2 * self.origin_x + self.r_width
      c['height'] = 2 * self.origin_y + self.r_height
      
      self.beige = '#D69B36'
      self.blue = '#66CCFF'
            
      self.band_width = self.r_width
      
      self.empty_space = 10
      self.band_height = int(self.r_height/5)
      
      self.draw_value(value)
      return      
   
   def draw_value(self, value):
      band_codes = determine_bands(value)
      tens_power = band_codes[1]
      band_codes = band_codes[0]
      
      if len(band_codes) > 2:
         bg = self.blue
      else:
         bg = self.beige
         
      self.c.create_rectangle(self.rect_cordinates, fill = bg) 

      try:
         #draw on the bands
         for band_index in range(0, len(band_codes)):
            color_digit = band_codes[band_index]
            self.draw_band(color_digit, band_index)
      
         last_index = len(band_codes)
         self.draw_band(tens_power, last_index)
      except ValueError as ve:
         self.c.create_rectangle(self.rect_cordinates, fill = '#666666') 
         self.c.create_text((self.origin_x * 4, self.origin_y * 4), text = 'WHAT?')
      return
           
   def draw_band(self, value, band_number):
      x1  = self.origin_x
      y1  = self.origin_y
      y1 += self.empty_space
      y1 += self.band_height * band_number
      
      y2  = y1 + self.band_height - self.empty_space
      x2  = x1 + self.band_width

      cordinate = (x1, y1, x2, y2)      
      c = color(value)
      self.c.create_rectangle(cordinate, fill = c)
      return

class GroupResistorFrame(ttk.Frame):
   def __init__(self, *args, **kwargs):
      ttk.Frame.__init__(self, *args, **kwargs)
      self.r_list = []
      return
      
   def draw_resistors(self, val_list):
      #print('Val list ' + str(val_list))
      for i in range(0, len(val_list)):
         #is there already a resistor
         #frame at the list position?
         try:
            r_frame = self.r_list[i]
            #yess there was a particular
            #resistor frame...
            r_frame.draw_value(val_list[i])
         except IndexError as ie:
            r_frame = ResistorFrame(master = self, value = val_list[i])
            self.r_list.append(r_frame)
            r_frame.grid(row = 0, column = i)
            
      unused_indxs = range(len(val_list), len(self.r_list))
      
      #if there aren't any unused indecies, your good, return
      if len(unused_indxs) == 0:
         return
         
      for indx in unused_indxs:
         #print('Destroying idecies' + str(indx))
         self.r_list[indx].destroy()
         
      self.r_list = self.r_list[0:len(val_list)]
      return
   
   def off(self):
      self.grid_remove()
      
   def on(self):
      self.grid()
        
def color(value):
   #expect that the value is from 0 -> 9
   if value == 0:
      return '#000000'
   elif value == 1:
      return '#663300'
   elif value == 2:
      return '#FF0000'
   elif value == 3:
      return '#FF9900'
   elif value == 4:
      return '#FFFF00'
   elif value == 5:
      return '#00FF00'
   elif value == 6:
      return '#0000FF'
   elif value == 7:
      return '#9900FF'
   elif value == 8:
      return '#666666'
   elif value == 9:
      return '#FFFFFF'
   else:
      raise ValueError('[Unknown Value %d] must be b/w 0 thru 9' % value)   

def determine_bands(res_val):
   orig_res_val = res_val
      
   tens_pow = 0

   while(True):
      tens_pow += 1
      res_val /= 10.0
         
      #is it a decimal number slash does 
      #it have a remainder?
      if res_val < 10 or (res_val % 1) > 0.0:
         tens_pow -= 1
         res_val *= 10.0
         break 
      
   tens_place = 10
   tens_place_digits = []
   while(True):
      remainder = res_val % tens_place        

      tens_place_digit = remainder / (tens_place/10)
         
      #push onto the list zero index is the newest additions
      tens_place_digits.insert(0, tens_place_digit)
      res_val -= tens_place_digit * tens_place / 10
         
      tens_place *= 10
                  
      if res_val <= 0:
         break
      
   return (tens_place_digits, tens_pow)      
                 
def main():
   import code
   root = Tk()
   r_frame = ResistorFrame(master = root, value = 150)
   r_frame.grid(row = 0, column = 0)
   root.rowconfigure(index = 0, weight = 1)
   root.columnconfigure(index = 0, weight = 1)
   
   rg = GroupResistorFrame(master = root)
   rg.grid(row = 0, column = 1)
   root.rowconfigure(index = 1, weight = 1)
   root.columnconfigure(index = 1, weight = 1)
   
   rg.draw_resistors([100,150,1000])
   code.interact(local=locals())   
   root.mainloop()
   
if __name__ == '__main__':
   main()
      
   

