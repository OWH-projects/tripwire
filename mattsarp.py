from mechanize import Browser
from bs4 import *
from time import *
import re
import datetime
import sys
from django.core.management import setup_environ
sys.path.append('/home/mwynn/django_projects/myproject')
import settings
setup_environ(settings)
from myproject.tripwire.models import SarpyWarrant
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# crank up a browser
mech = Browser()

# add a user-agent string
mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# ignore robots
mech.set_handle_robots(False)

# define opening url
baseurl = "http://www.sarpy.com/sheriff/warrants/Results.asp?lname=&fname=&sType=0&Disclaimer=0"

# beautifulsoup that bizzo
page = mech.open(baseurl)
soup = BeautifulSoup(page)
clicks = soup.findAll('form')

numwarrants = len(clicks)
print "\nSlurping up " + str(numwarrants) + " active warrants ...\n=============================\n"

count = 0
while (count < numwarrants):
    record = soup.findAll('tr')[2:][count]
    mouseovercontent = record.find('td', onmouseover=True)['onmouseover']

    #identifying the record and the various parts
    cells = record.findAll('td')
    rawissued = cell[1].text
    rawfullname = cell[2].text.split()
    race = cells[4].text
    rawdob = cells[5].text
    warrantstatus = cells[6].text
    
    #Get our last name separate from the rest
    last = rawfullname[0]
    rest = " ".join(rawfullname[:1])
    
    #Clean up our dob
    dobsplit = rawdob.split('/')
    if len(dobsplit) > 1:
        #Ensure first element has two characters
        if len(dobsplit[0]) == 1:
            dobmonth = "0" + dobsplit[0]
        else:
            dobmonth = dobsplit[0]
        #Then do the same for the day
        if len(dobsplit[1]) == 1:
            dobday = "0" + dobsplit[1]
        else:
            dobday = dobsplit[1]
        cleandob = dobsplit[2] + "-" + dobmonth + "-" + dobday
    else:
        cleandob = '1900-01-01'
    
    charge = BeautifulSoup(mouseovercontent).findAll('font')[4].text
    
    print rest.upper() + " " + last.upper()
    
    if SarpyWarrant.objects.filter(last=last, rest=rest, issued=issued).count() > 0:
	    pass
    else:	
        SarpyWarrant.objects.create(last=last, rest=rest, dob=cleandob, race=race, issued=issued, type=warrantstatus, charge=charge)

    count = count + 1
	
