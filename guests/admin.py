from django.contrib import admin
from .models import Guest, Activity, RSVP
from .forms import RSVPForm


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_lead', 'invited', 'username',)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    form = RSVPForm


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
