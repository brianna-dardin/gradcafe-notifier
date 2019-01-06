'''
This program runs the GUI that collects the information needed from the user to
check GradCafe for relevant results.
'''

from tkinter import *
from tkinter import ttk
import functions as func
from objectlist import ObjectList
import os
import pickle
import subprocess
import re
from datetime import datetime
import traceback

def main():
    # this creates the window of the app
    root = Tk()
    root.title("GradCafe Results Notifier")
    root.iconbitmap(os.path.join(file_path,"Coffee.ico"))
    root.resizable(width=False, height=False)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)	
    
    # this creates the structure for the tabbed screen
    n = ttk.Notebook(root)
    n.pack(fill='both', expand='yes')
    
    # this creates the two main tabs for the app
    titles = ['Manage Task','Help']
    mainframes = []
    for t in titles:
        main = ttk.Frame(n)
        main.pack(fill='both', expand=True)
        n.add(main, text=t)
        mainframes.append(main)
    
    # this creates the sections on the main tab
    sections = ['Basic Info','Fields of Study','Schools','Actions']
    frames = []
    for s in sections:
        # create frame object with label
        frame = ttk.Labelframe(mainframes[0], text=s)
        
        # this actually places all the frames onto the grid; otherwise they aren't visible
        frame.grid(sticky=E+W, pady=5, padx=10, ipady=2.5, ipadx=5)
        frames.append(frame)
    
    # this creates subsections within the first section of the tab
    # this is necessary because of the different sizes of the fields within it
    # without separate frames, the entry field for time gets stretched to the same
    # width as the email field which just looks bad
    subframes = []
    for i in range(2):
        sub = ttk.Frame(frames[0])
        sub.grid(sticky=E+W)
        subframes.append(sub)
    
    # the following creates the time and email variables used in the app and places them
    # within the first section
    hours = StringVar()
    ttk.Label(mainframes[0], text="Time").grid(in_=subframes[0], column=1, row=1, sticky=E)
    ttk.Entry(mainframes[0], width=5, textvariable=hours)\
        .grid(in_=subframes[0], column=2, row=1, sticky=(W, E))
    
    minutes = StringVar()
    ttk.Label(mainframes[0], text=":").grid(in_=subframes[0], column=3, row=1, sticky=E)
    ttk.Entry(mainframes[0], width=5, textvariable=minutes)\
        .grid(in_=subframes[0], column=4, row=1, sticky=(W, E))
    
    ampm = StringVar()
    ttk.OptionMenu(mainframes[0], ampm, "AM", *("AM", "PM"))\
        .grid(in_=subframes[0], column=5, row=1, sticky=(W, E))
    
    email = StringVar()
    ttk.Label(mainframes[0], text="Email").grid(in_=subframes[1], column=1, row=2, sticky=E)
    ttk.Entry(mainframes[0], width=50, textvariable=email)\
        .grid(in_=subframes[1], column=2, row=2, sticky=(W, E))
    
    # this checks to see if there was any previously saved data
    # if there is, then the app variables are set to these values
    # otherwise the default time is set and blank field and school variables are created
    og_data = func.get_data(file_path)
    if og_data != None and len(og_data) > 0:
        email.set(og_data["EMAIL"])
        hours.set(og_data["TIME"][0])
        minutes.set(og_data["TIME"][1])
        ampm.set(og_data["TIME"][2])
        
        field_list = create_list("Field",mainframes[0],frames[1],og_data["FIELDS"])
        school_list = create_list("School",mainframes[0],frames[2],og_data["SCHOOLS"])
    else:
        hours.set("12")
        minutes.set("00")
        ampm.set("AM")
        
        field_list = create_empty("Field",mainframes[0],frames[1])
        school_list = create_empty("School",mainframes[0],frames[2])
    
    # this creates a dictionary with all the relevant information so that it can be
    # easily passed into the button functions
    data = {}
    data["EMAIL"] = email
    data["TIME"] = [hours, minutes, ampm]
    data["FIELDS"] = field_list.objects
    data["SCHOOLS"] = school_list.objects
    
    # these create the buttons to carry out the main tasks of the app
    ttk.Button(mainframes[0], text="Create/Update Task", command=lambda: create_task(data))\
        .grid(in_=frames[3], column=1, row=1, sticky=W)
        
    ttk.Button(mainframes[0], text="Clear Data", command=lambda: clear_data(data))\
        .grid(in_=frames[3], column=2, row=1, sticky=(W,E))
        
    ttk.Button(mainframes[0], text="Delete Task", command=delete_notif)\
        .grid(in_=frames[3], column=3, row=1, sticky=E)
        
    # this sets up the help tab with a scrollbar
    # adapted from https://stackoverflow.com/questions/36575890/how-to-set-a-tkinter-window-to-a-constant-size
    canvas = Canvas(mainframes[1])
    f2a = ttk.Frame(canvas)
    f2a.pack_propagate(0)
    f2a.pack(fill='both', expand=True)
    myscrollbar = Scrollbar(mainframes[1],orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=f2a,anchor='nw')
    
    # this was the shortest width I could use without making the help text display weirdly
    help_width = 452
    
    def scroll_function(event):
        canvas.configure(scrollregion=canvas.bbox("all"),width=help_width,height=mainframes[0].winfo_height())
    f2a.bind("<Configure>",scroll_function)
    
    # once the help tab is configured, get the help text and display it
    with open(os.path.join(file_path,"helptext.txt"), "r") as fp:
        help_text = fp.read()
    
    ttk.Label(f2a, text=help_text, wraplength=help_width).grid(column=1, row=1, sticky=W)
    
    # this is used once the UI is set up so that the app can run and track any mouse events    
    root.mainloop()

# this function creates the field and school lists assuming there is previous data
def create_list(name, parent, frame, data):
    if len(data) > 0:
        obj_list = ObjectList(name, parent, frame, data)
        obj_list.add_rows()
    else:
        obj_list = create_empty(name, parent, frame)
    return(obj_list)

# this creates the field and school lists if there is no previous data
def create_empty(name, parent, frame):
    obj_list = ObjectList(name, parent, frame)
    obj_list.add_row()
    return(obj_list)

# this is the primary function that creates the scheduled task
def create_task(data):
    # all the variables created before were objects used by tkinter to track user input
    # once it's time to commit the answers, the final input needs to be extracted
    new_data = {}
    new_data["EMAIL"] = data["EMAIL"].get()
    new_data["TIME"] = get_values(data["TIME"])
    
    # this app does a simple check to make sure that the email entered can receive the emails
    # it also ensures that the entered time is valid
    valid_email = verify_email(new_data["EMAIL"])
    valid_time = verify_time(new_data["TIME"])
    
    if valid_email["valid"]:
        if valid_time["valid"]:
            # wrapping this code in a try/except block since these errors aren't caught
            # by the try/except for main()
            try:
                # if both the email and time are valid, we can continue processing the data
                new_data["FIELDS"] = get_values(data["FIELDS"])
                new_data["SCHOOLS"] = get_values(data["SCHOOLS"])
                
                # this program is designed for people who want to track results for certain programs
                # there is no need for notifications if you want to see everything; just go to the website
                # therefore if the user submits without input (or clicks the button by mistake)
                # this raises an error preventing a task from being created
                if len(new_data["FIELDS"]) < 1 and len(new_data["SCHOOLS"]) < 1:
                    raise ValueError("At least one field of study or one school is required. Please try again.")
                
                # once all the data is processed, it is pickled (or saved) to a file
                # so that it can be used by the scheduled task program
                with open(data_path, "wb") as fp:
                    pickle.dump(new_data, fp)
                
                # delete the preexisting task if it exists
                delete_task()
                
                # setup the task path and time for the scheduled task
                task = '"' + os.path.join(file_path,"gradcafeutility.exe") + '" '
                task += '"' + file_path + '"'
                time = datetime.strftime(valid_time["time"],"%H:%M")
                
                # create the task and display result to the user
                command = [schtasks,'/CREATE','/SC','DAILY','/TN',task_name,'/TR',task,'/ST',time]
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
                                        stdin=subprocess.DEVNULL)
                new_window("Result",proc.stdout.read())
            except Exception as e:
                func.log_error(file_path,"Main",e,traceback.format_exc())
                new_window("Error",str(e))
        else: # display error if time is invalid
            new_window("Error",valid_time["message"])
    else: # display error if email is invalid
        func.log_error(file_path,"Main",valid_email["message"],valid_email["trace"])
        new_window("Error",valid_email["message"])

# this extracts the values from a list of app variables
def get_values(data):
    new_data = []
    if len(data) > 0:
        for d in data:
            if len(d.get()) > 0 and d.get().isspace() == False:
                new_data.append(d.get())
    return(new_data)

# basic email verification to ensure the email can be sent
# adapted from https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
def verify_email(email):        
    response = {}
    
    # this checks to see if the email matches the basic format (user@domain.com)
    # no need to ping the server if the input doesn't meet this requirement
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        response["valid"] = False
        response["message"] = "Invalid email syntax. Please type your email again."
        return(response)
    
    # ping the email server to verify the email works
    valid_connection = func.setup_email(email)
    if valid_connection["valid"]:
        server = valid_connection["server"]
        server.mail(valid_connection["username"])
        code, message = server.rcpt(email)
        server.quit()
        
        # Assume 250 as Success
        if code == 250:
            response["valid"] = True
            return(response)
        else:
            response["valid"] = False
            response["message"] = "Bad response from email server. Please use a different email."
            return(response)
    else:
        return(valid_connection)

# this ensures the time input is a valid time by seeing if the text can be converted
# to a datetime object
def verify_time(time_data):
    response = {}
    try:
        time_string = ":".join(time_data[0:2]) + " " + time_data[-1]
        time = datetime.strptime(time_string, "%I:%M %p")
        
        response["valid"] = True
        response["time"] = time
        return(response)
    except Exception as e:
        response["valid"] = False
        response["message"] = "Invalid time input. Please try again."
        return(response)

# this deletes the scheduled task
def delete_task():
    # check whether one already exists
    old_task = [schtasks,'/QUERY','/TN',task_name]
    old_proc = subprocess.Popen(old_task, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
                                stdin=subprocess.DEVNULL)
    
    # if one exists, delete it
    if "error" not in str(old_proc.stdout.read()).lower():
        delete_command = [schtasks,'/DELETE','/TN',task_name,'/F']
        proc = subprocess.Popen(delete_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
                                stdin=subprocess.DEVNULL)
        return(proc.stdout.read())
    else:
        return(old_proc.stdout.read())

# helper function to create a new window for displaying success or error messages
def new_window(title,text):
    newroot = Tk()
    newroot.title(title)
    newroot.columnconfigure(0, weight=1)
    newroot.rowconfigure(0, weight=1)	
    
    mainframe = ttk.Frame(newroot)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    frame = ttk.Labelframe(mainframe)
    frame.grid(pady=4, padx=4, ipady=4, ipadx=4)
    
    ttk.Label(mainframe, text=text, wraplength=300).grid(in_=frame, column=1, row=1, sticky=(W,E))
    ttk.Button(mainframe, text="Close", command=newroot.destroy)\
        .grid(in_=frame, column=1, row=2, sticky=(W,E))
    
    # this ensures the new window is in focus when it is generated    
    newroot.focus_force()

# this sets all the app variables to empty values and deletes the file with the saved values
def clear_data(data):
    if len(data) > 0:
        for d in data:
            if "EMAIL" in d:
                data[d].set('')
            else:
                for i, s in enumerate(data[d]):
                    data[d][i].set('')
    
    if os.path.isfile(data_path):
        os.remove(data_path)

# this is used for the delete button to ensure the result is displayed in a new window
def delete_notif():
    new_window("Result",delete_task())

if __name__ == "__main__":
    # these variables are used in multiple functions so declare them first
    schtasks = r"C:\Windows\System32\schtasks.exe"
    task_name = "GradCafe Results Notification"
    file_path = os.path.join(os.getcwd(),"files")
    data_path = os.path.join(file_path,"variables.txt")
    
    # wrap the app in a try/except block and show the user any errors and also log them
    try:
        main()
    except Exception as e:
        func.log_error(file_path,"Main",e,traceback.format_exc())
        new_window("Error",str(e))