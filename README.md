# Weather_Station
Usage of Raspberry Pi to predict selected weather forecast parameters based on regression

Do realizacji systemu uzyłem nastepujacych technologi: Django, Python, Java wraz
z biblioteka Weka, Raspberry Pi z wgranym systemem Ubuntu, czujnika BME280 oraz
serwera VPS. Django oraz Python odpowiadaja za backend (logika aplikacji po stronie
serwera)oraz wyswietlanie wykresów. Java wraz z biblioteka Weka odpowiadaja za predykcje
(przewidywanie warunków pogodowych za pomoca analizy szeregów czasowych).
Raspberry Pi wraz z czujnikiem BME280 odpowiadaja za zbieranie danych oraz wysyłanie
ich do bazy danych.

