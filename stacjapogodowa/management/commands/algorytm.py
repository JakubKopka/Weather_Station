import datetime
from django.core.management.base import BaseCommand, CommandError
# from statsmodels.compat import numpy

from stacjapogodowa.models import Odczyty
from django.utils import timezone
from django.conf import settings


from pandas import read_csv, np
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

class Command(BaseCommand):
    args = ''
    help = 'xyz'
    p = 7  # parametr autoregresyjny
    d = 0  # rzad roznicowania
    q = 1  # parametr sredniej ruchomej

    def arima_function(self, lista_odczytow):
        X = np.array(lista_odczytow, np.float)

        size = int(len(X) * 0.66)
        train = X[0:size]
        test = X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=(self.p, self.d, self.q))

            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('przewidywane=%f, prawdziwy=%f' % (yhat, obs))
        # plot
        pyplot.plot(test)
        pyplot.plot(predictions, color='red')
        pyplot.show()
        return predictions
        # pyplot.plot(test)
        # pyplot.plot(predictions, color='red')
        # pyplot.show()


    def handle(self, *args, **options):
        # Odpalenie tego:
        # python manage.py exporter
        # przyklad: https://coderwall.com/p/k5p6ag/run-django-commands-using-cron
        # co 15 minut w cron
        # */15 * * * * python /var/www/myapp/manage.py exporter
        # * * * * * /path/to/virtualenv/bin/python /path/to/project/manage.py management_command


        # Wykonanie alogrytmu analizy szeregow czasowych
        # Ponizszy kod bierze wszystkie odczyty z ostatniej godziny tz. mam np 13:58, algorytm bierze wszystkie obiekty
        # od godziny 13 do 13:58

        # czas_teraz = timezone.now()
        # # czas_h_do_tylu = czas_teraz - datetime.timedelta(hours=1)
        # only_hour = datetime.datetime(czas_teraz.year, czas_teraz.month, czas_teraz.day, czas_teraz.hour, 0, 0)
        # obiekty = Odczyty.objects.filter(data_odczytu__range=(only_hour, czas_teraz))
        # print "Godzina do: ", czas_teraz
        # print "Godzina od ", only_hour
        # for i in obiekty:
        #     print i.data_odczytu

        # aktualna_ilosc = len(Odczyty.objects.all())
        # while True:
        #     teraz = len(Odczyty.objects.all())
        #     if aktualna_ilosc < teraz:
        #         print "Weszlo"
        #         aktualna_ilosc = len(Odczyty.objects.all())


        odczyty = Odczyty.objects.all().order_by('-id')[20:200]
        odczyty = reversed(odczyty)

        do_przewidywania = Odczyty.objects.all().order_by('-id')[:20]
        do_przewidywania = reversed(do_przewidywania)
        ostatni = Odczyty.objects.last()
        odczyty_temp = []
        odczyty_wilgo = []
        odczyty_cis = []

        for odczyt in odczyty:
            odczyty_temp.append(odczyt.temperatura)
            odczyty_wilgo.append(odczyt.wilgotnosc)
            odczyty_cis.append(odczyt.cisnienie)
        # temp = self.arima_function(odczyty_temp)
        # wilgo = self.arima_function(odczyty_wilgo)
        # cis = self.arima_function(odczyty_cis)
        # from datetime import timedelta
        # x = datetime.now()
        # y = x +timedelta(minutes=3)
        # print X

        # build model and fit

        # load required modules
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        # import statsmodels.api as sm
        # # mod1 = sm.tsa.SARIMAX(odczyty_temp, order=(4, 1, 1))
        # # res1 = mod1.fit()
        # # res1.forecast(50)
        # #
        # # # mod2 = sm.tsa.SARIMAX(odczyty_temp, order=(4, 1, 1))
        # # # res2 = mod2.filter(res1.params)
        # # print res1.forecast(50)
        # model = sm.tsa.ARIMA(odczyty_temp, order=(1, 0, 0))
        # results = model.fit(disp=0)
        # print results.forecast(10)

        # X = odczyty_temp
        # size = int(len(X) * 0.75)
        # train, test = X[0:size], X[size:len(X)]
        # model = ARIMA(train, order=(5, 1, 0))
        # results_AR = model.fit(disp=0)
        # preds = results_AR.predict(size + 1, size + 16)
        # pyplot.plot(test[0:17])
        # pyplot.plot(preds, color='red')
        # pyplot.show()
        #
        # from pandas import Series
        # from statsmodels.tsa.arima_model import ARIMA
        # import numpy
        #



        # Kodzik ze strony: https://machinelearningmastery.com/make-sample-forecasts-arima-python/

        # create a differenced series
        # def difference(dataset, interval=1):
        #     diff = list()
        #     for i in range(interval, len(dataset)):
        #         value = dataset[i] - dataset[i - interval]
        #         diff.append(value)
        #     return np.array(diff)
        #
        # # invert differenced value / odwroc roznice wartosci
        # def inverse_difference(history, yhat, interval=1):
        #     return yhat + history[-interval]
        #
        # X = odczyty_temp
        # days_in_year = 160
        # differenced = difference(X, days_in_year)
        # # fit model
        # model = ARIMA(X, order=(self.p, self.d, self.q))
        #
        # model_fit = model.fit(disp=0)
        # print(model_fit.summary())
        # # multi-step out-of-sample forecast
        # forecast = model_fit.forecast(steps=20)[0]
        # print "-------------------------------------------------"
        # # invert the differenced forecast to something usable / odwroc prognoze roznic na cos uzytecznego
        # history = [x for x in X]
        # day = 1
        # przewidywanie = list()
        # for yhat in forecast:
        #     inverted = inverse_difference(history, yhat, days_in_year)
        #     przewidywanie.append(yhat)
        #     print('Day %d: %f ---- %f' % (day, yhat, inverted))
        #     history.append(inverted)
        #     day += 1
        # d = 1
        # prawddziwy = list()
        # for y in do_przewidywania:
        #     print d, " : ", y.temperatura
        #     prawddziwy.append(y.temperatura)
        #     d += 1
        #
        # pyplot.plot( przewidywanie)
        # pyplot.plot(prawddziwy, color='red')
        # pyplot.show()

        # create a differenced series
        def difference(dataset, interval=1):
            diff = list()
            for i in range(interval, len(dataset)):
                value = dataset[i] - dataset[i - interval]
                diff.append(value)
            return np.array(diff)

        # invert differenced value
        def inverse_difference(history, yhat, interval=1):
            return yhat + history[-interval]


        # seasonal difference
        X = odczyty_temp
        days_in_year = 160
        #differenced = difference(X, days_in_year)
        # fit model
        model = ARIMA(X, order=(5, 1, 5))
        model_fit = model.fit(disp=0)
        # multi-step out-of-sample forecast
        forecast = model_fit.forecast(steps=20)[0]
        # invert the differenced forecast to something usable
        history = [x for x in X]
        day = 1
        for yhat in forecast:
            inverted = inverse_difference(history, yhat, days_in_year)
            print('Day %d: %f' % (day, yhat))
            history.append(yhat)
            day += 1
        for i in do_przewidywania:
            print(i.temperatura)

        # weka





