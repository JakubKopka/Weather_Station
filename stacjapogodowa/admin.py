# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Odczyty, Odczyty_50, Odczyty_10


class OdczytyAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_odczytu', 'temperatura', 'wilgotnosc', 'cisnienie',)


admin.site.register(Odczyty, OdczytyAdmin)
admin.site.register(Odczyty_50, OdczytyAdmin)
admin.site.register(Odczyty_10, OdczytyAdmin)
