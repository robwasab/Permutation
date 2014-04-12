#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys
import cmath
import math
import extractValues 
from component import *
from engineering_notation import to_eng_notation

if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk

VERTICAL = 0
PARALLEL = 0
HORIZONTAL = 1
SERIES = 1
SINGLE = 2
MULTIPLY = 3
DIVIDE = 4

X = 0
Y = 1

class ComponentFrame(ttk.Frame):
   #Every Component has a canvas that is padded
   #And it has a rect_cordinates that define where 
   #to draw in 
   def __init__(self, *args, **kwargs):
   
      ttk.Frame.__init__(self, *args, **kwargs) 
              
      c = Canvas(master = self)
      
      c.grid(row = 0, column = 0)    
      
      self.c = c  
      
      self.pad = 10
      
      self.width = 50
      
      self.height = 100
      
      self.origin = (self.pad, self.pad)

      return
      
   def set_orientation(self, orient):   
                  
      if orient == VERTICAL:
         self.origin = (self.pad, self.pad)
         x0 = self.origin[X]
         y0 = self.origin[Y]
         x1 = self.origin[X] + self.width
         y1 = self.origin[Y] + self.height 
      
         self.rect_cordinates = (x0, y0, x1, y1)

         south_east = (self.rect_cordinates[2], self.rect_cordinates[3])
         self.c['width']  = south_east[X] + self.pad
         self.c['height'] = south_east[Y] + self.pad
         self.orientation = VERTICAL
         
      elif orient == HORIZONTAL:
         self.origin = (self.pad, self.width + self.pad)
         x0 = self.origin[X]
         y0 = self.origin[Y]
         x1 = self.origin[X] + self.width
         y1 = self.origin[Y] + self.height 

         self.rect_cordinates = (x0, y0, x1, y1)

         self.c['width'] = self.pad * 2 + self.height
         self.c['height'] = self.pad * 2 + self.width 
         self.orientation = HORIZONTAL
      else:
         raise ValueError('Unknown orientation parameter')  
            
      return   

   def draw_value(self, value, tolerance = 0):
      return

class ResistorFrame(ComponentFrame):

   def __init__(self, value = 0, *args, **kwargs):
   
      ComponentFrame.__init__(self, *args, **kwargs)         

      self.set_orientation(VERTICAL)
            
      self.beige = '#D69B36'
      self.blue  = '#66CCFF'
            
      self.band_width = self.width
      
      self.empty_space = 10
      self.band_height = int(self.height/5)
      
      if value != 0: self.draw_value(value)   
         
      return      
            
   def draw_value(self, value, tolerance = 0):
   
      self.c.delete(ALL)
            
      band_codes = determine_bands(value)
      
      tens_power = band_codes[1]
      
      band_codes = band_codes[0]
      
      if len(band_codes) > 2:
         bg = self.blue
      else:
         bg = self.beige
      
      if self.orientation == HORIZONTAL:
         self.cordinates = rotate_horiz(self.origin, self.rect_cordinates)
      elif self.orientation == VERTICAL:
         self.cordinates = self.rect_cordinates
         
      self.c.create_rectangle(self.cordinates, fill = bg) 
      
      try:
         #draw on the bands
         for band_index in range(0, len(band_codes)):
         
            color_digit = band_codes[band_index]
             
            self.draw_band(color(color_digit), band_index)
      
         last_index = len(band_codes)
         
         pwr_color = color(tens_power)
         
         self.draw_band(pwr_color, last_index)
         
         if tolerance != 0:
            try:
            
               self.draw_tolerance(tolerance)
               
            except KeyError as ke:
               
               pass
               
         
      except ValueError as ve:
         print(ve)
         self.c.delete(ALL)
         self.c.create_rectangle(self.cordinates, fill = '#666666') 
         self.c.create_text((self.origin[X], self.origin[Y]), text = 'WHAT?')
      return
           
   def draw_band(self, colorc, band_number):
      x1  = self.origin[X]
      y1  = self.origin[Y]
      y1 += self.empty_space
      y1 += self.band_height * band_number
      
      y2  = y1 + self.band_height - self.empty_space
      x2  = x1 + self.band_width

      cordinate = (x1, y1, x2, y2)  
      
      if self.orientation == HORIZONTAL:
         cordinate = rotate_horiz(self.origin, cordinate)
      
      self.c.create_rectangle(cordinate, fill = colorc)
      return
   
   def draw_tolerance(self, tol):
   
      x1  = self.origin[X]
      y1  = self.origin[Y] + self.height - self.band_height//3 - self.empty_space//2
      
      y2  = y1 + self.band_height//3
       
      x2  = x1 + self.band_width

      cordinate = (x1, y1, x2, y2)  
      print(cordinate)
      
      if self.orientation == HORIZONTAL:
         cordinate = rotate_horiz(self.origin, cordinate)
      
      color = tolerance_color(tol)
      
      self.c.create_rectangle(cordinate, fill = color)
      
   
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




class CapacitorFrame(ComponentFrame):

   def __init__(self, value = 0, *args, **kwargs):
   
      ComponentFrame.__init__(self, *args, **kwargs)
            
      self.line_width = 6
            
      self.setup()
      
      self.set_orientation(VERTICAL)

      if value != 0: self.draw_value(value)
      
      return
      
   def setup(self):
   
      lw = self.line_width
      
      pad = self.height/10
      
      x_center = self.width/2
      
      y_center = self.height/2
        
      plate_spacing = 16
      
      plate_width = 3.0/4.0 * self.width
      
      remainder = plate_width % 2
      
      plate_width = int(plate_width + remainder)
      
      self.color = '#000000'
      
      helper_list = []
      
      #make the top lead rectangle
      
      x1 = x_center - lw/2
      y1 = pad
      
      x2 = x_center + lw/2
      y2 = y_center - plate_spacing/2 - lw
      
      lead_north = (x1, y1, x2, y2)
      
      helper_list.append(lead_north)
      
      #make the bottom lead rectangle
      
      x1 = x_center - lw/2
      y1 = y_center + plate_spacing/2 + lw
      
      x2 = x_center + lw/2
      y2 = self.height - pad

      lead_south = (x1, y1, x2, y2)

      helper_list.append(lead_south)
            
      #make the plates
      
      x1 = x_center - plate_width/2
      y1 = y_center - plate_spacing/2 - lw
      
      x2 = x_center + plate_width/2
      y2 = y_center - plate_spacing/2
      
      plate_north = (x1, y1, x2, y2)

      helper_list.append(plate_north)
      
      x1 = x_center - plate_width/2
      y1 = y_center + plate_spacing/2
      
      x2 = x_center + plate_width/2
      y2 = y_center + plate_spacing/2 + lw
      
      plate_south = (x1, y1, x2, y2)

      helper_list.append(plate_south)
               
      self.rectangles = helper_list
             
      return
      
   def draw_value(self, value, tolerance = 0):

      self.c.delete(ALL)
      
      color = self.color

      for i in range(0, len(self.rectangles)):
           
         cord = self.rectangles[i]
            
         x = self.origin[X]
         
         y = self.origin[Y]
         
         cord = (cord[0] + x, cord[1] + y, cord[2] + x, cord[3] + y)

         if self.orientation == HORIZONTAL:
            
            cord = rotate_horiz(self.origin, cord)
         
         self.c.create_rectangle(cord, fill = color)
      
      t = to_eng_notation(value)
      
      t = t + 'F'
      
      if tolerance != 0:
      
        t = t + ' +/-' + str(tolerance * 100) + '%'
      
      #text cordinate
      cord = (int(self.c['width'])/2, int(self.c['height']) - 7) 
      
      self.c.create_text(cord, text = t)
      
      return

class GroupComponentFrame(ttk.Frame):

   def __init__(self, *args, **kwargs):
   
      ttk.Frame.__init__(self, *args, **kwargs)
      
      self.frame_list = []
      
      return
      
   def draw_components(self, source_comp):
      #print('Val list ' + str(val_list))
      config = get_config_from_component(source_comp)
      
      add_component_to_frame = None
      orient = 0
      
      if config == PARALLEL:
         #lay each resistor vertically
         add_component_to_frame = lambda c, incr: c.grid(row = incr, column = 0)
         orient = HORIZONTAL
         
      elif config == SERIES:
         #lay each resistor horizontally
         add_component_to_frame = lambda c, incr: c.grid(column = incr, row = 0)
         orient = HORIZONTAL
         
      elif config == SINGLE:
         add_component_to_frame = lambda c, incr: c.grid(column = incr, row = 0)
         orient = HORIZONTAL
      
      elif config == MULTIPLY or config == DIVIDE:
         #lay each resistor horizontally
         add_component_to_frame = lambda c, incr: c.grid(column = incr, row = 0)
         orient = HORIZONTAL
         
      val_list = source_comp.getParts()
      
      for i in range(0, len(val_list)):
         #is there already a resistor
         #frame at the list position?
         try: 
            #try to see if there is an element in the gui frame list
            comp_frame = self.frame_list[i]
            
         except IndexError as ie:
            self.frame_list.append(None)
         
         #is the current val_list[i] a Component Object?
         #if it is, we need to recursively call draw_resistors again, with that 
         #Component 
         current_value = val_list[i]
         
         if isinstance(current_value, Component):
            #print('Starting Recursive Dive!')
            #print('Value of component to dive with: ' + str(current_comp))
            
            gui = None
            comp_frame = self.frame_list[i]
            
            if isinstance(comp_frame, GroupComponentFrame):
               gui = comp_frame
            else:
               if isinstance(comp_frame, ttk.Frame):
                  comp_frame.destroy()   
                                 
               gui = GroupComponentFrame(master = self)
               self.frame_list[i] = gui
               
            gui.grid_forget()   
            add_component_to_frame(gui, i)            
            gui.draw_components(current_value)
            
         else:               
            
            get_frame = None
            
            if type(source_comp) == Resistor:
            
               get_frame = lambda *args, **kwargs: ResistorFrame(*args, **kwargs)
            
            elif type(source_comp) == Capacitor:
            
               get_frame = lambda *args, **kwargs: CapacitorFrame(*args, **kwargs)
            
            elif isinstance(source_comp, Component):
            
               raise ValueError('Got a type Component, cannot draw this!')
                  
            else:
               #I don't know what to do!
               #based off the component details,
               #I couldn't determine if it was either a 
               #Resistor or a Capacitor
               raise ValueError('Couldnt determine component type!')
            
            comp_frame = self.frame_list[i]
               
            if isinstance(comp_frame, ttk.Frame):
               
               comp_frame.destroy()
                                    
            self.frame_list[i] = get_frame(master = self)
            
            self.frame_list[i].set_orientation(orient) 
            
            if len(source_comp.getParts()) == 1 and source_comp.getTolerance() > 0:
               
               self.frame_list[i].draw_value(current_value, tolerance = source_comp.getTolerance())
               
            else:
               
               self.frame_list[i].draw_value(current_value)
            
            add_component_to_frame(self.frame_list[i], i)
            
      #clean up
      unused_indxs = range(len(val_list), len(self.frame_list))
      
      #if there aren't any unused indecies, your good, return
      if len(unused_indxs) == 0:
         return
            
      for indx in unused_indxs:
         print('Cleaning up idecies ' + str(indx))
         self.frame_list[indx].destroy()
         
      self.frame_list = self.frame_list[0:len(val_list)]
      return
   
   def off(self):
      self.grid_remove()
      
   def on(self):
      self.grid()
   
   def __str__(self):
      return 'Group Resistor Frame'
         
   def destroy(self):
      for c in self.frame_list:
         c.grid_remove()
         c.destroy()
        
      ttk.Frame.destroy(self)
      return
      
def get_config_from_component(comp):

   try:
   
      op = comp.getOperation().__name__
      
      op = op.lower()
      
      if op.find('series') != -1:
      
         return SERIES
         
      elif op.find('parallel') != -1:
      
         return PARALLEL
         
      elif op.find('multiply') != -1:
      
         return MULTIPLY
         
      elif op.find('divide') != -1:
      
         return DIVIDE
         
   except Exception as e:
      return SINGLE
        
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

tol_dict = \
{0.01  :'#663300', 0.02 :'#FF0000', 0.005:'00FF00',\
 0.0025:'#0000FF', 0.001:'#9900FF', \
 0.0005:'#666666', 0.05 :'#7F6B00', 0.1:  '#999999'}


def tolerance_color(tol):

   return tol_dict[tol]

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
   r_frame.grid(row = 0, column = 0, sticky = 'nesw')
   root.rowconfigure(index = 0, weight = 1)
   root.columnconfigure(index = 0, weight = 1)
   
   gr = GroupComponentFrame(master = root)
   gr.grid(row = 0, column = 1, sticky = 'nesw')
   root.rowconfigure(index = 0, weight = 1)
   root.columnconfigure(index = 1, weight = 1)
   
   r = Resistor(components = [123,456,789], operation = extractValues.rParallel)
   
   gr.draw_components(r)
   
   c_frame = CapacitorFrame(master = root, value = 4.7E-6)
   
   c_frame.grid(row = 0, column = 2, sticky = 'nesw')
   root.rowconfigure(index = 0, weight = 1)
   root.columnconfigure(index = 2, weight = 1)

   gc = GroupComponentFrame(master = root)
   gc.grid(row = 0, column = 3, sticky = 'nesw')
   root.rowconfigure(index = 0, weight = 1)
   root.columnconfigure(index = 3, weight = 1)

   c = Capacitor(components = [1.1E-6, 4.7E-6, 10E-12], operation = extractValues.cParallel)
   
   gc.draw_components(c)
   
   code.interact(local=locals())   
   root.mainloop()
   
if __name__ == '__main__':
   main()
      
   

