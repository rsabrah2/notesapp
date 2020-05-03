from django import forms
from .models import NotesDb

class NoteUpload(forms.ModelForm):
    class Meta:
        model=NotesDb
        fields = ('user','title','textfile','wavfile')


class RegularForm(forms.Form):
    user = forms.CharField(max_length=100)
    keyword = forms.CharField(max_length=100)
    textfile = forms.FileField(allow_empty_file=True)

