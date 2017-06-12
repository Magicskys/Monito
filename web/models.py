# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Dashboad(models.Model):
    time=models.TimeField(u'时间',auto_now_add= True)
    cpu=models.FloatField(u"CPU",default=0.0)
    memory=models.FloatField(u"内存",default=0)
    io_in=models.BigIntegerField(u'io写入',default=0)
    io_out=models.BigIntegerField(u'io读入',default=0)
    net=models.IntegerField(u'网络速度',default=0)

    def natural_key(self):
        return (self.cpu,self.memory)
    # def __unicode__(self):
    #     return self.time
    class Meta:
        verbose_name_plural = '系统信息'
