# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Dashboad
# Register your models here.

class DashboadInfo(admin.ModelAdmin):
    list_display=('time','cpu','memory','io_in','io_out')

admin.site.register(Dashboad,DashboadInfo)