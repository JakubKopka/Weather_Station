# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Odczyty, Odczyty_Algorytm


class OdczytyAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_odczytu', 'temperatura', 'wilgotnosc', 'cisnienie', 'sila_wiatru')


admin.site.register(Odczyty, OdczytyAdmin)
admin.site.register(Odczyty_Algorytm, OdczytyAdmin)
