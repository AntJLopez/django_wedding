from django.contrib import admin
from .models import Guest, Activity, RSVP


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
