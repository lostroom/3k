from django import forms

from .models import Worker

from django_select2.forms import Select2Widget

class MyForm(forms.Form):
    #worker = forms.ModelChoiceField(queryset=Worker.objects.all())
    choose_1st_fighter = forms.ModelChoiceField(queryset=Worker.objects.all(), label='First worker')
    choose_2st_fighter = forms.ModelChoiceField(queryset=Worker.objects.all(), label='Second worker')
    choose_1st_fighter.widget.attrs.update({'class' : 'form-control'})
    choose_2st_fighter.widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Worker
        fields = ['choose_1st_fighter', 'choose_2st_fighter']


class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл'
    )
    docfile.widget.attrs.update({'class' : 'form-control-file'})
