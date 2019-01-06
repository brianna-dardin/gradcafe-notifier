'''
This class manages the data and widgets for the fields of study and the schools
'''

from tkinter import *
from tkinter import ttk

# inspired by https://stackoverflow.com/a/11451658/6553925
class ObjectList(object):
    def __init__(self, name, parent, frame, objects = None):
        self.name = name
        self.parent = parent
        self.frame = frame
        
        # if previous data exists, create and assign variables with those values
        self.objects = []
        if objects != None and len(objects) > 0:
            for i, s in enumerate(objects):
                self.objects.append(StringVar())
                self.objects[i].set(s)
        
        # the button is created through the other methods, this just ensures the variable exists
        self.button = None
    
    # this adds a new blank row to the bottom of the list    
    def add_row(self):
        self.objects.append(StringVar())
        
        label_number = len(self.objects)
        row_number = label_number - 1
        
        self.create_widgets(row_number,label_number)
    
    # this creates all the widgets for all the objects    
    def add_rows(self):
        for i, obj in enumerate(self.objects):
            self.create_widgets(i,i+1)
    
    # this function is used to create the widgets for the above methods
    def create_widgets(self,row_number,label_number):
        # this ensures the previously created add button is removed
        # so that it can be moved below the row widgets
        if 'button' in locals() and self.button != None:
            self.button.destroy()
        
        # create the widgets for this row and place them on the grid
        ttk.Label(self.parent, text=self.name+" #"+str(label_number))\
            .grid(in_=self.frame, column=1, row=row_number, sticky=E)
        
        ttk.Entry(self.parent, width=50, textvariable=self.objects[row_number])\
            .grid(in_=self.frame, column=2, row=row_number, sticky=(W, E))
        
        ttk.Button(self.parent, text="Remove", command=lambda: self.delete_row(row_number))\
            .grid(in_=self.frame, column=3, row=row_number, sticky=W)
        
        # recreate the add button
        self.button = ttk.Button(self.parent, text="Add "+self.name, command=self.add_row)
        self.button.grid(in_=self.frame, column=2, row=label_number, sticky=W)
    
    # this deletes a given row
    def delete_row(self, row_number):
        # at least one row of widgets is needed to stay on the screen 
        # so the user can still interact with the class
        if len(self.objects) > 1:
            # remove the button
            self.button.destroy()
            
            # create a new list to store the object list without the removed row
            new_objects = []
            for i, obj in enumerate(self.objects):
                if i != row_number:
                    new_objects.append(obj)
            
            # remove all widgets from the frame
            for w in self.frame.grid_slaves():
                w.destroy()
            
            # clear the instance object list and remove the frame from the grid
            self.objects.clear()
            self.frame.grid_remove()
            
            # add the new object list to the instance list
            for obj in new_objects:
                self.objects.append(obj)
            
            # create the new widgets and place the frame back on the grid
            self.add_rows()
            self.frame.grid()
        else:
            # set the only object in the list to an empty string
            # instead of removing anything from the screen
            self.objects[0].set('')