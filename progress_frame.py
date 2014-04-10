#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
import sys

#compatibility between python2 and python3
if sys.version_info[0] == 2:
   import Tkinter
   from Tkinter import *
   import ttk
else:
   import tkinter
   from tkinter import *
   from tkinter import ttk


class ProgressFrame(ttk.Frame):

   def __init__(self, *args, **kwargs):
      ttk.Frame.__init__(self, *args, **kwargs)

      progress_bar = ttk.Progressbar(master = self, orient = HORIZONTAL, mode = 'indeterminate')         
      progress_bar.grid(row = 0, column = 1, sticky = 'we')
   
      progress_label_var = StringVar()
      progress_label = ttk.Label(master = self, textvariable = progress_label_var)
      progress_label.grid(row = 0, column = 0, sticky = 'we')
   
      self.progress_bar = progress_bar
      self.progress_label = progress_label  
      self.progress_label_var = progress_label_var    
      return
   
   def hide(self):
      self.progress_bar.grid_remove()
      self.progress_label.grid_remove()
      return
   
   def show(self):
      self.progress_bar.grid()
      self.progress_label.grid()
      return
   
   def setText(self, text):
      self.progress_label_var.set(text)
      return
   
   def getProgressBar(self):
      return self.progress_bar   
