from django.shortcuts import render

# Imports the database and the forms created in files models.py and forms.py
from .models import NotesDb
from .forms import NoteUpload, DBQuery
#-----------------------------------------------------------------------

#Needed for opening
from django.core.files.storage import default_storage

from django.conf import settings
#import needed for the the conversion
from datetime import datetime
import time
import os
from django.core.files import File  # To write to FileField of database
# Gets the path for this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def home(request):
    return render(request,"home.html")

def list_notes(request):
    notes=NotesDb.objects.all()
    return render(request, 'notes_list.html', {'notes': notes})



def upload(request):
    #basefile is the directory where the uploaded files are saved. Configured in settings.py
    basefile = settings.MEDIA_ROOT
    #Initializes the default number of MPI processes
    nprocs ='1'
    elapsed=0
    if request.method=='POST':  # Executed when the upload button is pressed
        start_time=time.time()
        # ties form to the database
        form = NoteUpload(request.POST, request.FILES)
        if form.is_valid():
            # Saves the user input to the database
            notes = form.save()
            # Extracts the number processors from the form input
            nprocs = request.POST['nprocs']
            # Extracts the file name from the form input
            textfile = notes.textfile.name

            # Clears the form entries on the web page
            form = NoteUpload()

            textfile=basefile+"/"+textfile
            date_time_obj = datetime.now()
            filename = str(date_time_obj.month).zfill(2) + str(date_time_obj.day).zfill(2) + \
                       str(date_time_obj.year).zfill(4) + "_" + str(date_time_obj.hour).zfill(2) + \
                       str(date_time_obj.minute).zfill(2) + str(date_time_obj.second).zfill(2) + ".wav"
            python_file= BASE_DIR+"/main.py"
            speechfile = "/mnt/Audiofiles/audiofiles/combined/" + filename

            # sets up the command to execute the mpirun -- another option is used .Spawn; however, we couldn't get this
            # to work
            command2run = "mpirun -n "+nprocs+" python3 "+python_file+ " " + textfile + " " \
                          + filename
            # Runs the mpirun command
            os.system(command2run)

            # This section takes the saved combined file and upload it to the database
            wavefile = open(speechfile,'rb')
            django_wvfile=File(wavefile)
            notes.wavfile.save(str(wavefile),django_wvfile,save=True)

            msg_done="The file has been uploaded to the database"
            end_time = time.time()
            elapsed = end_time - start_time

    else:
        # This shows an empty upload.html page during the "GET" request
        form = NoteUpload()
        msg_done =''


    return render(request,"upload.html",{'form':form,'nprocs':nprocs,'msg':msg_done,'time':elapsed})

# This function controls the database query
def listen(request):
    entry = ""
    user = ""
    keyword = ""
    notes = NotesDb.objects.filter(user__iexact=user)
    if request.method=='POST':  #executed when the From From Database button is pressed
        form = DBQuery(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            keyword = form.cleaned_data.get("keyword")
            form = DBQuery()
            # Does some filtering to incorporate wildcards
            if (user == '*' and keyword =='*'):
                notes=NotesDb.objects.all()
            elif (user =='*'):
                notes = NotesDb.objects.filter(title__icontains=keyword)
            elif (keyword=='*'):
                notes = NotesDb.objects.filter(user__iexact=user)
            else:
                notes=NotesDb.objects.filter(user__iexact=user).filter(title__icontains=keyword)
            if len(notes) < 1:
                entry="Query didn't return Anything"
    else:
        # when the HTTP request is GET
        form = DBQuery()
        entry = ""


    return render(request,"listen.html",{'form': form, 'user':user, 'keyword':keyword,'notes':notes,'entry':entry})

# Renders the About page
def about(request):
    return render(request,"about.html")