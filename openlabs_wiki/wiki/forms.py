from django import forms

class ImageForm(forms.Form):
    imagefile = forms.ImageField(
        label='Select a file',
    )
