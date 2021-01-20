"""stock_predict URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include

import login.views
import stock.urls

urlpatterns = [
    url(r'^admin/',admin.site.urls),

    url(r'index/',include(stock.urls)),

    url(r'^login/',login.views.login),
    url(r'^register/',login.views.register),
    url(r'^logout/',login.views.logout),
    url(r'^home/',login.views.home),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^refresh',login.views.refresh_captcha)
]
