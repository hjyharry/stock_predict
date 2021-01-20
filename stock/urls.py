from django.contrib import admin
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.refresh),
    url(r'^^\d{6}$',views.stock_detail),
]