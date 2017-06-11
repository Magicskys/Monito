# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login,logout,authenticate
from forms import LoginForm
import psutil
from django.core import serializers
from models import Dashboad
import datetime
# Create your views here.



def index(request):
    if request.user.is_authenticated():
        form={'cpu':psutil.cpu_count(),'logical_cpu':psutil.cpu_count(logical=False),'len_user':len(psutil.users()),'open_date':datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S"),'len_net':len(psutil.net_io_counters(pernic=True))}
        return render(request,'content.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')

def log_in(request):
    if request.method=='GET':
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    elif request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None and user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("密码错误")
    else:
        form=LoginForm()
        return render(request,'login.html',{'form':form})


def log_out(request):
    logout(request)
    return HttpResponse("退出")


def test(request):
    data=Dashboad.objects.order_by("-id").values_list("id")[0][0]
    Dashboad.objects.filter(id__lt=data-100).delete()
    return HttpResponse("ok")
    # return JsonResponse(data=data,safe=False,content_type="application/json")


def test2(request):
    if request.is_ajax():
        cpu=psutil.cpu_percent()
        io_in,io_out=int(psutil.disk_io_counters()[3]),int(psutil.disk_io_counters()[4])
        memory=psutil.virtual_memory().free
        Dashboad.objects.create(cpu=cpu,memory=memory,io_in=io_in,io_out=io_out)
        if Dashboad.objects.count() >=100:
            endid = Dashboad.objects.order_by("-id").values_list("id")[0][0]
            Dashboad.objects.filter(id__lt=endid - 100).delete()
        # data=Dashboad.objects.all().values_list("memory")
        data=serializers.serialize("json",Dashboad.objects.all(),fields=['cpu','memory'],use_natural_foreign_keys=True, use_natural_primary_keys=True)

        # return HttpResponse(data)
        return JsonResponse(data=data,safe=False,content_type="application/json")
    else:
        return HttpResponse("error")