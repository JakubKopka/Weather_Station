# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        context = super(WilgotnoscView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

class CisnienieView(TemplateView):
    template_name = 'cisnienie.html'
    title = 'Ciśnienie'

    def get_context_data(self, **kwargs):
        context = super(CisnienieView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

class WiatrViews(TemplateView):
    template_name = 'wiatr.html'
    title = 'Wiatr'

    def get_context_data(self, **kwargs):
        context = super(WiatrViews, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
