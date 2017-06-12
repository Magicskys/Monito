from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^login/',views.log_in,name='login'),
    url(r'^logout/',views.log_out,name='logout'),
    url(r'^test/',views.test,name='test'),
    url(r'^test2/',views.test2,name='test2'),
    url(r'^userinfo/',views.userinfo,name='userinfo'),
    url(r'^psinfo/',views.psinfo,name='psinfo'),
    url(r'^netinfo/',views.netinfo,name='netinfo'),
]