from django import forms

class InputForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea)

class OutputForm(forms.Form):
    output = forms.CharField(widget=forms.Textarea)

class OneMoreInputForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea)