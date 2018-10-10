from guests.models import Guest  # noqa
import random
import itertools  # noqa
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


def generate(starting=0):
    invited_leads = Guest.objects.leads().invited().order_by(
        'family', 'percentile')
    invite_sheet = []
    file_counter = 0
    for guest in invited_leads:
        invite = Invitation()
        party = len(guest.party())
        invite.number = guest.id
        invite.admit = party
        invite.username = guest.username

        if party == 1:
            invite.invitees = str(guest)
        elif party == 2:
            line = f'{guest} & '
            plus_one = guest.party()[1]
            line += 'Guest' if plus_one.unnamed else plus_one.first_name
            invite.invitees = line
        else:
            line = f'{guest.first_name}, '
            plus_one = guest.party()[1]
            line += 'Guest' if plus_one.unnamed else plus_one.first_name
            line += ' & Family'
            invite.invitees = line

        invite_sheet.append(str(invite))
        if len(invite_sheet) >= 4:
            file_counter += 1
            files = [svg.transform.fromstring(inv) for inv in invite_sheet]
            invite_sheet = []

            sheet = svg.transform.SVGFigure(
                files[0].width,
                f'{sum(Decimal(f.height.strip("m")) for f in files)}mm')

            svgs = [f.getroot() for f in files]
            total_height = 0
            for n, svg_file in enumerate(svgs):
                svg_file.moveto(0, total_height)
                height = Decimal(files[n].height.strip("m"))
                height *= 72 / Decimal('25.4') * Decimal('1.25')
                total_height += height

            sheet.append(svgs)
            filename = f'invitations/images/invite_sheet_{file_counter:03}'
            sheet.save(f'{filename}.svg')
            subprocess.call([
                'inkscape',
                '-A',
                f'{filename}.pdf',
                f'{filename}.svg'])
            os.remove(f'{filename}.svg')
            subprocess.call([
                'pstoedit',
                '-dt',
                '-f',
                'dxf:-polyaslines -mm',
                f'{filename}.pdf',
                f'{filename}.dxf'])
            os.remove(f'{filename}.pdf')


def run():
    print('====================================================')
    generate()
