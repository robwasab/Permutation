#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys
import os
import code
import re

import extractValues
import binarySearch 
import resistor_gui

if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk

def main():
   root = Tk()
   root.title('EE Slave')
   
   global status_label_var 
   status_label_var = StringVar()
   status_label = ttk.Label(master = root, textvariable = status_label_var)
   status_label.grid(row = 2, column = 0, columnspan = 2, sticky = 'we')
   
   create_file_frame(root)
   create_component_frame(root)
   create_component_search_frame(root)
   
   code.interact(local=locals())   
   #enter the main loop
   root.mainloop()
   return 
  
  
   
def create_file_frame(root):
   #this frame selects the file to open the components from   
   file_frame = ttk.LabelFrame(root, text = 'Component File Selector Frame')
   file_frame.grid(row = 0, column = 0, sticky = 'nesw')

   global file_names_list
   file_names_list = search_current_dir()
   
   #make the list into a tuple because StringVar works better when 
   #it uses a tuple
   file_names_list = tuple(file_names_list)
   
   lbox_variable = StringVar(value = file_names_list)
   
   global lbox 
   lbox = Listbox(master = file_frame, listvariable = lbox_variable)

   file_name_variable = StringVar()
   file_name_variable.set('No file chosen')
   file_name_label = ttk.Label(master = file_frame, textvariable = file_name_variable)
   
   def lbox_selected(*args):
      indecies = lbox.curselection()
      index = int(indecies[0])
      #print(file_names_list[index])
      file_name = file_names_list[index]
      file_name_variable.set('Selected file: ' + file_name)
      return
      
   #Bind the callback command
   lbox.bind('<<ListboxSelect>>', lbox_selected)
   lbox.bind('<Double-1>', lbox_selected)
   
   #use grid to place all the widgets
   file_name_label.grid (row = 0, column = 0, sticky = 'we')
   lbox.grid            (row = 1, column = 0, sticky = 'nesw')

   distribute_weight(file_frame)
   return



def create_component_frame(root):      
   #Create the component creator frame
   global component_frame
   component_frame = ttk.LabelFrame(master = root, text = 'Component Permutation Frame')
   component_frame.grid(row = 0, column = 1, sticky = 'nesw')
      
   #capacitor or resistor radiobuttons
   #state variable
   global component_choice_var
   component_choice_var = StringVar()
   component_choice_var.set('resistor')
   
   #make the radiobuttons to choose between either 
   #capacitor or resistor component permutations
   choose_cap = ttk.Radiobutton(master = component_frame, variable = component_choice_var, value = 'capacitor')
   choose_res = ttk.Radiobutton(master = component_frame, variable = component_choice_var, value = 'resistor')
   choose_cap['text'] = 'Capacitor'
   choose_res['text'] = 'Resistor'
   
   configuration_choice_var = StringVar()
   configuration_choice_var.set('series')
   
   choose_series   = ttk.Radiobutton(master = component_frame, variable = configuration_choice_var, value = 'series')
   choose_parallel = ttk.Radiobutton(master = component_frame, variable = configuration_choice_var, value = 'parallel')
   choose_series  ['text'] = 'Series configuration'
   choose_parallel['text'] = 'Parallel configuration'
      
   component_show_all_button = ttk.Button(master = component_frame, text = 'show all permutations')
   
   global component_list_box_var
   component_list_box_var = StringVar()
   #leave the list_box_var variable blank
   #update component_list_box_var whenever you add to the dictionary permuted_components
   #permuted_components is declared below 
      
   global component_list_box 
   component_list_box = Listbox(master = component_frame, listvariable = component_list_box_var)
         
   choose_res.grid(row = 0, column = 0, sticky = 'w')
   choose_cap.grid(row = 1, column = 0, sticky = 'w')
   
   choose_series.grid  (row = 0, column = 1, sticky = 'w')
   choose_parallel.grid(row = 1, column = 1, sticky = 'w')
   
   permutation_length_label = ttk.Label(master = component_frame, text = 'Permutation Maximum Length')
   
   permutation_length_var = StringVar()
   permutation_spin_box = Spinbox(master = component_frame, textvariable = permutation_length_var)
   permutation_spin_box['to'] = 3
   permutation_spin_box['from'] = 1
   
   permute_button = ttk.Button(master = component_frame, text = 'Permute')
   
   permutation_length_label.grid(row = 2, column = 0)
   permutation_spin_box.grid    (row = 2, column = 1, sticky = 'w')
   permutation_spin_box['width'] = 3
   permute_button.grid          (row = 3, column = 0, columnspan = 2)
      
   component_list_box_label = ttk.Label(master = component_frame, text = \
   'This is called the:\nComponent List Box >>') 

   component_list_box_label.grid(row = 4, column = 0)
   component_list_box.grid      (row = 4, column = 1)
   
   component_show_all_button.grid(row = 5, column = 1, sticky = 'w')
   
   #important variable
   #holds all the permuted components
   #with the key as the component its configuration and its 
   #permutation length
   #see the code under def permute to see key creation
   global permuted_components
   permuted_components = {}
      
   def permute(*args):
       component_choice = component_choice_var.get()
       configuration = configuration_choice_var.get()
       length    = permutation_length_var.get()
       key = component_choice + '-' + configuration + '-' + length
       
       length = int(length)
       
       print(key)
    
       file_name = get_file_name_from_file_frame()
       operation = None
       
       #seriesCaps = extractValues.getComponentCombinations(capValues, 2, extractValues.cSeries, 'C Series')
       #parallelCaps =  extractValues.getComponentCombinations(capValues, 2, extractValues.cParallel, 'C Parallel')
       
       if component_choice == 'capacitor':
          #load all the single capValues and resValues from file
          capValues = extractValues.capacitorValues(file_name)   

          if   configuration == 'series':
             operation = extractValues.cSeries
             
          elif configuration == 'parallel':
             operation = extractValues.cParallel
          
          permuted_components[key] = \
          extractValues.getComponentCombinations(capValues, length, operation, 'capacitor ' + configuration)
             
       elif component_choice == 'resistor':
          #load all the single capValues and resValues from file
          rValues   = extractValues.resistorValues(file_name)

          if   configuration == 'series':
             operation = extractValues.rSeries
             
          elif configuration == 'parallel':
             operation = extractValues.rParallel

          permuted_components[key] = \
          extractValues.getComponentCombinations(rValues, length, operation, 'resistor ' + configuration)
       
       #refresh the component_search list_box
       text = get_list_of_keys_from_dict(permuted_components)
       text = tuple(text)
       component_list_box_var.set(text)      
       return
                
   permute_button['command'] = permute
      
   def show_all_component_combos(*args):
      try:
         key = get_key_from_component_list_box()
         print_permuted_components_with_key(permuted_components, key)
      except Exception as e:
         print(e)
      return
   
   component_show_all_button['command'] = show_all_component_combos
   return



def create_component_search_frame(root):
   search_frame = ttk.LabelFrame(master = root, text = 'Search Frame')
   search_frame.grid(row = 0, column = 2, sticky = 'nesw')
   ###subtly important row configure
   #is the reason why search_frame expands when the window expands
   root.rowconfigure(index = 2, weight = 1)
   root.columnconfigure(index = 2, weight = 2)
   
   #need a list box so that the user can
   #browse through all the permuted components
   #and a search box that finds just one component
   #below all of these options, is the resistor_gui
   global browse_all_label
   browse_all_label_var = StringVar()
   browse_all_label_var.set('Browse through all components')
   browse_all_label = ttk.Label(master = search_frame, textvariable = browse_all_label_var)
   
   global browse_all_list_box_var
   browse_all_list_box_var = StringVar() 
      
   global browse_all_list_box 
   browse_all_list_box = Listbox(master = search_frame, listvariable = browse_all_list_box_var)
   
   #do you remember component_list_box from above?
   #Make the component list box 
   #update a central key, telling us what
   #particular key from permuted_components is
   #highlighted
   #
   #And with that key, update the browse box with
   #all the components from the dictionary 
   #permuted_components using component_list_box's
   #currently highlighted item as the key
   
   def component_list_box_command(*args):
      global current_component_list_box_key
      current_component_list_box_key = get_key_from_component_list_box()   
      update_browse_all_list_box(*args)
      browse_all_label_var.set('Using %s for browsing' % current_component_list_box_key)
      return
      
   component_list_box.bind('<<ListboxSelect>>', component_list_box_command)
   
   search_label = ttk.Label(master = search_frame, text = 'Search for a single component')
   search_entry_var = StringVar()
   search_entry_var.set('')
   
   sub_frame = ttk.Frame(master = search_frame)
   search_entry  = ttk.Entry(master = sub_frame, textvariable = search_entry_var)
   search_button = ttk.Button(master = sub_frame, text = 'search')
   search_button.grid      (row = 0, column = 0, sticky = 'e')
   search_entry.grid       (row = 0, column = 1, sticky = 'w')
  
   global r_frame
   r_frame = resistor_gui.GroupResistorFrame(master = search_frame)
   
   def browse_all_list_box_command(*args):
      #get the index from browse_all_list_box
      indecies = browse_all_list_box.curselection()
      index = int(indecies[0])
      key = current_component_list_box_key
      comp = permuted_components[key][index]
      parts = comp.getParts()
      r_frame.draw_resistors(parts)
      print(comp.getValue())
      print(comp)
      return 
      
   browse_all_list_box.bind('<<ListboxSelect>>', browse_all_list_box_command)
      
   def search_button_command(*args):
      try:
         key = current_component_list_box_key
         bag_of_parts = permuted_components[key]
         
         #get the sought after value from component_search_entry
         text = search_entry_var.get()
         val = 0.0
         try:
            val = float(text)
            
            obj_indx = binarySearch.binarySearch(bag_of_parts, val)
            obj = bag_of_parts[obj_indx]
            
            status_label_var.set('found a component: ' + str(obj.getValue()))
            
            r_frame.draw_resistors(obj.getParts())
            
            #clear all the current idecies
            highlighted = browse_all_list_box.curselection()
            for item in highlighted:
               browse_all_list_box.selection_clear(item)
            
            #highlight the index that the binary search 
            #returned   _
            browse_all_list_box.selection_set(obj_indx)
            browse_all_list_box.see(obj_indx)
            print(obj)
            
         except ValueError:
            status_label_var.set('Search entry contents not valid')
            return
      except Exception as e:
         print(e)       
      return
   
   search_button['command'] = search_button_command 
   
   
   browse_all_label.grid   (row = 0, column = 0, sticky = 'w')
   browse_all_list_box.grid(row = 1, column = 0, sticky = 'nesw')
   sub_frame.grid          (row = 3, column = 0, sticky = 'nesw')
   search_label.grid       (row = 2, column = 0, sticky = 'w')
   r_frame.grid            (row = 4, column = 0, sticky = 'nesw')
   #search_frame.rowconfigure(index = 4, weight = 1)
   #search_frame.columnconfigure(index = 4, weight = 1)
   
   r_frame.draw_resistors([123,456,789])
   #r_frame.on()
   
   distribute_weight(search_frame)
   return
        
        
def update_browse_all_list_box(*args):
   key = get_key_from_component_list_box()
   bag_of_parts = permuted_components[key]
   
   #update the global variable browse_all_list_box_var
   #it is declared in component_search_frame below 
   #Spagetti Code!!!
   l = components_to_string(permuted_components, key)
   l = tuple(l)
   browse_all_list_box_var.set(l)
   return
    
    
    
def get_list_of_keys_from_dict(dictionary):
   return list(dictionary.keys())



def get_key_from_component_list_box():
   indecies = component_list_box.curselection()  
 
   if not indecies:
      msg = 'Please select an item from the Component List Box'
      status_label_var.set(msg)
      raise Exception(msg)
          
   index = int(indecies[0])   
   keys = get_list_of_keys_from_dict(permuted_components)
   return keys[index]
   
   
    
def print_permuted_components_with_key(permuted_components, key):
   comp_list = permuted_components[key]
   for comp in comp_list:
      print(comp)
   return

def components_to_string(permuted_components, key):
   #make a list the same length as len(permuted_components[key])
   l = [0] * len(permuted_components[key])   
   components = permuted_components[key]
   
   for i in range(0, len(l)):
      l[i] = str(components[i])
   
   return l
   
def get_file_name_from_file_frame():
   indecies = lbox.curselection()
   index = int(indecies[0])
   #print(file_names_list[index])
   file_name = file_names_list[index]
   return file_name



def distribute_weight(frame):
   grid = frame.grid_size();

   #make everything in the frame's grid grows
   #traverse each grid point within frame
   #setting the weighting to 1:1
   for col in range(0, grid[0]):
      for row in range(0, grid[1]):
         print('row: ', row, ' col: ', col) 
         frame.rowconfigure   (row, weight = 1)
         frame.columnconfigure(col, weight = 1)
   return



#this function returns a list of filenames in 
#the current directory
def search_current_dir(ext = 'txt'):
   directory = os.path.abspath(os.curdir)
   files = os.listdir(directory)
   
   valid_files = []
   search_pattern = r'.+' + ext
   for afile in files:
      print(afile)
      match = re.search(search_pattern, afile)
      if match:
         valid_files.append(afile)
         
   return valid_files



if __name__ == '__main__':
   try:
      files = search_current_dir()
      
      main()
   except KeyboardInterrupt:
      sys.exit(1)   
   
