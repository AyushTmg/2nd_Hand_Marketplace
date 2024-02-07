from django import forms 
from .models import Item,Comment,Reply
from multiupload.fields import MultiFileField,MultiImageField



# ! Form for Item
class ItemForm(forms.ModelForm):
    class Meta:
        model=Item 
        fields=[
            'title',
            'description',
            'category',
            'condition',
            'location',
            'price',
            'is_negotiable'
        ]




# ! Form for Item Image
class ImageForm(forms.Form):
    image = MultiFileField(min_num=1, max_num=5, max_file_size=10485760)




# ! Form for Comment on Item
class CommentForm(forms.ModelForm):
    class Meta: 
        model=Comment
        fields=['description']




# ! Form for Reply for comment
class ReplyForm(forms.ModelForm):  
    class Meta:
        model=Reply
        fields=['description']




