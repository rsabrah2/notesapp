from django import forms
from .models import NotesDb

# Creates forms to input values int the fields User, Title, and Textfile of the database
class NoteUpload(forms.ModelForm):
    class Meta:
        model=NotesDb
        fields = ('user', 'title', 'textfile')


# Creates form used to enter the query criteria
class DBQuery(forms.Form):
    user = forms.CharField(max_length=100)
    keyword = forms.CharField(max_length=100)


