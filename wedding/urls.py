from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wedding import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('guests/', include('guests.urls')),
    path('logout/', views.guest_logout, name='guest_logout'),
    path('<guest_username>/', views.guest_login, name='guest_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
