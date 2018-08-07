from django.urls import path

from . import views


urlpatterns = [
    path('', views.guest_list, name='guest_list'),
    path('new', views.guest_create, name='guest_create'),
    path('view/<int:pk>', views.guest_read, name='guest_read'),
    path('edit/<int:pk>', views.guest_update, name='guest_update'),
    path('delete/<int:pk>', views.guest_delete, name='guest_delete'),
]
