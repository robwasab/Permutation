#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3

import tkinter
from tkinter import *
from tkinter import ttk

import sys
import os
import code

import extractValues
import binarySearch 

def main():
   global current_chain_link
   current_chain_link = ChainLink(name = 'Base Link')
   
   root = Tk()
   create_file_frame(root)
   create_component_frame(root)
   code.interact(local=locals())   
   #enter the main loop
   root.mainloop()
   return 
   
def create_file_frame(root):
   global file_frame_chain_link 
   file_frame_chain_link = current_chain_link
     
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
      
      #regardless of whether or not the next
      #chain link actually has a next pointer
      #call it anyways
      file_frame_chain_link.activate_next()
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
   component_frame = ttk.Frame(master = root)
   component_frame.grid(row = 0, column = 1, sticky = 'nesw')
   
   #deactivate = lambda arg: component_frame.grid_remove()
   #activate   = lambda arg: component_frame.grid()
   
   #component_frame_chain_link = ChainLink(name = 'Component Frame', \
   #activate_routine = activate, deactivate_routine = deactivate)
   
   #capacitor or resistor radiobuttons
   #state variable
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
   
   component_search_entry_var = StringVar()
   component_search_entry_var.set('Enter the component value to search for')
   component_search_entry  = ttk.Entry(master = component_frame, textvariable = component_search_entry_var)
   component_search_button = ttk.Button(master = component_frame, text = 'search through permuted components')
   
   component_show_all_button = ttk.Button(master = component_frame, text = 'show all permutations')
   
   global component_list_box_var
   component_list_box_var = StringVar()
   #leave the list_box_var variable blank
   #update component_list_box_var whenever you add to the dictionary permuted_components
   #permuted_components is declared below 
      
   global component_list_box 
   component_list_box = Listbox(master = component_frame, listvariable = component_list_box_var)
   
   component_frame_label = ttk.Label(master = component_frame, text = 'Component Permutation Frame')
   component_frame_label.grid(row = 0, column = 0, sticky = 'w')
      
   choose_cap.grid(row = 1, column = 0, sticky = 'w')
   choose_res.grid(row = 1, column = 1, sticky = 'w')
   
   choose_series.grid  (row = 2, column = 0, sticky = 'w')
   choose_parallel.grid(row = 2, column = 1, sticky = 'w')
   
   permutation_length_label = ttk.Label(master = component_frame, text = 'Permutation Maximum Length')
   
   permutation_length_var = StringVar()
   permutation_spin_box = Spinbox(master = component_frame, textvariable = permutation_length_var)
   permutation_spin_box['to'] = 3
   permutation_spin_box['from'] = 1
   
   permute_button = ttk.Button(master = component_frame, text = 'Permute')
   
   permutation_length_label.grid(row = 3, column = 0)
   permutation_spin_box.grid    (row = 3, column = 1, sticky = 'w')
   permutation_spin_box['width'] = 3
   permute_button.grid          (row = 4, column = 0, columnspan = 2)
      
   component_list_box_label = ttk.Label(master = component_frame, text = 
   '\
   Select from list, which\n\
   which group of components\n\
   you wish to use in your\n\
   search >>') 

   component_list_box_label.grid(row = 5, column = 0)
   component_list_box.grid      (row = 5, column = 1)
   
   component_search_entry.grid (row = 6, column = 0, sticky = 'we')
   component_search_button.grid(row = 6, column = 1, sticky = 'w')

   component_show_all_button.grid(row = 7, column = 1, sticky = 'w')

   global status_label_var 
   status_label_var = StringVar()
   status_label = ttk.Label(master = component_frame, textvariable = status_label_var)
   status_label.grid(row = 8, column = 0, sticky = 'sw')
   
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
   
   def component_search(*args):
      try:
         key = get_key_from_component_list_box()
         #print(key)
         #print_permuted_components_with_key(permuted_components, key)
         bag_of_parts = permuted_components[key]
      
         #get the value from component_search_entry
         text = component_search_entry_var.get()
         val = 0.0
         try:
            val = float(text)
            obj = binarySearch.binarySearch(bag_of_parts, val)
            print('found: ', obj)
            status_label_var.set(str(obj))
         except ValueError:
            status_label_var.set('Search entry contents not valid')
            return
      except Exception as e:
         print(e)
      return
         
   component_search_button['command'] = component_search 
   
   def show_all_component_combos(*args):
      try:
         key = get_key_from_component_list_box()
         print_permuted_components_with_key(permuted_components, key)
      except Exception as e:
         print(e)
      return
   
   component_show_all_button['command'] = show_all_component_combos
      
   distribute_weight(component_frame)
   distribute_weight(root)   
   return

def get_list_of_keys_from_dict(dictionary):
   return list(dictionary.keys())

def get_key_from_component_list_box():
   indecies = component_list_box.curselection()  
 
   if not indecies:
      status_label_var.set('An item in component list box not selected')
      raise Exception('An item in component list box not selected')
          
   index = int(indecies[0])   
   keys = get_list_of_keys_from_dict(permuted_components)
   return keys[index]
    
def print_permuted_components_with_key(permuted_components, key):
   comp_list = permuted_components[key]
   for comp in comp_list:
      print(comp)
   return
   
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

def ChainLink(object):
   #if previous is None then this is the first
   #chain item
   def __init__(self, next = None, activate_routine = None, deactivate_routine = None, name = ''):
      self.next = next
      self.activate_routine = activate_routine
      self.deactivate_routine = deactivate_routine
      return
   
   def __str__():
      return '-> %s' % name
   
   def setNext(next):
      self.next = next
   
   def activate_next(self):
      if self.next.activate_routine:
         self.next.activate_routine()
      return
   
   def deactivate_rest_of_chain(self):
      if self.next:
         self.next.deactivate_routine()
         self.next.deactivate_rest_of_chain()
      return
   
   
if __name__ == '__main__':
   try:
      files = search_current_dir()
      
      main()
   except KeyboardInterrupt:
      sys.exit(1)   
   
