'''
This module is for helper functions that are used in both the GUI app and the scheduled task
'''

import os
import pickle
from datetime import datetime
from secret import smtp_server, port, username, password
import smtplib
import traceback

# this fetches the data from the saved file if it still exists
def get_data(path):
    data_path = os.path.join(path,"variables.txt")
    
    if os.path.isfile(data_path):
        with open(data_path, "rb") as fp:
            variables = pickle.load(fp)
        return(variables)
    else:
        return(None)

# this logs the error with stack trace to a log file
def log_error(path, program, err, tb):
    with open(os.path.join(path,"log.txt"),'a') as log:
        now = datetime.strftime(datetime.now(), '%d %b %Y %H:%M:%S')
        log.write(now+" ("+program+"): "+str(err)+"\n"+tb)

# this creates the connection with the email server used to send the email
# the credentials are stored in the secret module
def setup_email(email):
    connection = {}
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password) 
        server.set_debuglevel(0)
        
        connection["valid"] = True
        connection["server"] = server
        connection["username"] = username
        return(connection)
    except Exception as e:
        connection["valid"] = False
        connection["message"] = e
        connection["trace"] = traceback.format_exc()
        return(connection)
