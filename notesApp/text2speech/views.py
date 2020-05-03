from django.shortcuts import render, redirect
from .models import NotesDb
from django.core.files.storage import FileSystemStorage
from .forms import NoteUpload, RegularForm
# custom import
from django.core.files.storage import FileSystemStorage  # this is needed to Save files to the filesystem
from django.core.files.storage import default_storage
from django.conf import settings
import os
#import needed for the the conversion
from datetime import datetime
import sys
import glob
import shutil
import os
from django.core.files import File  # To write to FileField of database

# Create your views here.
def home(request):
    return render(request,"home.html")

def list_notes(request):
    notes=NotesDb.objects.all()
    return render(request, 'notes_list.html', {'notes': notes})

def sampleForm(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    if request.method=='POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        file = fs.open(name, 'rb')
        filetype=str(type(file))
    else:
        form = RegularForm()
        tfile_name= ''
        file_path = ''
        file=''
        filetype =""

    return render(request,'sampleForm.html',{'txtfile':filetype})

def upload(request):
    basefile = settings.MEDIA_ROOT
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
            speechfile = "/mnt/Audiofiles/audiofiles/combined/" + filename
            command2run = "mpirun -n 3 python3 /home/mpiuser/code/notesapp/notesApp/text2speech/scratch_main.py " + textfile + " " \
                          + filename +" " +speechfile
            os.system(command2run)
            wavefile = open(speechfile,'rb')
            django_wvfile=File(wavefile)
            notes.wavfile.save(str(wavefile),django_wvfile,save=True)
            """wv=str(type(wavefile))
            wv2=notes.wavfile
            wv2b=str(type(wv2))"""
            #notes.wavfile=wavefile
            #notes.save
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