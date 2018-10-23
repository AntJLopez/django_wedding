from django.contrib import admin
from .models import Guest, Activity, RSVP
from .forms import RSVPForm  # noqa


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_lead', 'invited', 'username',)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    form = RSVPForm
    list_display = ('__str__', 'attending', 'nights_onsite',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
