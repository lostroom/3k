from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^test_d3', views.graph, name='test_d3'),
    url(r'^play_count_by_month', views.play_count_by_month, name='play_count_by_month'),
]
