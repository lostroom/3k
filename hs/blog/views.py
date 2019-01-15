from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from .models import Play
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

from .scripts import calculate_phone_graph
from .scripts import calculate_org_graph as cog
from .scripts import calculate_post_graph as cpg
import os
import datetime

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

def handle_uploaded_workers_info(f):
    with open('blog/media/downloads/workers_info.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)

def handle_uploaded_phone_log(f):
    with open('blog/media/downloads/phone_log.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)

def handle_uploaded_post_log(f):
    with open('blog/media/downloads/post_log.csv', 'wb+') as destination:
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
def phone_graph(request):
    return render(request, 'blog/phone_graph.html')

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
