# GradCafe Results Notifier

The bane of every aspiring grad student's existence is GradCafe, or more specifically, the admissions results that are posted in their database. The urge to visit the site and refresh it can sometimes be overwhelming in the face of the anxiety over getting in. To help assuage my own anxiety in the wake of my PhD applications, I decided to create a simple app that will notify me - and anyone else who chooses to use it - when there are any updates on the site, so the time spent refreshing the website can instead be put to better use!

This app was written completely in Python, with the GUI developed in gradcafe.py (and supported by objectlist.py) and the program that is triggered by the scheduled task is in gradcafeutility.py. Both programs are supported by functions.py and secret.py and were compiled into executables using the batch files and version information files in the exe folder.

### Install

The compiled program can be downloaded from [here](https://drive.google.com/file/d/17-EH8qmT2iMD2Am4sM5kifoD4vysTMfX/view?usp=sharing). Simply unzip and run gradcafe.exe!

### Usage
[This screenshot](https://i.imgur.com/9Ic0jQN.png) shows what the GUI looks like. The following description is taken from the help text embedded in the app:

This program creates a scheduled task that will email you once a day if anyone has posted any new results on GradCafe under the fields of study and the schools you specify on the main screen.
             
To get started, enter the time you wish to receive the email. This program works by checking for all the results posted on the previous day. Also, the default time displayed on the GradCafe site when not logged in appears to be US East Coast time, so please keep that in mind when scheduling the task. The default time of midnight should be sufficient for most users in North and South America, otherwise I would recommend calculating what time it is in your timezone when it is midnight on the North American east coast for optimal results.

Then enter email you want the notification to be sent to. The email will be coming from "gradcafenotifier@gmail.com", which shouldn't be blocked by your email server, but you may want to whitelist it just in case.

Then you can enter the programs/fields of study and the schools you wish to track. Once you are done, click the Create/Update Task button to create the scheduled task.
    
If you ever wish to change what you are looking for, simply open this application again, change your answers, and click the Create/Update Task button.

If you want to remove all the previously set values, click the Clear Data button.
    
If you no longer want to receive the emails, you can click the Delete Task button.
    
If anything breaks or if you have any questions, please feel free to contact the developer, Brianna Dardin, at brianna.dardin@gmail.com
    
Thank you for downloading and I hope you find this tool useful! :)
