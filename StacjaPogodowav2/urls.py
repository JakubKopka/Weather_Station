"""StacjaPogodowav2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from stacjapogodowa import views
from stacjapogodowa.views import StronaGlownaView, TemperaturaView, CisnienieView, WilgotnoscView, temperatura

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', StronaGlownaView.as_view(), name='StronaGlowna'),
    url(r'^temperatura/', temperatura, name='Temperatura'),
    url(r'^cisnienie/', CisnienieView.as_view(), name='Cisnienie'),
    url(r'^wilgotnosc/', WilgotnoscView.as_view(), name='Wilgotnosc'),
]
