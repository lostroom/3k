from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.start_page, name='start_page'),

    url(r'^upload/worker_info/$', views.upload_worker_info, name='upload_worker_info'),
    url(r'^upload/org_struct/$', views.upload_org_struct, name='upload_org_struct'),
    url(r'^upload/phone_log/$', views.upload_phone_log, name='upload_phone_log'),
    url(r'^upload/post_log/$', views.upload_post_log, name='upload_post_log'),

    url(r'^graph/post_graph/$', views.phone_graph, name='phone_graph'),
    url(r'^graph/phone_graph/$', views.phone_graph, name='phone_graph'),
    url(r'^graph/org_graph/$', views.org_struct_graph, name='org_struct_graph'),

    url(r'^graph/phone_graph/calcucate/$', views.create_phone_json, name='create_phone_json'),
    url(r'^graph/org_graph/calcucate/$', views.create_org_json, name='create_org_json'),
    url(r'^graph/post_graph/calcucate/$', views.create_post_json, name='create_post_json')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
