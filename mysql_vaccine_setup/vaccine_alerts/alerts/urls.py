from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_info', views.add_information, name='add_info'),
    path('go_back', views.index, name='index_2')
]