# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.conf import settings



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
        odczyty = Odczyty.objects.all()[:settings.ILOSC_ODCZYTOW]

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:
            data2 = i.data_odczytu.strftime('%H:%M')
            data.append([data2, i.temperatura, 0])

        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['title'] = "Wykres Temperatury - ostatnia godzina"
        chart.options['pointSize'] = settings.POINT_SIZE

        context = {'chart': chart}
        context['title'] = self.title

        return context


class WilgotnoscView(TemplateView):
    template_name = 'wilgotnosc.html'
    title = 'Wilgotność'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all()[:settings.ILOSC_ODCZYTOW]

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:

            data2 = i.data_odczytu.strftime('%H:%M')
            data.append([data2, i.wilgotnosc, 88])


        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.options['title'] = "Wykres Wilgotności - ostatnia godzina"
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['pointSize'] = settings.POINT_SIZE

        context = {'chart': chart}
        context['title'] = self.title

        return context

class CisnienieView(TemplateView):
    template_name = 'cisnienie.html'
    title = 'Ciśnienie'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all()[:settings.ILOSC_ODCZYTOW]

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:
            data2 = i.data_odczytu.strftime('%H:%M')
            data.append([data2, i.cisnienie, 995])

        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.options['title'] = "Wykres Ciśinienia - ostatnia godzina"
        chart.options['subtitle'] = 'test'
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['pointSize'] = settings.POINT_SIZE

        context = {'chart': chart}
        context['title'] = self.title

        return context




