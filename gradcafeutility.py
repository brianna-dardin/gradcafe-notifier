'''
This program scrapes the GradCafe website using the user-provided options and
if any new results are found, emails the user
'''

import sys
import functions as func
from urllib import parse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import traceback

def main():
    # get the previously saved data and raise an error if nothing was saved
    variables = func.get_data(path)
    if variables == None or len(variables) < 1:
        raise ValueError("Answers not saved.")
    
    # format the search string for the fields and schools
    school_string = get_string(variables["SCHOOLS"])
    field_string = get_string(variables["FIELDS"])
    
    # set up the request URL and ensure it's URL encoded
    # t=t tells the website to look only at results from the last 2 days
    base_url = 'https://www.thegradcafe.com/survey/index.php?t=t&q='
    search_query = school_string + ' ' + field_string
    request_url = base_url + parse.quote_plus(search_query)
    
    # while it is probably unlikely most search queries will have more than a page
    # of results in only 2 days, this loop checks to see if there are
    # in which case it will request the next page of results and process those
    # until there is less than a page of results left
    yesterdays_results = []
    page = 1
    while True:
        new_url = request_url + '&p=' + str(page)
        
        # this gets all the results from the current page
        all_results = get_results(new_url)
        
        # this adds any results from yesterday to the list containing the results
        # from all the pages
        for r in all_results["yesterday"]:
            yesterdays_results.append(r)
        
        # if there is less than a full page worth of results, break the loop
        if len(all_results["all"]) < 25:
            break
        
        # increment page count if there are potentially more results
        page += 1
    
    # if any results from yesterday were found, send the email                
    if len(yesterdays_results) > 0:
        # create text version of email
        text = "Check the website for more info\n\n"+request_url
        
        # this creates the html version of the email by creating a table with all the results
        html = '<html><head></head><body>'
        html += '<p><a href="'+request_url+'">Check the website for more info</a></p>'
        html += '<table>'
        for fld in yesterdays_results:
            html += '<tr>'
            for f in fld:
                html += str(f)
            html += '</tr>'
        html += '</table></body></html>'
        
        # create the email server and send the email
        valid_connection = func.setup_email(variables["EMAIL"])
        if valid_connection["valid"]:
            server = valid_connection["server"]
            
            # create email header
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'New GradCafe Admissions Results'
            msg['From'] = valid_connection["username"]
            msg['To'] = variables["EMAIL"]
            
            # set the text/plain and text/html parts of the email and attach them to message
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            server.sendmail(valid_connection["username"], variables["EMAIL"], msg.as_string())
            server.quit()
        else:
            func.log_error(path,"Utility",valid_connection["message"],valid_connection["trace"])
    else:
        # while not an error, this simply keeps track of every execution of the program
        func.log_error(path,"Utility","No new results posted.",'')

# this converts the field and school lists to the proper OR syntax recognized by GradCafe
def get_string(data):
    if len(data) > 0:    
        for i, s in enumerate(data):
            # input with spaces needs to have quotes around it to ensure the entire phrase
            # is properly searched
            if len(s.split(" ")) > 1:
                data[i] = '"' + s + '"'
        string = '(' + '|'.join(data) + ')'
    else:
        # if no fields or schools are specified, don't add anything to the query
        string = ''
    return(string)

# this submits the GET request to the URL and handles the results
# finding all results and parsing them to find yesterday's were separated into
# different functions so that they can be used separately in the while loop
def get_results(request_url):
    r = requests.get(request_url)
    r.raise_for_status()
    
    response = {}
    response["all"] = find_results(r.text)
    response["yesterday"] = parse_results(response["all"])
    return(response)
        
def find_results(text):   
    # parse the HTML and find the table with the results
    soup = BeautifulSoup(text, "lxml")
    result_table = soup.find("table", {"class": "submission-table"})
    
    # raise an error if the main table isn't found or if there are no rows in the table
    # otherwise return all the rows of the table
    if result_table == None:
        raise ValueError("Admissions results table not found")
    else:
        results = result_table.find_all("tr")
        if len(results) < 1:
            raise ValueError("No results found.")
            
    return(results)

# this iterates through the results found above to find any posted yesterday    
def parse_results(results):
    new_results = []
    for res in results:
        # find all the columns in each row and iterate over them
        fields = res.find_all("td")
        if len(fields) > 0:
            for f in fields:
                # if the column contains the date it was posted, extract the date
                # and check whether it is yesterday's date
                # if it is, then add it to the list
                if "datecol" in f.get("class"):
                    date = datetime.strptime(f.get_text(), '%d %b %Y').date()
                    if date == yesterday:
                        new_results.append(fields)
    return(new_results)

if __name__ == "__main__":
    # wrap the program in a try/except block and log any errors
    try:
        # all scheduled tasks are run in C:\Windows\System32 so they don't have access to 
        # the original files, therefore the file path was added as an argument to the task
        # this extracts the argument so the saved data can be found
        # otherwise log an error by creating a log file in the user's Documents folder
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = os.path.expanduser("~\Documents")
            raise ValueError("No file path argument given.")
            
        # calculate what day yesterday here in case there are multiple pages of results
        yesterday = datetime.today().date() - timedelta(days=1)
        
        main()
    except Exception as e:
        func.log_error(path,"Utility",e,traceback.format_exc())