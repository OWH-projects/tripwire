from tripwire.models import *
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.template.loader import *
from django.core.mail import EmailMultiAlternatives
from time import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'None'
    help = "Send emails to users who are listed in the subscribers model."

    def handle(self, *args, **options):

        lastnames = Name.objects.values("last")
        firstnames = Name.objects.values("first")
    
        firstlist = []
        for obj in firstnames:
            firstlist.append(obj['first'])
    
        recipients = ['matt.wynn@owh.com', 'cody.winchester@owh.com']
    
        jailmatches = SarpyWarrant.objects.filter(last__in=lastnames).filter(reduce(lambda x, y: x |y, [Q(rest__icontains=first) for first in firstlist]))
    
        for obj in jailmatches:
            print obj.rest + ' ' + obj.last

        print jailmatches.count()
