from django.db import models

# Create your models here.
class NotesDb(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    textfile= models.FileField(upload_to='NotesFile')
    wavfile= models.FileField(upload_to='WavFile', null=True, blank=True)