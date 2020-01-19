"""medisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.shortcuts import HttpResponse
# import pymysql
from login import views
from . import view

# urlpatterns = [
#     path('hello/', view.hello),
# ]





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.taghome),
    path('login/',views.login),
    path('register/',views.register),
    # path('index/',views.index),
    # path('example1/',views.example1),
    # path('taglogistic/',views.taglogistic),
    # path('example2/',views.example2),
    # path('example3/',views.example3),
    # path('check/',views.check),
    # path('check2/',views.check2),
    # path('look/',views.look),
    # path('modify/',views.modify),
    # path('logout/', views.logout),
    # path('tagging/', views.tagging),
    # path('tagnext/', views.tagnext),
    # path('tagbefore/', views.tagbefore),
    # path('ajaxmethod/', views.ajaxmethod),
    # path('savetag/', views.savetag),
    # path('modifytag/', views.modifytag),
]