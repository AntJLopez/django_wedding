from guests.models import Guest
from pprint import pprint  # noqa


def run():
    invited = Guest.objects.invited()
    invited_leads = invited.leads().order_by(
        'family', 'percentile', 'last_name')

    print(f'Invitations: {len(invited_leads)}')
    print(f'Invited: {len(invited)}')
    print(f'Estimated Attendees: {round(sum(g.likelihood for g in invited))}')
