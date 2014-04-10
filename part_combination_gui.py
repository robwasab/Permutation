#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys
import os
import code
import re
from math import fabs

import extractValues
from component import *
from engineering_notation import to_eng_notation
from progress_frame import ProgressFrame
import binarySearch 
import resistor_gui
from settings import *
import component_pairing

import multiprocessing as mp
import Queue

#compatibility between python2 and python3
if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
   import tkMessageBox as messagebox
   import tkFileDialog as fdialog
 
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk
   from tkinter import messagebox
   from tkinter import filedialog as fdialog

def main():

   root = Tk()
   
   root.title('EE Slave')
   
   global settings_dict 
   
   settings_dict = load_usr_settings()
   
   global status_label_var 
   
   status_label_var = StringVar()   
   
   status_label = ttk.Label(master = root, textvariable = status_label_var)
   
   status_label.grid(row = 1, column = 0, columnspan = 2, sticky = 'we')
   
   global progress_frame
   
   progress_frame = ProgressFrame(master = root)
   
   progress_frame.grid(row = 1, column = 2, sticky = 'nesw')
   
   progress_frame.hide()   
   
   
   create_file_frame(root)
   
   
   global tabbed_frame
   
   tabbed_frame = ttk.Notebook(master = root)
   
   id_0 = create_component_frame(tabbed_frame)
   
   tabbed_frame.add(id_0, text = 'Component Frame')
   
   global pairing_frame
   
   pairing_frame = create_pairing_frame(tabbed_frame)
   
   tabbed_frame.add(pairing_frame, text = 'Pairing Frame')
   
   tabbed_frame.tab(pairing_frame, state = 'hidden')
    
   tabbed_frame.grid(row = 0, column = 1, sticky = 'nesw')
   
   root.rowconfigure(0, weight = 1)
   
   root.columnconfigure(1, weight = 1)
   
   create_component_search_frame(root)
   
   
   #setup_routine()
   
   code.interact(local=locals())   
   #enter the main loop
   root.mainloop()
   return 
  
  
  
  
   
def create_file_frame(root):
   #this frame selects the file to open the components from   
   global file_frame
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
   component_frame = ttk.LabelFrame(master = root, text = 'Component Permutation Frame')
   component_frame.grid(row = 0, column = 0, sticky = 'nesw')
      
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
      
   save = ttk.Button(master = component_frame, text = 'save components')
   load = ttk.Button(master = component_frame, text = 'load components')
      
   global component_list_box_var
   component_list_box_var = StringVar()
   #leave the list_box_var variable blank
   #update component_list_box_var whenever you add to the dictionary permuted_components
   #permuted_components is declared below 
      
   global component_list_box 
   component_list_box = Listbox(master = component_frame, listvariable = component_list_box_var)
         
   adv_label = ttk.Label(master = component_frame, text = 'click for advanced information...')
         
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
   component_list_box.grid      (row = 4, column = 1, sticky = 'nesw')
   
   save.grid(row = 5, column = 1, sticky = 'w')
   load.grid(row = 5, column = 0, sticky = 'e')
   
   adv_label.grid(row = 6, column = 0, sticky = 'w')
   
   #important variable
   #holds all the permuted components
   #with the key as the component its configuration and its 
   #permutation length
   #see the code under def permute to see key creation
   global permuted_components
   permuted_components = {}
      
   def permute():
   
      component_choice = component_choice_var.get()
      
      configuration = configuration_choice_var.get()
      
      length    = int(permutation_length_var.get())
       
      error_msg = ''
      
      read_source_success = False 
      
      source = ''
      
      source_components = []
      
      operation = None
       
      try:       
         #try getting source components from the file list box
         file_name = get_file_name_from_file_frame()
          
         source = file_name
                           
         if component_choice == 'capacitor':
            #load all the single capValues and resValues from file
            source_components = extractValues.capacitorValues(source)   
         
         elif component_choice == 'resistor':
         
            source_components = extractValues.resistorValues(source)
                 
         read_source_success = True
       
      except Exception as e:     
        
         #Couldn't retrieve a file from the list box   
         print(e)    
         
         error_msg += str(e)
         
         #no success so try to read source components from the 
         #component list box
         read_source_success = False
       
      if not read_source_success:
         try:
            #try sourcing the components from the component list box
            #instead of the file list box
            
            key = get_key_from_component_list_box()   
               
            source = key
            
            source_components = permuted_components[key]
            
            read_source_success = True
            
         except Exception as e: 
         
            error_msg += '\n' + str(e)
            
            read_source_success = False
      
      if not read_source_success:
      
         status_label_var.set(error_msg)
         return 
      
      if component_choice == 'capacitor':
      
         if configuration == 'series':
         
            operation = extractValues.cSeries
             
         elif configuration == 'parallel':
         
            operation = extractValues.cParallel
                       
      elif component_choice == 'resistor':
      
         if configuration == 'series':
         
            operation = extractValues.rSeries
             
         elif configuration == 'parallel':
         
            operation = extractValues.rParallel
         
      label = component_choice + ' ' + configuration
      
      key = component_choice + '-' + configuration + '-' + str(length) + '[' + source + ']'

      progress_frame.show()
      
      progress_frame.setText('Permuting... with ' + str(key))
      
      pb = progress_frame.getProgressBar()
      
      pb.start()
      
      #run this in background:
      #permuted_components[key] = \
      #extractValues.getComponentCombinations(source_components, length, operation, label)
      #print_permuted_components_with_key(permuted_components, key)
      
      out_queue = mp.Queue()    

      func = extractValues.getComponentCombinations
      
      start_background(root, out_queue, func, componentList = source_components, \
      numComponentsInGroup = length, operation = operation, operationName = label)
         
      # Start a function to check a queue for GUI-related updates
      # When the background process is done, it will call permute_finisher
      finsher_func = permute_finisher
      
      #snag the old key
      old_key = source
      
      #call updater which will use root.after
      updater(root, out_queue, finsher_func, key, old_key)
      return
   
   permute_button['command'] = permute
      
   def save_command(*args):
   
      try:
      
         key = get_key_from_component_list_box()
         
         #print_permuted_components_with_key(permuted_components, key)
         save_components_to_python_file(permuted_components, key)
         
      except Exception as e:
      
         print(e)
         
         status_label_var.set(str(e))
         
      return
   
   save['command'] = save_command
   
   def load_command(*args):
   
      try:
         
         load_components_from_python_file(permuted_components)
         
      except Exception as e:
       
         print(str(e))
         
         status_label_var.set(str(e))
      
      return
      
   load['command'] = load_command
   
   def advanced_usage_toast(*args):
   
      messagebox.showinfo(message = advanced_message)
      
      return
   
   adv_label.bind('<ButtonPress-1>', advanced_usage_toast)
   
   root.rowconfigure(index = 0, weight = 1)
   
   root.columnconfigure(index = 0, weight = 2)
   
   distribute_weight(component_frame)
   
   return component_frame



advanced_message = 'instead of choosing source parts from the \'component file frame\'\
 you can AGAIN permute components from the \'component permutation frame\'\
\nThey are after all, just numbers right?'




def create_pairing_frame(parent):
   
   pairing_frame = ttk.LabelFrame(master = parent, text = 'Pairing Frame')
   
   pairing_frame.grid(row = 0, column = 0, sticky = 'nesw')
   
   component_choice_one = Spinbox(master = pairing_frame)
   
   component_choice_two = Spinbox(master = pairing_frame)
   
   op_choice_var = StringVar()
   
   op_choice_var.set('multiply')
   
   operation_frame = ttk.Frame(master = pairing_frame)
   
   choose_multiply = ttk.Radiobutton(master = operation_frame, variable = op_choice_var, value = 'multiply')
   
   choose_divide = ttk.Radiobutton(master = operation_frame, variable = op_choice_var, value = 'divide')
   
   choose_multiply['text'] = 'Multiply'
   
   choose_divide['text'] = 'Divide'
   
   op_label_var = StringVar()
   
   op_label = ttk.Label(master = pairing_frame, textvariable = op_label_var)
      
   pair_button = ttk.Button(master = pairing_frame, text = 'Find Pairs')   
      
   choose_multiply.grid(row = 0, column = 0, sticky = 'we')
      
   choose_divide.grid  (row = 1, column = 0, sticky = 'we')
   
   component_choice_one.grid(row = 0, column = 0, sticky = 'w'  )
   
   operation_frame.grid     (row = 0, column = 1, sticky = 'nesw')
   
   component_choice_two.grid(row = 0, column = 2, sticky = 'e'  )
   
   op_label.grid(row = 1, column = 0, columnspan = 3, sticky = 'we')
   
   pair_button.grid(row = 2, column = 0, sticky = 'we')
   
   update_spinbox_wrapper = lambda *arg: update_pairing_frame(component_choice_one, component_choice_two)
      
   op_label_wrapper = lambda *arg: update_op_label(component_choice_one, component_choice_two, \
   op_choice_var, op_label_var)

   def wrapper(*arg):
      
      update_spinbox_wrapper(arg)
      
      op_label_wrapper(arg)
      
      return

   parent.bind('<<NotebookTabChanged>>', wrapper)
   
   component_choice_one['command'] = op_label_wrapper
   
   component_choice_two['command'] = op_label_wrapper
   
   choose_multiply['command'] = op_label_wrapper
   
   choose_divide['command'] = op_label_wrapper
   
   root = get_master(parent)
   
   pair_command = lambda *arg: find_pairs(root, component_choice_one, component_choice_two,\
   op_choice_var, op_label_var)
   
   pair_button['command'] = pair_command
   
   return pairing_frame



def update_op_label(spinbox1, spinbox2, op_choice_var, label_var):
   
   comp1 = spinbox1.get()
   
   comp2 = spinbox2.get()
   
   op_str = ''
   
   if op_choice_var.get() == 'multiply':
   
      op_str = ' X '
      
   elif op_choice_var.get() == 'divide':
    
      op_str = ' / '
      
   label_var.set(comp1 + op_str + comp2)
   
   return
   
   
   
def update_pairing_frame(spinbox1, spinbox2):

   keys = get_list_of_keys_from_dict(permuted_components)
   
   spinbox1['value'] = keys
   
   spinbox2['value'] = keys
   
   return
   

   
def find_pairs(root, spinbox1, spinbox2, op_choice_var, label_var):
   
   key1 = spinbox1.get()
   
   key2 = spinbox2.get()
   
   operation = None
   
   if op_choice_var.get() == 'multiply':
   
      operation = component_pairing.multiply
      
   elif op_choice_var.get() == 'divide':
    
      operation = component_pairing.divide
   
   else:
      raise ValueError('Unknown Operation')
      
   #run this in background:
   #findBestPairs(list1, list2, operation, tolerance = 0.001, target = -1):
   #list1 = permuted_components[key1]
   #list2 = permuted_components[key2]
   #pairs = findBestPairs(list1, list2, operation)
   
   print(key1)
   print(key2)
   print(operation)
      
   def task(key1, key2, operation):
           
      list1 = permuted_components[key1]
      
      list2 = permuted_components[key2]
      
      pairs = component_pairing.findBestPairs(list1, list2, operation)
      
      return pairs

   progress_frame.show()
     
   progress_frame.setText('Pairing...')
      
   progress_frame.getProgressBar().start()

   out_queue = mp.Queue()

   start_background(root, out_queue, task, key1, key2, operation)
   
   def pair_finisher(ret, new_key):
      
      permuted_components[new_key] = ret
            
      update_component_list_box()
            
      return
   
   new_key = label_var.get()
   
   updater(root, out_queue, pair_finisher, new_key)   
   
   return
   
   
def create_component_search_frame(root):
   
   global search_frame
   
   search_frame = ttk.LabelFrame(master = root, text = 'Search Frame')
   
   search_frame.grid(row = 0, column = 2, sticky = 'nesw')
   
   ###subtly important row configure
   #is the reason why search_frame expands when the window expands
   
   root.rowconfigure(index = 0, weight = 1)
   
   root.columnconfigure(index = 2, weight = 2)
   
   #need a list box so that the user can
   #browse through all the permuted components
   #and a search box that finds just one component
   #below all of these options, is the resistor_gui
   global browse_all_label
   
   browse_all_label_var = StringVar()
   
   browse_all_label_var.set('Browse through all components')
   
   browse_all_label = ttk.Label(master = search_frame, textvariable = browse_all_label_var)
   
   global browse_all_max_min_label_var
   
   browse_all_max_min_label_var = StringVar()
   
   browse_all_max_min_label_var.set('')
   
   browse_all_max_min_label = ttk.Label(master = search_frame, textvariable = browse_all_max_min_label_var)
   
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
   global current_component_list_box_key
   
   current_component_list_box_key = ''
   
   error_var = StringVar()
   
   error_label = ttk.Label(master = search_frame, textvariable = error_var)
   
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
      
      print(comp.toSaveStr())
      
      r_frame.draw_resistors(comp)
      
      error_var.set('')
      
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
            
            r_frame.draw_resistors(obj)
            
            per_error = fabs(float(obj)- val)/val * 100
            
            error_var.set('Percent Error: %.3f' % per_error)
            
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
   
   browse_all_max_min_label.grid(row = 2, column = 0, sticky = 'w')
   
   sub_frame.grid          (row = 4, column = 0, sticky = 'nesw')
   
   search_label.grid       (row = 3, column = 0, sticky = 'w')
   
   error_label.grid        (row = 5, column = 0, sticky = 'nwe')  

   r_frame.grid            (row = 6, column = 0, sticky = 'nesw')
      
   #search_frame.rowconfigure(index = 4, weight = 1)
   #search_frame.columnconfigure(index = 4, weight = 1)
   
   r_frame.draw_resistors(Component(components = [123,456,789], operation = extractValues.rParallel))
   
   distribute_weight(search_frame)
   
   return


    
    
        
def setup_routine():
   test_file = 'EE347_parts.txt'
   rValues   = extractValues.resistorValues(test_file)
   
   configuration = 'parallel'
   length = 2
   operation = extractValues.rParallel
   key = 'resistor' + '-' + configuration + '-' + str(length) + '[' + test_file + ']'

   permuted_components[key] = \
   extractValues.getComponentCombinations(rValues, length, operation, 'resistor ' + configuration)
   
   combo0 = Component((100, 100), operation, 'r parallel')
   operation = extractValues.rSeries
   
   combo1 = Component((50, 50, combo0), operation, 'r series')
   permuted_components[key].append(combo1)
   
   update_component_list_box()
   return  


# B A C K G R O U N D   F U N C T I O N S   F O R   O P E R A T I N G   T H E 
# P R O G R E S S   B A R

# ~ U P D A T E R ~
# 
# This function is a utility function
# This function uses root.after to keep calling itself.
# root.after calls a function after a period of time has past.
# calling updater on its first time automatically hooks itself into root.after
# updater will continue enlisting in hooking itself up to root.after every time 
# it is called.
# Until, updater finds a SENTINEL in the queue. updater then retrieves the return 
# value of the background process and passes it to a user provided finisher function.
# 'finisher' in the sense that it is called when the background process is finished.
#
# start_background is called with the permutation utility - combination
# AND with a freshly instantiated queue.
#
# see the 'permute' function embedded within create_component_frame. 
#
# It will push a SENTINEL and its
# return value into the queue when it is finished.
#
# AFTER the background process is started, permute_update_status is called.
# again see the 'permute' function that is embedded within create_component_frame
# the root window, after permute_update_status is called, continually calls
# permute_update_status until the background process pushes a SENTINEL (STOP VALUE)
# through the queue and a return value.

#S T A T E   V A R I A B L E S

SENTINEL = None
WAIT_FOR_SENTINEL = 0
WAIT_FOR_RETURN_LIST = 1
updater_state = 0

def updater(root, out_queue, finisher_func, *itsArgs, **itsKwArgs):

   global updater_state
   
   try:
   
      queue_obj = out_queue.get_nowait()
      
   except Queue.Empty:   
   
      root.after(250, updater, root, out_queue, finisher_func, *itsArgs, **itsKwArgs)
      
      return
   
   if updater_state == WAIT_FOR_SENTINEL:  
    
      if queue_obj == SENTINEL:
      
         updater_state = WAIT_FOR_RETURN_LIST
   
   elif updater_state == WAIT_FOR_RETURN_LIST:
      
      retval = queue_obj
      
      finisher_func(retval, *itsArgs, **itsKwArgs)
      
      progress_frame.getProgressBar().stop()
   
      progress_frame.hide()
      
      updater_state = WAIT_FOR_SENTINEL
      
      return
   
   root.after(250, updater, root, out_queue, finisher_func, *itsArgs, **itsKwArgs)
   return
   


def permute_finisher(retval, current_key, old_key):

   permuted_components[current_key] = retval
            
   update_component_list_box(old_key)
         
   #TODO: if there are more than 1 keys, then activate the 
   #pairing utility 
   return

   
      

def start_background(root, out_queue, func, *args, **kwargs):
   #take a normal function and make it so that it returns its
   #return value into out_queue
   
   def modified_func(passed_queue, args, kwargs):
   
      ret = func(*args, **kwargs)
      
      passed_queue.put(SENTINEL)
      
      passed_queue.put(ret)
      return
      
   proc = mp.Process(target=modified_func, args=(out_queue, args, kwargs))
   
   proc.daemon = True
   
   proc.start()
   return

        
def update_browse_all_list_box(*args):

   key = get_key_from_component_list_box()
   
   bag_of_parts = permuted_components[key]
   
   #update the global variable browse_all_list_box_var
   #it is declared in component_search_frame below 
   #Spagetti Code!!!
   
   progress_frame.show()
   
   progress_frame.setText('Updating Browse List Box...')
   
   pb = progress_frame.getProgressBar()
   
   pb.start()
   
   def wrapper(permuted_comp, keyy):
   
      l = components_to_string(permuted_comp, keyy)  
       
      l = tuple(l)
      return l
   
   que = mp.Queue()
   
   root = get_master(progress_frame)
   
   start_background(root, que, wrapper, permuted_components, key)
   
   def finished(retval, progress_b):
   
      pb = progress_b
      
      l = retval
      
      pb.stop()
   
      browse_all_list_box_var.set(l)
      
      maxa = to_eng_notation(permuted_components[key][-1])
      
      mina = to_eng_notation(permuted_components[key][0])
      
      browse_all_max_min_label_var.set('Max: %s Min: %s' % (maxa, mina))
      
      progress_frame.hide()
      return
      
   updater(root, que, finished, pb)                
   return
    
    

def get_master(widget):

   parent_name = widget.winfo_parent()
   
   parent = widget._nametowidget(parent_name)
   return parent


def update_component_list_box(old_key = ''):

   text = get_list_of_keys_from_dict(permuted_components)
   
   text = tuple(text)
   
   component_list_box_var.set(text)  
            
   #fix the component_list_box so it highlights the old selection
   try:
   
      key_index = text.index(old_key)
      
      #clear all the current idecies
      highlighted = component_list_box.curselection()
      
      for item in highlighted:
      
         component_list_box.selection_clear(item)
         
      component_list_box.selection_set(key_index)
      
   except ValueError:
      #old_key wasn't in list... oh well
      pass

   #if there are more than 2 items in the permuted_components dict
   #activate the pairing frame...
   if len(text) >= 1:
      tabbed_frame.tab(pairing_frame, state = 'normal')
      
   return



def save_components_to_python_file(permuted_components, key):

   default_file_name = str(key) + '.py'
   
   default_file_name = default_file_name.replace('-', '_')
   
   default_file_name = default_file_name.replace('[', '_')
   
   default_file_name = default_file_name.replace(']', '_')
   
   default_file_name = default_file_name.replace(' ', '_')
   
   default_file_name = default_file_name.replace('.txt', '')
      
   title = 'Saving Components: ' + str(key)
   
   #go to the home directory 
   file_name = fdialog.asksaveasfilename(initialfile = default_file_name, initialdir = settings_dict[SAVE_KEY], \
   title = title)
   
   if file_name == '':
      status_label_var.set('Save Cancelled...')
      return
           
   saved_dir = get_dir_from_path(file_name)      
   
   settings_dict[SAVE_KEY] = saved_dir
      
   out_file = file(file_name, 'w')
   
   out_file.write('from extractValues import Component\n')
   
   out_file.write('import extractValues\n')
   
   out_file.write('key_name = ' + '\''+ key + '\'\n')
   
   out_file.write('components = [\\\n')
   
   counter = 0
   
   for component in permuted_components[key]:
   
      append = ',\\\n'
      
      if counter == (len(permuted_components[key]) - 1):
      
         append = ']'   
         
      counter += 1
      
      statement = component.toSaveStr() + append
      
      out_file.write(statement)
      
   out_file.close() 
   
   save_usr_settings(settings_dict)
   
   return





def load_components_from_python_file(permuted_components):

   file_name = fdialog.askopenfilename(initialdir = settings_dict[LOAD_KEY])
   
   if file_name == '':
   
      raise ValueError('No file selected to load')
      
      return
      
   match = re.search('(.+)\.py', file_name)
   
   print(match.group(1))
   
   if not match:
   
      raise ValueError('Attempted to load a NON-python file')
      
      return 
         
   imp = match.group(1)
   
   imp.replace('.py', '')
   
   (directory, imp) = strip_path(imp)
   
   print(imp)
  
   sys.path.append(directory)
   
   mod = __import__(imp)
   
   key = mod.key_name
   
   components = mod.components
   
   permuted_components[key] = components
   
   path = get_dir_from_path(file_name)   
   
   settings_dict[LOAD_KEY] = path
   
   save_usr_settings(settings_dict)
   
   old_key = current_component_list_box_key
   
   update_component_list_box(old_key)
   
   return
   
   
   
   
   
def strip_path(path):
   
   for i in range(len(path)-1, 0, -1):
   
      if path[i] == '/':
      
         return (path[0: i], path[i+1 : len(path)] )
         
   return path   
   
   
   
   
   
def get_list_of_keys_from_dict(dictionary):

   return list(dictionary.keys())






def get_key_from_component_list_box():

   indecies = component_list_box.curselection()  
 
   if not indecies:
   
      msg = 'Please select an item from the Component List Box'
      
      raise Exception(msg)
          
   index = int(indecies[0])   
   
   keys = get_list_of_keys_from_dict(permuted_components)
   
   return keys[index]


   
   
    
def print_permuted_components_with_key(permuted_components, key):

   comp_list = permuted_components[key]
   
   for comp in comp_list:
   
      print(comp.toSaveStr())
      
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
   try:
      index = int(indecies[0])
      highlight_label_frame(file_frame, False)

   except IndexError as ie:
      msg_error = 'File wasnt selected in file frame'
      
      highlight_label_frame(file_frame, True)
      raise IndexError(msg_error)
      
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
         if afile[0] == '.' or afile[-1] == '~':
            continue
         valid_files.append(afile)
         
   return valid_files





def highlight_label_frame(label_frame, highlight):
   if highlight:
      label_frame['relief'] = RAISED
   else:
      label_frame['relief'] = FLAT
   return





if __name__ == '__main__':
   try:
      files = search_current_dir()
      
      main()
   except KeyboardInterrupt:
      sys.exit(1)   
   
