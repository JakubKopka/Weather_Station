# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import math
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.conf import settings
from django.utils import timezone



from django.views.generic.base import TemplateView
from stacjapogodowa.models import Odczyty, Odczyty_10, Odczyty_50


def MAE(abs):
    n = len(abs)
    if n > 0:
        sum_abs = 0.0
        for i in range(n):
            sum_abs += abs[i]
        return round(1.0 / n * sum_abs, 3)
    else:
        return 0


def RMSE(abs):
    n = len(abs)
    if n > 0:
        sum_abs = 0.0
        for i in range(n):
            sum_abs += abs[i] * abs[i]
        return round(math.sqrt(1.0 / n * sum_abs), 3)
    else:
        return 0

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
        odczyty = list(reversed(odczyty))

        odczyty_50 = Odczyty_50.objects.all().order_by('-id')[:50]
        odczyty_50 = list(reversed(odczyty_50))

        odczyty_10 = Odczyty_10.objects.all().order_by('-id')[:10]
        odczyty_10 = list(reversed(odczyty_10))

        lista_dat = []

        for i in odczyty:
            lista_dat.append(i.data_odczytu)

        for i in odczyty_10:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        for i in odczyty_50:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        data = []
        abs_50 = []
        abs_10 = []
        for i in lista_dat:
            odczyt_1 = None
            odczyt_2 = None
            odczyt_3 = None
            data2 = i.strftime('%H:%M')

            for o1 in odczyty:
                if i == o1.data_odczytu:
                    odczyt_1 = o1.temperatura
            for o2 in odczyty_10:
                if i == o2.data_odczytu:
                    odczyt_2 = o2.temperatura
            for o3 in odczyty_50:
                if i == o3.data_odczytu:
                    odczyt_3 = o3.temperatura

            data.append([data2, odczyt_1, odczyt_2, odczyt_3])
            if odczyt_1 != None and odczyt_2 != None:
                abs = math.fabs(odczyt_1-odczyt_2)
                abs_10.append(abs)
            if odczyt_1 != None and odczyt_3 != None:
                abs = math.fabs(odczyt_1-odczyt_3)
                abs_50.append(abs)


        print(len(data))
        data = data[settings.ILOSC_ODCZYTOW*-1:]
        data2 = [
            ['Data', 'Odczyty', 'Algorytm dla 10', 'Algorytm dla 50'],
        ]
        data = data2 + data
        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object



        chart = LineChart(data_source)
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['title'] = "Temperatura [°C]"
        chart.options['pointSize'] = settings.POINT_SIZE
        context = {'chart': chart}
        context['title'] = self.title


        context['MAE_10'] = MAE(abs_10)
        context['RMSE_10'] = RMSE(abs_10)
        context['MAE_50'] = MAE(abs_50)
        context['RMSE_50'] = RMSE(abs_50)

        return context


class WilgotnoscView(TemplateView):
    template_name = 'wilgotnosc.html'
    title = 'Wilgotność'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all().order_by('-id')[:settings.ILOSC_ODCZYTOW]
        odczyty = list(reversed(odczyty))

        odczyty_50 = Odczyty_50.objects.all().order_by('-id')[:50]
        odczyty_50 = list(reversed(odczyty_50))

        odczyty_10 = Odczyty_10.objects.all().order_by('-id')[:10]
        odczyty_10 = list(reversed(odczyty_10))

        lista_dat = []

        for i in odczyty:
            lista_dat.append(i.data_odczytu)

        for i in odczyty_10:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        for i in odczyty_50:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        data = []
        abs_50 = []
        abs_10 = []
        for i in lista_dat:
            odczyt_1 = None
            odczyt_2 = None
            odczyt_3 = None
            data2 = i.strftime('%H:%M')

            for o1 in odczyty:
                if i == o1.data_odczytu:
                    odczyt_1 = o1.wilgotnosc
            for o2 in odczyty_10:
                if i == o2.data_odczytu:
                    odczyt_2 = o2.wilgotnosc
            for o3 in odczyty_50:
                if i == o3.data_odczytu:
                    odczyt_3 = o3.wilgotnosc

            data.append([data2, odczyt_1, odczyt_2, odczyt_3])
            if odczyt_1 != None and odczyt_2 != None:
                abs = math.fabs(odczyt_1 - odczyt_2)
                abs_10.append(abs)
            if odczyt_1 != None and odczyt_3 != None:
                abs = math.fabs(odczyt_1 - odczyt_3)
                abs_50.append(abs)

        print(len(data))
        data = data[settings.ILOSC_ODCZYTOW * -1:]
        data2 = [
            ['Data', 'Odczyty', 'Algorytm dla 10', 'Algorytm dla 50'],
        ]
        data = data2 + data
        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['title'] = "Wilgotność [%] "
        chart.options['pointSize'] = settings.POINT_SIZE

        context = {'chart': chart}
        context['title'] = self.title

        context['MAE_10'] = MAE(abs_10)
        context['RMSE_10'] = RMSE(abs_10)
        context['MAE_50'] = MAE(abs_50)
        context['RMSE_50'] = RMSE(abs_50)

        return context

class CisnienieView(TemplateView):
    template_name = 'cisnienie.html'
    title = 'Ciśnienie'

    def get_context_data(self, **kwargs):
        odczyty = Odczyty.objects.all().order_by('-id')[:settings.ILOSC_ODCZYTOW]
        odczyty = list(reversed(odczyty))

        odczyty_50 = Odczyty_50.objects.all().order_by('-id')[:50]
        odczyty_50 = list(reversed(odczyty_50))

        odczyty_10 = Odczyty_10.objects.all().order_by('-id')[:10]
        odczyty_10 = list(reversed(odczyty_10))

        lista_dat = []

        for i in odczyty:
            lista_dat.append(i.data_odczytu)

        for i in odczyty_10:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        for i in odczyty_50:
            if not i.data_odczytu in lista_dat:
                lista_dat.append(i.data_odczytu)

        data = []
        abs_50 = []
        abs_10 = []
        for i in lista_dat:
            odczyt_1 = None
            odczyt_2 = None
            odczyt_3 = None
            data2 = i.strftime('%H:%M')

            for o1 in odczyty:
                if i == o1.data_odczytu:
                    odczyt_1 = o1.cisnienie
            for o2 in odczyty_10:
                if i == o2.data_odczytu:
                    odczyt_2 = o2.cisnienie
            for o3 in odczyty_50:
                if i == o3.data_odczytu:
                    odczyt_3 = o3.cisnienie

            data.append([data2, odczyt_1, odczyt_2, odczyt_3])
            if odczyt_1 != None and odczyt_2 != None:
                abs = math.fabs(odczyt_1 - odczyt_2)
                abs_10.append(abs)
            if odczyt_1 != None and odczyt_3 != None:
                abs = math.fabs(odczyt_1 - odczyt_3)
                abs_50.append(abs)

        print(len(data))
        data = data[settings.ILOSC_ODCZYTOW * -1:]
        data2 = [
            ['Data', 'Odczyty', 'Algorytm dla 10', 'Algorytm dla 50'],
        ]
        data = data2 + data
        # DataSource object
        data_source = SimpleDataSource(data=data)
        # Chart object
        chart = LineChart(data_source)
        chart.width = settings.SZEROKOSC
        chart.height = settings.WYSOKOSC
        chart.options['title'] = "Ciśnienie [hPa]"
        chart.options['pointSize'] = settings.POINT_SIZE

        context = {'chart': chart}
        context['title'] = self.title

        context['MAE_10'] = MAE(abs_10)
        context['RMSE_10'] = RMSE(abs_10)
        context['MAE_50'] = MAE(abs_50)
        context['RMSE_50'] = RMSE(abs_50)

        return context




