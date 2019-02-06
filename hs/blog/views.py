from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Worker, Call
from .forms import MyForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

from .scripts import calculate_phone_graph
from .scripts import calculate_org_graph as cog
from .scripts import calculate_post_graph as cpg
import os
import datetime
import pandas as pd

#получение даты последнего измениния файла
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

@login_required
def start_page(request):
    return render(request, 'blog/index.html')

def handle_uploaded_org_struct(f):
    with open('blog/media/downloads/org_struct.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)

'''tabnum = models.TextField()
fio = models.TextField()
gender = models.TextField()
birthdate  = models.TextField()
p = Person(name="Fred Flintstone", shirt_size="L")
p.save()'''

def handle_uploaded_workers_info(f):
    with open('blog/media/downloads/workers_info.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    df = pd.read_csv('blog/media/downloads/workers_info.csv', sep=';', names=['id', 'tabnum', 'fio', 'gender', 'birthdate', 'photo'])
    for i, j in df.iterrows():
        p = Worker(tabnum=int(j['tabnum']), fio=j['fio'], gender=j['gender'], birthdate = j['birthdate'], photo_id=j['photo'])
        p.save()

def handle_uploaded_phone_log(f):
    with open('blog/media/downloads/phone_log.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)
    df = pd.read_csv('blog/media/downloads/phone_log.csv', sep=';', names=['id', 'from', 'to', 'duration', 'time', 'date'])
    for i, j in df.iterrows():
        first_tabnum =Worker.objects.get(tabnum=int(j['from']))
        second_tabnum =Worker.objects.get(tabnum=int(j['to']))
        p = Call(call_from=first_tabnum, call_to=second_tabnum, call_duration=int(j['duration']),
        call_time = datetime.datetime.strptime(j['time'],'%H:%M:%S'),
        call_date=datetime.datetime.strptime(j['date'], '%d.%m.%Y'))
        p.save()

def handle_uploaded_post_log(f):
    with open('blog/media/downloads/post_log.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)

def handle_uploaded_skud_log(f):
    with open('blog/media/downloads/skud_log.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)

def handle_uploaded_job_history_log(f):
    with open('blog/media/downloads/workers_job_history.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)



@login_required
def upload_org_struct(request):

    lastup = modification_date('blog/media/downloads/org_struct.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_org_struct(request.FILES['docfile'])
            return render(request, 'blog/upload_org_struct.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_org_struct.html', {'form': form, 'lastup' : lastup})

@login_required
def upload_worker_info(request):

    lastup = modification_date('blog/media/downloads/workers_info.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_workers_info(request.FILES['docfile'])
            return render(request, 'blog/upload_workers_info.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_workers_info.html', {'form': form, 'lastup' : lastup})


@login_required
def upload_phone_log(request):

    lastup = modification_date('blog/media/downloads/phone_log.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_phone_log(request.FILES['docfile'])
            return render(request, 'blog/upload_phone_log.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_phone_log.html', {'form': form, 'lastup' : lastup})

@login_required
def upload_post_log(request):

    lastup = modification_date('blog/media/downloads/post_log.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_post_log(request.FILES['docfile'])
            return render(request, 'blog/upload_post_log.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_post_log.html', {'form': form, 'lastup' : lastup})

@login_required
def upload_skud_log(request):

    lastup = modification_date('blog/media/downloads/skud_log.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_skud_log(request.FILES['docfile'])
            return render(request, 'blog/upload_skud_log.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_skud_log.html', {'form': form, 'lastup' : lastup})

@login_required
def upload_workers_job_history(request):

    lastup = modification_date('blog/media/downloads/workers_job_history.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_job_history_log(request.FILES['docfile'])
            return render(request, 'blog/upload_workers_job_history.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_workers_job_history.html', {'form': form, 'lastup' : lastup})

@login_required
def connect_graph(request):
    return render(request, 'blog/connect_graph.html')

@login_required
def check_connect(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            #handle_uploaded_post_log(request.FILES['docfile'])
            photo_1 = Worker.objects.get(fio=form.cleaned_data['choose_1st_fighter'])
            photo_2 = Worker.objects.get(fio=form.cleaned_data['choose_2st_fighter'])
            return render(request, 'blog/check_connect.html', {'form' : form, 'fio1' : form.cleaned_data['choose_1st_fighter'],
             'fio2' : form.cleaned_data['choose_2st_fighter'], 'photo_1' : photo_1.photo_id, 'photo_2' : photo_2.photo_id})
        else:
            print ('no valid')
            return render(request, 'blog/check_connect.html', {'form' : form})
    else:
        form = MyForm()
    return render(request, 'blog/check_connect.html', {'form' : form})


@login_required
def org_struct_graph(request):
    return render(request, 'blog/org_graph.html')

@login_required
def create_phone_json(request):
        calculate_phone_graph.main()
        return HttpResponseRedirect('/graph/phone_graph/')

@login_required
def create_org_json(request):
        cog.main()
        return HttpResponseRedirect('/graph/org_graph/')

@login_required
def create_post_json(request):
        cpg.main()
        return HttpResponseRedirect('/graph/post_graph/')
