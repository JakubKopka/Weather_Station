# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.conf import settings
from django.utils import timezone



from django.views.generic.base import TemplateView
from stacjapogodowa.models import Odczyty, Odczyty_10, Odczyty_50


class StronaGlownaView(TemplateView):
    title = 'Strona Główna'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(StronaGlownaView, self).get_context_data(**kwargs)
        odczyty = Odczyty.objects.all()
        odczyty = reversed(odczyty)
        context['odczyty'] = odczyty
        context['title'] = self.title
        return context


class TemperaturaView(TemplateView):
    template_name = 'temperatura.html'
    title = 'Temperatura'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all().order_by('-id')[:settings.ILOSC_ODCZYTOW]
        odczyty_50 = Odczyty_10.objects
        odczyty = reversed(odczyty)

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:
            data2 = i.data_odczytu.strftime('%H:%M')
            data.append([data2, i.temperatura])

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
        odczyty = Odczyty.objects.all().order_by('-id')[:settings.ILOSC_ODCZYTOW]
        odczyty = reversed(odczyty)

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

        czas_teraz = timezone.now()
        #czas_h_do_tylu = czas_teraz - datetime.timedelta(hours=1)
        only_hour = datetime.datetime(czas_teraz.year, czas_teraz.month, czas_teraz.day, czas_teraz.hour, 0,0)
        obiekty = Odczyty .objects.filter(data_odczytu__range=(only_hour, czas_teraz))
        print "Godzina do: ", czas_teraz
        print "Godzina od ", only_hour
        for i in obiekty:
            print i.data_odczytu

        # now = timezone.now()
        # earlier = now - timedelta(hours=1)
        # x = Odczyty.objects.filter(data_odczytu__range=(earlier, now))
        # for i in x:
        #     print i.data_odczytu

        odczyty = Odczyty.objects.all().order_by('-id')[:settings.ILOSC_ODCZYTOW]
        odczyty = reversed(odczyty)

        data = [
            ['Data', 'Odczyty', 'Algorytm'],
        ]
        for i in odczyty:
            hour = i.data_odczytu.strftime('%H:%M')
            data.append([hour, i.cisnienie, 995])

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




