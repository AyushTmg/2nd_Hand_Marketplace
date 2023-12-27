from django import forms 
from .models import Item
from multiupload.fields import MultiFileField

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item 
        fields=['title','description','category','condition','location','price','is_negotiable']

class ImageForm(forms.Form):
    image = MultiFileField(min_num=1, max_num=10, max_file_size=10485760)