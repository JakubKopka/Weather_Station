# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from stacjapogodowa.models import Odczyty

class StronaGlownaView(TemplateView):
    name = 'StronaGlowna'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(StronaGlownaView, self).get_context_data(**kwargs)
        context['latest_articles'] = Odczyty.objects.all()[:2]
        return context


class TemperaturaView(View):
    name = 'Temperatura'
    template_name = 'temperatura.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Temperatura')


class WilgotnoscView(View):
    name = 'Wilgotnosc'
    template_name = 'wilgotnosc.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Wilgotnosc')


class CisnienieView(View):
    name = 'Cisnienie'
    template_name = 'cisnienie.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Cisnienie')


class WiatrViews(View):
    name = 'Wiatr'
    template_name = 'wiatr.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Sila Waitru i Kierunek Wiatru')
