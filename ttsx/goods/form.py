from django import forms


class image(forms.Form):
    icon = forms.ImageField()
    name = forms.CharField()