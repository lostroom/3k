from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Worker, Call, Letter, Meet, Stat
from .forms import MyForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

from .scripts import analyze_calls
from .scripts import analyze_letters
from .scripts import calculate_org_graph as cog
from .scripts import handle_letter
import os
import datetime
import pandas as pd
import time
import json

from django.db.models import Q

#получение даты последнего изменения файла
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
    Call.objects.all().delete()
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
    df = pd.read_csv('blog/media/downloads/post_log.csv', sep=';', names=['id', 'from', 'to', 'theme', 'message', 'date', 'time'])
    Letter.objects.all().delete()
    for i, j in df.iterrows():
        first_tabnum =Worker.objects.get(tabnum=int(j['from']))
        second_tabnum =Worker.objects.get(tabnum=int(j['to']))
        letter_dict = handle_letter.main(j['theme'], j['message'])

        p = Letter(letter_from=first_tabnum, letter_to=second_tabnum, letter_theme=j['theme'],letter_message=j['message'],
        letter_time = datetime.datetime.strptime(j['time'],'%H:%M:%S'),
        letter_date=datetime.datetime.strptime(j['date'], '%d.%m.%Y'),
        letter_dict = letter_dict)
        p.save()

def handle_uploaded_meet_log(f):
    with open('blog/media/downloads/meet_log.csv', 'wb+') as destination:
        for chunk in f.chunks():\
            destination.write(chunk)
    df = pd.read_csv('blog/media/downloads/meet_log.csv', sep=';', names=['id', 'meet_id', 'participant', 'theme', 'subject', 'date', 'time'])
    Meet.objects.all().delete()
    for i, j in df.iterrows():
        participant =Worker.objects.get(tabnum=int(j['participant']))

        p = Meet(meet_key=j['meet_id'], meet_participant=participant, meet_theme=j['theme'],meet_subject=j['subject'],
        meet_time = datetime.datetime.strptime(j['time'],'%H:%M:%S'),
        meet_date=datetime.datetime.strptime(j['date'], '%d.%m.%Y'))
        p.save()

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
def upload_meet_log(request):

    lastup = modification_date('blog/media/downloads/meet_log.csv')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_meet_log(request.FILES['docfile'])
            return render(request, 'blog/upload_meet_log.html', {'form': form, 'lastup' : lastup})
    else:
        form = UploadFileForm()
    return render(request, 'blog/upload_meet_log.html', {'form': form, 'lastup' : lastup})

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


            t1 = Worker.objects.get(fio=form.cleaned_data['choose_1st_fighter'])
            t2 = Worker.objects.get(fio=form.cleaned_data['choose_2st_fighter'])

            c = Call.objects.filter((Q(call_from=t1) & Q(call_to=t2)) | (Q(call_from=t2) & Q(call_to=t1))).order_by('call_date')

            date_rng = pd.date_range(start='1/1/2018', end='31/12/2018', freq='D').tolist()
            df1 = pd.DataFrame(data=date_rng)
            df1.columns = ['day_of_year']
            call_list = [[i.call_date, i.call_duration]  for i in c]
            df2 = pd.DataFrame(data=call_list, columns=['day_of_call', 'duration'])
            df2['day_of_call'] = pd.to_datetime(df2['day_of_call'], format='%Y-%m-%d')

            df3 = df1.merge(df2, how='left', left_on='day_of_year', right_on='day_of_call')
            gdf = df3.groupby('day_of_year', as_index=False)['duration'].sum()
            gdf['javatime'] = gdf['day_of_year'].apply(lambda x: int(time.mktime(x.timetuple()))*1000)
            test_pack = gdf[['javatime','duration']].values.tolist()

            total_duration = df2['duration'].sum()
            avg_duration = int(df2['duration'].mean())
            day_calls = str(round(df2['duration'].count()/220,2)).replace(',','.')

            return render(request, 'blog/check_connect.html', {'form' : form, 'fio1' : form.cleaned_data['choose_1st_fighter'],
             'fio2' : form.cleaned_data['choose_2st_fighter'], 'photo_1' : photo_1.photo_id, 'photo_2' : photo_2.photo_id,
              'test_list' : test_pack, 'total_duration' :total_duration, 'avg_duration':avg_duration, 'day_calls' : day_calls})
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
def calls_calculate(request):
        lastup = modification_date('blog/media/downloads/phone_log.csv')
        analyze_calls.main()
        form = UploadFileForm()
        return render(request, 'blog/upload_phone_log.html', {'form': form, 'lastup' : lastup})

@login_required
def letters_calculate(request):
        lastup = modification_date('blog/media/downloads/post_log.csv')
        analyze_letters.main()
        form = UploadFileForm()
        return render(request, 'blog/upload_post_log.html', {'form': form, 'lastup' : lastup})

@login_required
def action_buttons(request):
        return render(request, 'blog/action_buttons.html')

@login_required
def action_buttons_1(request):

    def synt_id(x):
        if x[0]>x[1]:
            return str(x[1])+'_'+str(x[0])
        else:
            return str(x[0])+'_'+str(x[1])

    df_workers = pd.DataFrame(list(Worker.objects.all().values('tabnum', 'fio', 'photo_id')))
    df_workers['key'] = 1
    df_matrix = df_workers[['tabnum', 'key']].merge(df_workers[['tabnum', 'key']], how='inner', on='key')
    df_matrix['synt_id'] = df_matrix[['tabnum_x', 'tabnum_y']].apply(synt_id, axis=1)
    df_matrix = df_matrix[df_matrix.tabnum_x != df_matrix.tabnum_y]
    df_matrix = df_matrix[['synt_id']]

    df_calls = pd.DataFrame(list(Call.objects.all().values()))
    df_calls['synt_id'] = df_calls[['call_from_id', 'call_to_id']].apply(synt_id, axis=1)
    df_calls_agg =  df_calls.groupby('synt_id').agg({'call_to_id': 'count'})

    df_letters = pd.DataFrame(list(Letter.objects.all().values()))
    df_letters['synt_id'] = df_letters[['letter_from_id', 'letter_to_id']].apply(synt_id, axis=1)
    df_letters_agg =  df_letters.groupby('synt_id').agg({'letter_from_id': 'count'})

    df_meet = pd.DataFrame(list(Meet.objects.all().values()))
    df_meet_matrix = df_meet[['meet_key', 'meet_participant_id']].merge(df_meet[['meet_key', 'meet_participant_id']], how='inner', on='meet_key')
    df_meet_matrix = df_meet_matrix[df_meet_matrix.meet_participant_id_x != df_meet_matrix.meet_participant_id_y]
    df_meet_matrix['synt_id'] = df_meet_matrix[['meet_participant_id_x', 'meet_participant_id_y']].apply(synt_id, axis=1)
    df_meet_agg =  df_meet_matrix.groupby('synt_id').agg({'meet_participant_id_x': 'count'})

    df_total = df_matrix.merge(df_calls_agg, how='left', on='synt_id').merge(df_letters_agg, how='left', on='synt_id')\
    .merge(df_meet_agg, how='left', on='synt_id')
    df_total = df_total.fillna(0)
    df_total['result'] = df_total['letter_from_id']+3*df_total['meet_participant_id_x']
    #+0.1*df_total['call_to_id']

    Stat.objects.all().delete()
    for i,j in df_total.iterrows():
        t1 =Worker.objects.get(tabnum=int(j['synt_id'].split('_')[0]))
        t2 =Worker.objects.get(tabnum=int(j['synt_id'].split('_')[1]))

        p = Stat(synt_id=j['synt_id'], first_tabnum=t1, second_tabnum=t2,
        stat_letters=j['letter_from_id'], stat_calls=j['call_to_id'],
        stat_meets=j['meet_participant_id_x'], stat_result=j['result'])
        p.save()

    data ={}
    data['nodes'] = []
    data['edges'] = []

    for i, j in df_workers.iterrows():
        data['nodes'].append({"label": j['fio'], "id": int(j['tabnum']) , "data": "olodata",
        "shape": 'circularImage', "image": '../../media/photos/man_icon.png'})

    for i, j in df_total[df_total.result>0].iterrows():
        pairs = j['synt_id'].split('_')
        data['edges'].append({"from": int(pairs[0]), "to": int(pairs[1]), "width" : float(j['result'])/15,  "data": str(j['result'])})

    '''for i,j in group_df.iterrows():
        pairs = j['meta_id'].split('_')
        data['edges'].append({"from": int(pairs[0]), "to": int(pairs[1]), "data": "total sec:"+str(j['duration'])})'''

    with open('blog/static/jsons/phone_graph.json', 'w+') as outfile:
        json.dump(data, outfile)


    return render(request, 'blog/action_buttons.html')

@login_required
def create_org_json(request):
        cog.main()
        return HttpResponseRedirect('/graph/org_graph/')

@login_required
def create_post_json(request):
        cpg.main()
        return HttpResponseRedirect('/graph/post_graph/')
