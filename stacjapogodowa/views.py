# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from celery.schedules import crontab
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from stacjapogodowa.models import Odczyty


class StronaGlownaView(TemplateView):
    title = 'Strona Główna'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(StronaGlownaView, self).get_context_data(**kwargs)
        context['odczyty'] = Odczyty.objects.all()
        context['title'] = self.title
        return context


class TemperaturaView(TemplateView):
    template_name = 'temperatura.html'
    title = 'Temperatura'

    def get_context_data(self, **kwargs):
        context = super(TemperaturaView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class WilgotnoscView(TemplateView):
    template_name = 'wilgotnosc.html'
    title = 'Wilgotność'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all()[:20]
        cisnienie = [];
        data = [];
        context = super(WilgotnoscView, self).get_context_data(**kwargs)
        context['title'] = self.title

        for i in odczyty:
            data2 = i.data_odczytu.strftime("%H:%M")
            data.append([i.wilgotnosc, data2])

        # context['dane'] = cisnienie
        # context['data'] = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        context['data'] = data

        print context['data']

        from graphos.sources.simple import SimpleDataSource
        from graphos.renderers.gchart import LineChart

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:

            data2 = i.data_odczytu.strftime('%H:%M')
            data.append([data2, i.wilgotnosc, 10])


        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.width = 1600
        chart.height = 600
        context = {'chart': chart}

        return context

class CisnienieView(TemplateView):
    template_name = 'cisnienie.html'
    title = 'Ciśnienie'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all();
        cisnienie = [];
        data = [];

        # for i in odczyty:
        #     dict = {}
        #     dict.update(i.cisnienie,str(i.data_odczytu) )
        #     data.append(dict)
        # context = super(CisnienieView, self).get_context_data(**kwargs)
        # context['title'] = self.title
        # # context['dane'] = cisnienie
        # # context['data'] = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        # context['data'] = data
        #
        # print context['data']
        # return context

class WiatrViews(TemplateView):
    template_name = 'wiatr.html'
    title = 'Wiatr'

    def get_context_data(self, **kwargs):
        context = super(WiatrViews, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context




