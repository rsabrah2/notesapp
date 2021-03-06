from django.db import models
from django.utils import timezone
# Create your models here.
# Each variable specified here will be a database field
# Django automatically adds a primary key
class NotesDb(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    textfile= models.FileField(upload_to='NotesFile')
    wavfile= models.FileField(upload_to='WavFile', null=True, blank=True)
    timestamp=models.DateTimeField(default=timezone.now)