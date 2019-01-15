from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл'
    )
    docfile.widget.attrs.update({'class' : 'form-control-file'})
