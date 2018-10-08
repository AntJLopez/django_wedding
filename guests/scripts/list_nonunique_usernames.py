from guests.models import Guest


def run():
    usernames = set()
    duplicates_found = False
    for guest in Guest.objects.all():
        if not guest.username:
            continue
        if guest.username in usernames:
            duplicates_found = True
            print(f'Duplicate username found: {guest.username}')
        else:
            usernames.add(guest.username)
    if not duplicates_found:
        print('No duplicate usernames found!')
