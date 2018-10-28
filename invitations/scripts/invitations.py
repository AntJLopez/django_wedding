from guests.models import Guest  # noqa
import random
import itertools  # noqa
import csv
from pprint import pprint  # noqa
from bs4 import BeautifulSoup
from num2words import num2words as num2word
from word2number.w2n import word_to_num as word2num
import svgutils as svg
from decimal import Decimal
import subprocess
import os


class Invitation():
    def tag(self, tag_name):
        tag_dict = {
            'admit': 'tspan3643',
            'invitees': 'tspan3645',
            'number': 'tspan3641',
            'username': 'tspan3499',
        }
        if tag_name in tag_dict:
            tag_name = tag_dict[tag_name]
        return self.soup.find(id=tag_name)

    def __init__(self, template='invitations/scripts/invitation_template.svg'):
        with open(template, encoding='utf-8') as f:
            self.soup = BeautifulSoup(f.read(), 'xml')

    def __str__(self):
        return str(self.soup)

    @property
    def admit(self):
        return word2num(self.tag('admit').string.split(' ', 1)[1])

    @admit.setter
    def admit(self, admit_num):
        admit_tag = self.tag('admit')
        admit_tag.string = f'ADMIT {num2word(admit_num).upper()}'

    @property
    def invitees(self):
        return self.tag('invitees').string

    @invitees.setter
    def invitees(self, invitees):
        self.tag('invitees').string = invitees

    @property
    def number(self):
        return int(self.tag('number').string[-3:])

    @number.setter
    def number(self, number):
        self.tag('number').string = f'No. {random.randint(1, 9)}{number:03}'

    @property
    def username(self):
        return self.tag('username').string

    @username.setter
    def username(self, username):
        self.tag('username').string = username

    def write(self, filename='invitations/scripts/invitation.svg'):
        with open(filename, 'w', newline='\n', encoding='utf-8') as f:
            f.write(str(self))


def test():
    invite1 = Invitation()
    invite1.number = 5
    invite1.admit = 10
    invite1.username = 'shittyrobots'
    invite1.write('invitations/images/invite1.svg')
    invite2 = Invitation()
    invite2.number = 200
    invite2.username = 'joe'
    invite2.admit = 2
    invite2.write('invitations/images/invite2.svg')


def invitations(
        filename='invitations/images/invitation_information.csv',
        max=None, return_all=False):
    MAX_LINE_LENGTH = 28

    invited_leads = Guest.objects.leads().invited().order_by(
        'family', 'percentile')
    if not return_all:
        invited_leads = invited_leads.filter(invite_printed=False)
    if max:
        invited_leads = itertools.islice(invited_leads, max)

    csvfile = open(filename, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Recipient', 'ID', 'Invite Number'])
    for invite_number, guest in enumerate(invited_leads):
        writer.writerow([str(guest), guest.id, f'{invite_number + 1:03}'])
        invite = Invitation()
        party = len(guest.party())
        invite.number = guest.id
        invite.admit = party
        invite.username = guest.username

        if party == 1:
            invite.invitees = str(guest)
        elif party == 2:
            plus_one = guest.party()[1]
            if plus_one.unnamed():
                line = f'{guest} & Guest'
                if len(line) > MAX_LINE_LENGTH:
                    line = f'{guest.first_name} & Guest'
                invite.invitees = line
            elif guest.last_name == plus_one.last_name:
                first_names = f'{guest.first_name} & {plus_one.first_name}'
                line = f'{first_names} {guest.last_name}'
                if len(line) > MAX_LINE_LENGTH:
                    line = first_names
                invite.invitees = line
            else:
                line = f'{guest} & {plus_one}'
                if len(line) > MAX_LINE_LENGTH:
                    line = f'{guest} & {plus_one.first_name}'
                if len(line) > MAX_LINE_LENGTH:
                    line = f'{guest.first_name} & {plus_one.first_name}'
                if len(line) > MAX_LINE_LENGTH:
                    line = f'{guest.first_name} & Guest'
                invite.invitees = line
        else:
            line = f'{guest.first_name}, '
            plus_one = guest.party()[1]
            line += 'Guest' if plus_one.unnamed() else plus_one.first_name
            line += ' & Family'
            if len(line) > MAX_LINE_LENGTH:
                line = f'{guest.first_name} & Family'
            invite.invitees = line

        yield str(invite)
    csvfile.close()


def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


def svg_to_pdf(filename, clean_up=True):
    subprocess.call([
        'inkscape',
        '-A',
        f'{filename}.pdf',
        f'{filename}.svg'])
    if clean_up:
        os.remove(f'{filename}.svg')


def pdf_to_dxf(filename, clean_up=True):
    subprocess.call([
        'pstoedit',
        '-dt',
        '-f',
        'dxf:-mm',
        f'{filename}.pdf',
        f'{filename}.dxf'])
    if clean_up:
        os.remove(f'{filename}.pdf')


def pdf_to_ai(filename, clean_up=True):
    subprocess.call([
        'pstoedit',
        '-dt',
        '-f',
        'ps2ai',
        f'{filename}.pdf',
        f'{filename}.ai'])
    if clean_up:
        os.remove(f'{filename}.pdf')


def mm2px(mm):
    return mm * 72 / Decimal('25.4') * Decimal('1.25')


def px2mm(px):
    return px / Decimal('1.25') * Decimal('25.4') / 72


def generate_invitation_sheets(group_size=4, vertical=False):
    for c, invite_group in enumerate(chunks(invitations(), group_size)):
        files = [svg.transform.fromstring(inv) for inv in invite_group]

        template_width = Decimal(files[0].width.strip('m'))
        template_height = Decimal(files[0].height.strip('m'))

        if vertical:
            sheet = svg.transform.SVGFigure(
                f'{template_width}mm',
                f'{template_height * len(files)}mm')
        else:
            sheet = svg.transform.SVGFigure(
                f'{2 * template_width}mm',
                f'{2 * template_height}mm',
            )

        svgs = [f.getroot() for f in files]
        for n, svg_file in enumerate(svgs):
            if vertical:
                svg_file.moveto(0, mm2px(n * template_height))
            else:
                x = n // 2 * template_width
                y = n % 2 * template_height
                svg_file.moveto(mm2px(x), mm2px(y))
        sheet.append(svgs)

        filename = f'invitations/images/invite_sheet_{c + 1:03}'
        sheet.save(f'{filename}.svg')
        svg_to_pdf(filename, clean_up=False)
        pdf_to_dxf(filename, clean_up=False)


def generate_invitation_singles():
    for c, invite in enumerate(invitations()):
        filename = f'invitations/images/invitation_{c + 1:03}'
        with open(f'{filename}.svg', 'w', newline='\n', encoding='utf-8') as f:
            f.write(invite)
        svg_to_pdf(filename)
        pdf_to_dxf(filename)


def run():
    generate_invitation_singles()
    # svg_to_pdf('invitations/images/cut_template_sheet')
    # pdf_to_dxf('invitations/images/cut_template_sheet')
