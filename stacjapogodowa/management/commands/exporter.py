import datetime
from django.core.management.base import BaseCommand, CommandError
from stacjapogodowa.models import Odczyty
from django.conf import settings
from django.utils import timezone


from pandas import read_csv, np
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def arima_function(self, lista_odczytow):
        X = np.array(lista_odczytow, np.float)

        size = int(len(X) * 0.66)
        train = X[0:size]
        test = X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=(1, 1, 0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (yhat, obs))
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


        odczyty = Odczyty.objects.all()
        ostatni = Odczyty.objects.last()
        odczyty_temp = []
        odczyty_wilgo = []
        odczyty_cis = []
        print ostatni.id
        for odczyt in odczyty:
            odczyty_temp.append(odczyt.temperatura)
            odczyty_wilgo.append(odczyt.wilgotnosc)
            odczyty_cis.append(odczyt.cisnienie)
        temp = self.arima_function(odczyty_temp)
        wilgo = self.arima_function(odczyty_wilgo)
        cis = self.arima_function(odczyty_cis)
        # print X




