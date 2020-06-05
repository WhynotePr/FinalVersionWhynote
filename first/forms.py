from django import forms
from first.models import *
from django.forms import ModelForm, TimeInput, DateInput

from django.contrib.auth.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

class UserProfileInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        widgets = {
            'day': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            }
        fields = ('eventtitle', 'day', 'start_time', 'end_time', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ('eventtitle', 'day', 'start_time', 'end_time', 'notes')
        self.fields['eventtitle'].widget.attrs['placeholder'] = 'Title'
        self.fields['day'].input_formats = ('%Y-%m-%d',)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)
        #
        #self.fields['start_time'].required = False
        #self.fields['end_time'].required = False
        self.fields['notes'].required = False
        self.fields['notes'].widget.attrs['placeholder'] = 'Notes'
        for f in fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'note_title',
            'note_text',
            'tag',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note_title'].widget.attrs['placeholder'] = 'Title'
        self.fields['tag'].widget.attrs['placeholder'] = 'Folder'
        self.fields['note_title'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['class'] = 'form-control'


class BookForm(forms.ModelForm):
    """For uploading pdf files"""

    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')
        # widgets = {
        #     'title' : forms.Textarea(attrs={
        #         'maxlength': '10',
        #     }),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ('title', 'author', 'pdf', 'cover')
        self.fields['title'].widget.attrs['placeholder'] = 'Title (not required)'
        self.fields['author'].widget.attrs['placeholder'] = 'Author (not required)'
        self.fields['pdf'].widget.attrs['placeholder'] = 'File'
        self.fields['cover'].widget.attrs['placeholder'] = 'Cover'
        self.fields['author'].required = False
        for f in fields[:2]:
            self.fields[f].widget.attrs['class'] = 'form-control'

