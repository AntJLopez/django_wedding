from guests.models import Guest


def run(*args):
    for guest in Guest.objects.all():
        names = guest.full_name.split()
        first_name = last_name = ''
        for name in names:
            if name[0] == name[-1] == '"':
                index = names.index(name) + 1
                first_name = ' '.join(names[:index])
                last_name = ' '.join(names[index:])
                continue
            elif name.lower() == 'al':
                index = names.index(name)
                first_name = ' '.join(names[:index])
                last_name = ' '.join(names[index:])
                continue
        if len(names) == 1:
            first_name = names[0]
        if not first_name:
            first_name = ' '.join(names[:1])
            last_name = ' '.join(names[1:])
        fillers = ['wife', 'husband', '?', 'partner', 'guest', 'daughter']
        for filler in fillers:
            if first_name and filler in first_name.lower():
                first_name = ''
            if last_name and filler in last_name.lower():
                last_name = ''
        print(guest.full_name)
        print(f'{first_name} : {last_name}\n')

        if 'write' in args:
            if not guest.first_name:
                guest.first_name = first_name if first_name else ''
            if not guest.last_name:
                guest.last_name = last_name if last_name else ''
            guest.save()
