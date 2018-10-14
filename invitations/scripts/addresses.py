from guests.models import Guest
import labels
import os
import csv
from reportlab.graphics import shapes
import itertools
from pprint import pprint  # noqa

states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
    'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
    'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
    'WI', 'WY', ]


def add_US_if_state():
    for guest in Guest.objects.all():
        if guest.administrative_area in states and not guest.country:
            print(guest)
            guest.country = 'US'
            guest.save()


def us_addresses():
    for g in Guest.objects.invited():
        if g.country == 'US':
            lines = []
            lines.append(g.thoroughfare)
            if g.premise:
                lines.append(g.premise)
            line = (f'{g.locality}, {g.administrative_area} {g.postal_code}')
            lines.append(line)
            yield (g, lines)


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


def create_labels(folder='invitations/scripts/labels/'):
    def draw_label(label, width, height, obj):
        label.add(
            shapes.String(2, 2, str(obj), fontName='Helvetica', fontSize=10))

    specs = labels.Specification(
        215.9, 279.4, 2, 5, 101.6, 50.8, corner_radius=2)
    guests = Guest.objects.invited().filter(country='US')
    for page_num, page in enumerate(chunks(guests, size=10)):
        sheet = labels.Sheet(specs, draw_label, border=True)
        for guest in page:
            text = f'{guest.party_line()}\n'
            text += '\r'.join(guest.address())
        sheet.add_label(text)
        sheet.save(os.path.join(folder, f'label_sheet_{page_num:02}.pdf'))


def create_us_csv(filename='invitations/scripts/labels/addresses.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Recipient', 'Line 1', 'Line 2', 'State Line'])
        for guest in Guest.objects.leads().invited().filter(country='US'):
            if guest.country == 'US':
                lines = [guest.party_line()].extend(guest.address())
                lines = [guest.party_line()]
                lines.append(guest.thoroughfare)
                lines.append(guest.premise if guest.premise else '')
                line = (f'{guest.locality}, {guest.administrative_area} ')
                line += guest.postal_code
                lines.append(line)
                writer.writerow(lines)


def create_kw_csv(filename='invitations/scripts/labels/kuwait_guests.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Name'])
        for guest in Guest.objects.leads().invited().filter(country='KW'):
            print(guest)
            writer.writerow([str(guest)])


def complete_countries():
    for guest in Guest.objects.invited().leads():
        g = str(guest)
        if not guest.country:
            kw = [' Al ', 'Zamanon', 'Ilene', 'Evita']
            if any(name in g for name in kw):
                print(guest)
                guest.country = 'KW'
                guest.save()
            us = ['Harriman', 'Kwiecinski', 'Marotta', 'Mozill', 'Torta']
            if any(name in g for name in us):
                guest.country = 'US'
                guest.save()
        if not guest.country:
            print(guest)


def run():
    complete_countries()
    create_kw_csv()
