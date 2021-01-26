from django.urls import path

from . import views

app_name = 'deals'
urlpatterns = [
    path('statistic/', views.statistic, name='statistic'),
    path('loader/', views.loader, name='loader'),
]