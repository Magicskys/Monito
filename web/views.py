# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login,logout,authenticate
from forms import LoginForm
import psutil,json
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

def userinfo(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            userinfo=[i for i in psutil.users()]
            return JsonResponse(data=userinfo,safe=False,content_type="application/json")
        else:
            userinfo=psutil.users()
            return render(request,'userinfo.html',{'userinfo':userinfo,'userinfo_len':len(userinfo)})
    else:
        return HttpResponseRedirect('/login')

def psinfo(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            psinfo = [i.as_dict(attrs=['status', 'username', 'pid', 'name', 'exe']) for i in psutil.process_iter()]
            return JsonResponse(data=json.dumps(psinfo),safe=False,content_type='application/json')
        else:
            psinfo=[i for i in psutil.process_iter()]
            return render(request,'psinfo.html',{'psinfo':psinfo,'psinfo_len':len(psinfo)})
    else:
        return HttpResponseRedirect('/login')

def netinfo(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            netinfo = {i:j for i,j in psutil.net_io_counters(pernic=True).items()}
            try:
                netinfo_two=psutil.net_connections()
                netinfo_two_len=len(netinfo_two)
            except:
                netinfo_two=False
                netinfo_two_len=0
            return JsonResponse(data=json.dumps([netinfo,len(netinfo),netinfo_two,netinfo_two_len]),safe=False,content_type='application/json')
        else:
            netinfo=psutil.net_io_counters(pernic=True)
            try:
                netinfo_two=psutil.net_connections()
                netinfo_two_len=len(netinfo_two)
            except:
                netinfo_two=False
                netinfo_two_len=0
            return render(request,'netinfo.html',{'netinfo_len':len(netinfo),'netinfo_two_len':netinfo_two_len,'netinfo':netinfo,'netinfo_two':netinfo_two})
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
    if request.user.is_authenticated():
        logout(request)
        return HttpResponse("成功退出")
    else:
        return HttpResponseRedirect("/login/")

def test(request):
    userinfo =[i.as_dict(attrs=['status','username','pid','name','exe']) for i in psutil.process_iter()]
    return HttpResponse(json.dumps(userinfo))
    # return JsonResponse(data=data,safe=False,content_type="application/json")

def test2(request):
    if request.is_ajax():
        cpu=psutil.cpu_percent()
        io_in,io_out=int(psutil.disk_io_counters()[3]),int(psutil.disk_io_counters()[4])
        memory=psutil.virtual_memory()
        memory=round(float(memory[0]-memory[1])/float(memory[0])*100,2)
        Dashboad.objects.create(cpu=cpu,memory=memory,io_in=io_in,io_out=io_out)
        if Dashboad.objects.count() >=100:
            endid = Dashboad.objects.order_by("-id").values_list("id")[0][0]
            Dashboad.objects.filter(id__lt=endid - 100).delete()
        # data=Dashboad.objects.all().values_list("memory")
        data=serializers.serialize("json",Dashboad.objects.all(),fields=['cpu','memory'],use_natural_foreign_keys=True, use_natural_primary_keys=True)
        # return HttpResponse(data)
        return JsonResponse(data=data,safe=False,content_type="application/json")
    else:
        return HttpResponse("")