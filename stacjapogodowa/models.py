from django.db import models

class Odczyty(models.Model):
    data_odczytu = models.DateTimeField()
    temperatura = models.FloatField()
    wilgotnosc = models.FloatField()
    cisnienie = models.FloatField()

    class Meta:
        verbose_name = ("Odczyt")
        verbose_name_plural = ("Odczyty")


class Odczyty_Algorytm(models.Model):
    data_odczytu = models.DateTimeField()
    temperatura = models.FloatField()
    wilgotnosc = models.FloatField()
    cisnienie = models.FloatField()

    class Meta:
        verbose_name = ("Odczyt stworozny przez algorytm")
        verbose_name_plural = ("Odczyty stworzone przez algorytm")

