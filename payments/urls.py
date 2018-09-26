from django.urls import path

from . import views


urlpatterns = [
    path('make_gift/', views.make_gift, name='make_gift'),
]
