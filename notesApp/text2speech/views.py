from django.shortcuts import render, redirect
from .models import NotesDb
from django.core.files.storage import FileSystemStorage
from .forms import NoteUpload, DBQuery
# custom import
from django.core.files.storage import FileSystemStorage  # this is needed to Save files to the filesystem
from django.core.files.storage import default_storage

from django.conf import settings
#import needed for the the conversion
from datetime import datetime

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
    basefile = settings.MEDIA_ROOT
    print(BASE_DIR)
    if request.method=='POST':
        form = NoteUpload(request.POST, request.FILES)
        if form.is_valid():
            notes = form.save()
            userid = notes.user
            keyword = notes.title
            textfile = notes.textfile.name
            f = default_storage.open(textfile, 'r')
            file = f.read()
            f.close()

            textfile=basefile+"/"+textfile
            date_time_obj = datetime.now()
            filename = str(date_time_obj.month).zfill(2) + str(date_time_obj.day).zfill(2) + \
                       str(date_time_obj.year).zfill(4) + "_" + str(date_time_obj.hour).zfill(2) + \
                       str(date_time_obj.minute).zfill(2) + str(date_time_obj.second).zfill(2) + ".wav"
            python_file= BASE_DIR+"/scratch_main.py"
            speechfile = "/mnt/Audiofiles/audiofiles/combined/" + filename
            command2run = "mpirun -n 3 python3 "+python_file+ " " + textfile + " " \
                          + filename
            #print(command2run)
            os.system(command2run)
            wavefile = open(speechfile,'rb')
            django_wvfile=File(wavefile)
            notes.wavfile.save(str(wavefile),django_wvfile,save=True)

    else:
        form = NoteUpload()
        file_path = ''
        textfile=''
        file_path = ''
        file=''
        #wv=''
        wv2b=''
        userid=''
    return render(request,"upload.html",{'form':form,'txt':basefile,'userid':userid})

def listen(request):
    entry = ""
    user = ""
    keyword = ""
    notes = NotesDb.objects.filter(user__iexact=user)
    if request.method=='POST':
        form = DBQuery(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            keyword = form.cleaned_data.get("keyword")
            form = DBQuery()
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
        form = DBQuery()
        entry = ""


    return render(request,"listen.html",{'form': form, 'user':user, 'keyword':keyword,'notes':notes,'entry':entry})


def about(request):
    return render(request,"about.html")