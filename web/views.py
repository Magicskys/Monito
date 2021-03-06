# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login,logout,authenticate
from forms import LoginForm
import psutil,json,os,random,string,cStringIO
from PIL import ImageFont,ImageDraw,Image
from Monito.settings import BASE_DIR
from django.core import serializers
from models import Dashboad
import datetime
import os
# Create your views here.

def audit_login(view):
    def _audit_login(request,*args,**kwargs):
        if request.user.is_authenticated():
            return view(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login')
    return _audit_login


@audit_login
def index(request):
    form={'cpu':psutil.cpu_count(),'logical_cpu':psutil.cpu_count(logical=False),'len_user':len(psutil.users()),'open_date':datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S"),'len_net':len(psutil.net_io_counters(pernic=True))}
    return render(request,'content.html',{'form':form})

@audit_login
def userinfo(request):
    if request.is_ajax():
        userinfo=[i for i in psutil.users()]
        return JsonResponse(data=userinfo,safe=False,content_type="application/json")
    else:
        userinfo=psutil.users()
        return render(request,'userinfo.html',{'userinfo':userinfo,'userinfo_len':len(userinfo)})

@audit_login
def psinfo(request):
    if request.is_ajax():
        if request.GET['pid']:
            pid_info=psutil.Process(int(request.GET['pid'])).as_dict()
            return JsonResponse(data=json.dumps(pid_info),safe=False,content_type='application/json')
        psinfo = [i.as_dict(attrs=['status', 'username', 'pid', 'name', 'exe']) for i in psutil.process_iter()]
        return JsonResponse(data=json.dumps(psinfo),safe=False,content_type='application/json')
    else:
        psinfo=[i for i in psutil.process_iter()]
        return render(request,'psinfo.html',{'psinfo':psinfo,'psinfo_len':len(psinfo)})

@audit_login
def pskill(request):
    if request.is_ajax():
        try:
            psutil.Process(int(request.GET['pid'])).kill()
        except:
            return JsonResponse(data='关闭进程失败',safe=False,content_type='application/json')
        return JsonResponse(data="成功关闭进程",safe=False,content_type='application/json')
    else:
        return JsonResponse(data="关闭进程失败",safe=False,content_type='application/json')


@audit_login
def netinfo(request):
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

@audit_login
def log_out(request):
    logout(request)
    return HttpResponse("成功退出")


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
        data=serializers.serialize("json",Dashboad.objects.all(),fields=['cpu','memory'],use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return JsonResponse(data=data,safe=False,content_type="application/json")
    else:
        return HttpResponse("")

def captcha(request):
    image=Image.new('RGB',(147,49),color=(255,255,255))
    # font_file=os.path.join(BASE_DIR,'static/fonts/Trojan.ttf')
    # font=ImageFont.truetype(font_file,47)
    draw=ImageDraw.Draw(image)
    rand_str=''.join(random.sample(string.letters+string.digits,4))
    draw.text((100,30),rand_str,fill=(0,0,0))
    del draw
    # request.session['catpcha']=rand_str.lower()
    buf=cStringIO.StringIO()
    image.save(buf,'jpeg')
    return HttpResponse(buf.getvalue(),'image/jpeg')

