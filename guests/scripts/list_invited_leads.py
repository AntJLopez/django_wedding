from guests.models import Guest
from pprint import pprint  # noqa


def run():
    invited_leads = Guest.objects.leads().invited()
    for guest in invited_leads:
        print(guest)
    print(f'{len(invited_leads)} invitations will go out.')
