from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/org_struct/success/$', views.success_upload_org_struct, name='success_upload_org_struct'),
    url(r'^upload/org_struct/$', views.upload_org_struct, name='upload_org_struct'),
    url(r'^upload/phone_log/success/$', views.success_upload_phone_log, name='success_upload_phone_log'),
    url(r'^upload/phone_log/$', views.upload_phone_log, name='upload_phone_log'),
    url(r'^graph/phone_graph/$', views.phone_graph, name='phone_graph'),
    url(r'^graph/phone_graph/calcucate/$', views.create_phone_json, name='create_phone_json'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^test_d3', views.graph, name='test_d3'),
    url(r'^play_count_by_month', views.play_count_by_month, name='play_count_by_month'),
]
