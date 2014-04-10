#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys
import cmath
import math
import extractValues 
from component import *

if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk

R_VERTICAL = 0
R_PARALLEL = 0
R_HORIZONTAL = 1
R_SERIES = 1
R_SINGLE = 2

X = 0
Y = 1

class ResistorFrame(ttk.Frame):

   def __init__(self, value = 0, *args, **kwargs):
      ttk.Frame.__init__(self, *args, **kwargs)         
      c = Canvas(master = self)
      c.grid(row = 0, column = 0)    
      self.c = c  
      self.r_width = 50
      self.r_height = 100
      self.pad = 10
      self.orientation = -1
      
      self.origin = (self.pad, self.pad)
      
      self.set_orientation(R_VERTICAL)
            
      self.beige = '#D69B36'
      self.blue  = '#66CCFF'
            
      self.band_width = self.r_width
      
      self.empty_space = 10
      self.band_height = int(self.r_height/5)
      
      self.draw_value(value)      
      return      
         
   def set_orientation(self, orient):
      if self.orientation == orient:
         return
         
      if orient == R_VERTICAL:
         self.origin = (self.pad, self.pad)
         x0 = self.origin[X]
         y0 = self.origin[Y]
         x1 = self.origin[X] + self.r_width
         y1 = self.origin[Y] + self.r_height 
      
         self.rect_cordinates = (x0, y0, x1, y1)

         south_east = (self.rect_cordinates[2], self.rect_cordinates[3])
         self.c['width']  = south_east[X] + self.pad
         self.c['height'] = south_east[Y] + self.pad
         self.orientation = R_VERTICAL
         
      elif orient == R_HORIZONTAL:
         self.origin = (self.pad, self.r_width + self.pad)
         x0 = self.origin[X]
         y0 = self.origin[Y]
         x1 = self.origin[X] + self.r_width
         y1 = self.origin[Y] + self.r_height 

         self.rect_cordinates = (x0, y0, x1, y1)

         self.c['width'] = self.pad * 2 + self.r_height
         self.c['height'] = self.pad * 2 + self.r_width 
         self.orientation = R_HORIZONTAL       
      else:
         raise ValueError('Unknown orientation parameter')
         
      return   
      
   def draw_value(self, value):
      self.c.delete(ALL)
      band_codes = determine_bands(value)
      tens_power = band_codes[1]
      band_codes = band_codes[0]
      
      if len(band_codes) > 2:
         bg = self.blue
      else:
         bg = self.beige
      
      if self.orientation == R_HORIZONTAL:
         self.cordinates = rotate_horiz(self.origin, self.rect_cordinates)
      elif self.orientation == R_VERTICAL:
         self.cordinates = self.rect_cordinates
         
      self.c.create_rectangle(self.cordinates, fill = bg) 
      
      try:
         #draw on the bands
         for band_index in range(0, len(band_codes)):
            color_digit = band_codes[band_index]
            self.draw_band(color_digit, band_index)
      
         last_index = len(band_codes)
         self.draw_band(tens_power, last_index)
      except ValueError as ve:
         print(ve)
         self.c.delete(ALL)
         self.c.create_rectangle(self.cordinates, fill = '#666666') 
         self.c.create_text((self.origin[X], self.origin[Y]), text = 'WHAT?')
      return
           
   def draw_band(self, value, band_number):
      x1  = self.origin[X]
      y1  = self.origin[Y]
      y1 += self.empty_space
      y1 += self.band_height * band_number
      
      y2  = y1 + self.band_height - self.empty_space
      x2  = x1 + self.band_width

      cordinate = (x1, y1, x2, y2)  
      
      if self.orientation == R_HORIZONTAL:
         cordinate = rotate_horiz(self.origin, cordinate)
             
      c = color(value)
      self.c.create_rectangle(cordinate, fill = c)
      return
   
   def __str__(self):
      return 'ResistorFrame'
  
def rotate_horiz(origin, rect_cord):
   
   corigin = complex(origin[X], origin[Y])
   
   cangle = cmath.exp(math.pi/2 * -1j)
   x1 = rect_cord[0]
   y1 = rect_cord[1]
   xy1 = complex(x1, y1)
   xy1 -= corigin
   xy1 *= cangle
   xy1 += corigin
      
   x2 = rect_cord[2]
   y2 = rect_cord[3]
   xy2 = complex(x2, y2)
   xy2 -= corigin
   xy2 *= cangle
   xy2 += corigin  
   return (xy1.real, xy1.imag, xy2.real, xy2.imag)
   
class GroupResistorFrame(ttk.Frame):
   def __init__(self, *args, **kwargs):
      ttk.Frame.__init__(self, *args, **kwargs)
      self.r_list = []
      return
      
   def draw_resistors(self, comp):
      #print('Val list ' + str(val_list))
      config = get_config_from_component(comp)
      
      add_resistor_to_frame = None
      orient = 0
      
      if config == R_PARALLEL:
         #lay each resistor vertically
         add_resistor_to_frame = lambda r, incr: r.grid(row = incr, column = 0)
         orient = R_HORIZONTAL
         
      elif config == R_SERIES:
         #lay each resistor horizontally
         add_resistor_to_frame = lambda r, incr: r.grid(column = incr, row = 0)
         orient = R_HORIZONTAL
         
      elif config == R_SINGLE:
         add_resistor_to_frame = lambda r, incr: r.grid(column = incr, row = 0)
         orient = R_HORIZONTAL
         
      val_list = comp.getParts()
      
      for i in range(0, len(val_list)):
         #is there already a resistor
         #frame at the list position?
         try: 
            #try to see if there is an element in the list
            r_frame = self.r_list[i]
         except IndexError as ie:
            self.r_list.append(None)
         
         #is the current val_list[i] a Component Object?
         #if it is, we need to recursively call draw_resistors again, with that 
         #Component 
         current_comp = val_list[i]
         if type(current_comp) == Component:
            #print('Starting Recursive Dive!')
            #print('Value of component to dive with: ' + str(current_comp))
            
            gui = None
            r_frame = self.r_list[i]
            
            if isinstance(r_frame, GroupResistorFrame):
               gui = r_frame
            else:
               if isinstance(r_frame, ttk.Frame):
                  r_frame.destroy()   
                                 
               gui = GroupResistorFrame(master = self)
               self.r_list[i] = gui
               
            gui.grid_forget()   
            add_resistor_to_frame(gui, i)            
            gui.draw_resistors(current_comp)
         else:               
            r_frame = self.r_list[i]
            
            if not isinstance(r_frame, ResistorFrame):
               print('Destroying index ' + str(i) + ' Not a ResistorFrame')
               
               if isinstance(r_frame, ttk.Frame):
                  r_frame.destroy()
                                    
               self.r_list[i] = ResistorFrame(master = self, value = current_comp)
            
            self.r_list[i].set_orientation(orient) 
            self.r_list[i].draw_value(current_comp)
            add_resistor_to_frame(self.r_list[i], i)
            
      #clean up
      unused_indxs = range(len(val_list), len(self.r_list))
      
      #if there aren't any unused indecies, your good, return
      if len(unused_indxs) == 0:
         return
            
      for indx in unused_indxs:
         print('Cleaning up idecies ' + str(indx))
         self.r_list[indx].destroy()
         
      self.r_list = self.r_list[0:len(val_list)]
      return
   
   def off(self):
      self.grid_remove()
      
   def on(self):
      self.grid()
   
   def __str__(self):
      return 'Group Resistor Frame'
         
   def destroy(self):
      for r in self.r_list:
         r.grid_remove()
         r.destroy()
        
      ttk.Frame.destroy(self)
      return
      
def get_config_from_component(comp):
   try:
      op = comp.getOperation().__name__
      op = op.lower()
      if op.find('series') != -1:
         return R_SERIES
      elif op.find('parallel') != -1:
         return R_PARALLEL
   except Exception as e:
      return R_SINGLE
        
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
      raise ValueError('[Unknown Value %f] must be b/w 0 thru 9' % value)   

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
      
   

