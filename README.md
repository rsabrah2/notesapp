Introduction to Our Project
===========================
Directory Structure
-------------------
**1. notesApp**  
Contains all the files developed for this project  

***`Important sub folders for this project`***
1. notesApp  
* settings.py  
   Contains the configuration information for the Django project.
* urls.py  
   This file lists the URL information at a project level. Used to determine how to handle the URL requests. 

2. text2speech  
   Contains the python code files. Following are the ones used for this project
   * views.py  
     Contains the main codes that control the whole app
     Functions include:
     * home : renders the home page
     * list_notes: renders the page that shows all the notes saved on the database
     * upload: code used to read the user entry and calls the function to create the combined wave file and upload to database
     * listen: code to query the database based on user input
     * about: render the about page
   * models.py  
     Used to define the fields of the database table. 
   * forms.py  
     Defines the forms used for user entry
   * urls.py
     Similar to the project level file, this file lists the URL information at a project level.
   * main.py  
     Contains the code that performs the MPI execution of the text-2-speech conversion
   * functions.py  
     Separate file created to handle the functions called in main.py
3. templates  
   Contains the html files created for this  project
4. media  
   Contains the media files used in this project - includes the audio file, as well as the text file
   


  
**2. textfiles**  
    Contains the notesfiles we used for testing  


**3. vnotes**  
   Contains the virtual environment settings we used to test our app

**4. TestCodes**  
    Trial version of the code

