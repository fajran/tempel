from django import forms

from tempel import utils

class EntryForm(forms.Form):
    language = forms.ChoiceField(choices=utils.get_languages(),
                                 initial="python")
    content = forms.CharField(widget=forms.Textarea)
    private = forms.BooleanField(required=False)

class EditForm(forms.Form):
    language = forms.ChoiceField(choices=utils.get_languages(),
                                 initial="python")
    content = forms.CharField(widget=forms.Textarea)

