from guests.models import Guest
from pprint import pprint  # noqa


def run():
    invited_leads = Guest.objects.leads().invited().order_by(
        'family', 'percentile')
    for guest in invited_leads:
        print(f'{guest} ({guest.percentile})')
    print(f'{len(invited_leads)} invitations will go out.')
