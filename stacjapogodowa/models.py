from django.db import models

class Odczyty(models.Model):
    data_odczytu = models.DateTimeField()
    temperatura = models.FloatField()
    wilgotnosc = models.FloatField()
    cisnienie = models.FloatField()

    class Meta:
        verbose_name = ("Odczyt")
        verbose_name_plural = ("Odczyty")


class Odczyty_50(models.Model):
    data_odczytu = models.DateTimeField()
    temperatura = models.FloatField()
    wilgotnosc = models.FloatField()
    cisnienie = models.FloatField()

    class Meta:
        verbose_name = ("Odczyt stworozny przez algorytmy dla 50 do przodu")
        verbose_name_plural = ("Odczyty stworzone przez algorytmy dla 50 do przodu")

class Odczyty_10(models.Model):
    data_odczytu = models.DateTimeField()
    temperatura = models.FloatField()
    wilgotnosc = models.FloatField()
    cisnienie = models.FloatField()

    class Meta:
        verbose_name = ("Odczyt stworozny przez algorytmy dla 10 do przodu")
        verbose_name_plural = ("Odczyty stworzone przez algorytmy dla 10 do przodu")