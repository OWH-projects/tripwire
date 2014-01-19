"""

Who's in the Douglas County Jail?

"""

from mechanize import Browser
from bs4 import *
from time import *
import re
#import datetime
import sys
from django.core.management import setup_environ
sys.path.append('/home/omaha/webapps/dj/myproject')
import settings
setup_environ(settings)
from myproject.tripwire.models import Inmate

#today = str(datetime.date.today().strftime("%m-%d-%Y"))
#f = open('douglas-booked-' + today + '.txt', 'wb')

# crank up a browser
mech = Browser()

# add a user-agent string
mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# ignore robots
mech.set_handle_robots(False)

# define opening url
baseurl = "http://www.dccorr.com/corrections/accepted"

# beautifulsoup that bizzo
counter = 1
while counter < 5:
    try:
        page = mech.open(baseurl)
    except:
        print "Base page didn't open on try No. " + str(counter) +". Feel bad."
        counter += 1
        sleep(30)
    else:
        print "Opened the page."
        break

html = page.read()
print "Reading the page"

soup = BeautifulSoup(html)
print "Souping the page."

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

print "Looping through the alphabet."
for thing in letters:
    # select the correct form on the page
    mech.select_form(nr=1)
    print "Selecting the form."
        
    # fill out the form
    mech.form['lname'] = thing
    print "Filling out the form."
    
    # submit and read in the results page
    req = mech.submit()
    print "Submitting the form."
    
    counter = 1
    while counter < 5:
        try:
            resultspage = req.read()
        except:
            print "Results page didn't open on try No. " + str(counter)
            counter += 1
            sleep(30)
        else:
            print "Opened results page."
            break

    soup = BeautifulSoup(resultspage)
    print "Souping the results page."
    
    # check to see if the search returned any records
    error = re.compile(r'No results matched your query')
    if error.search(str(soup)):    
        print 'Nobody in DCCC has a last name that starts with ' + thing.upper()
        sleep(3)
        mech.back()
        continue
    else:
        pass
        print 'Processing data for inmates whose names start with ' + thing.upper()
    
    # grab the links for each inmate's detail page
    inmatelinks = []
    print "Stuffing detail page links into a list."
    for link in mech.links(url_regex='inmate-details\?datanum'):
        inmatelinks.append(link.url)
        
    # loop through each detail page, collecting data
    print "Looping through detail pages."
    for url in inmatelinks:
        counter = 1
        while counter < 5:
            try:
                page = mech.open(url)
            except:
                print "Couldn't open detail page on try No. " + str(counter)
                counter += 1
                sleep(30)
            else:
                print "Opened the detail page."
                break
                
        html = page.read()
        print "Reading the detail page."
        
        soup = BeautifulSoup(html)
        print "Souping the detail page."
        
        table = soup.find('table', class_='presult')
        print "Finding the correct table."
        
        # get name
        try:
            name = table.findAll('td')[3].get_text().replace("Name","")
            rest = name.split(',')[1].strip()
            last = name.split(',')[0].strip()
        except:
            rest = "TURD"
            last = "MCGURT"
        print "Name: " + rest, last
        
        # get ID number
        try:
            inmate_id = table.findAll('td')[0].get_text(strip=True).replace("Data Number:","")
        except:
            inmate_id = "Not reported"
        print "Inmate ID: " + inmate_id
        
        # get admission date and time
        try:
            rawdate = table.findAll('td')[1].get_text().replace("Admission Date - Time: ","")
            admissiondate = rawdate.split(' - ')[0].strip()
            admissiontime = rawdate.split(' - ')[1].strip()
            admissionmonth = admissiondate[:2]
            admissionday = admissiondate[3:5]
            admissionyear = admissiondate[6:]
            admission = admissionyear + "-" + admissionmonth + "-" + admissionday
        except:
            admission = "Not reported"
            admissiontime = "Not reported"
        print "Admitted: " + admission
        
        # get projected release
        try:
            proj_release = table.findAll('td')[2].get_text().replace("Projected Release Date: ","").strip()
        except:
            proj_release = "Not reported"
        print "Projected release: " + proj_release
        
        # get sex
        try:
            sex = table.findAll('td')[4].get_text(strip=True).replace("Sex","")
        except:
            sex = "Not reported"
        print "Sex: " + sex
        
        # get race
        try:
            race = table.findAll('td')[5].get_text(strip=True).replace("Race")
        except:
            race = "Not reported"
        print "Race: " + race
        
        # get age
        try:
            age = table.findAll('td')[6].get_text(strip=True).replace("Age","")
        except:
            age = "Not reported"
        print "Age: " + age
        
        # get facility
        try:
            facility = table.findAll('td')[7].get_text(strip=True).replace("Facility","")
        except:
            facility = "Not reported"
        print "Facility: " + facility
        
        # get height
        try:
            height = table.findAll('td')[8].get_text(strip=True).replace("Height","")
        except:
            height = "Not reported"
        print "Height: " + height
        
        # get weight
        try:
            weight = table.findAll('td')[9].get_text().replace("Weight","").replace(" lb","").strip()
        except:
            weight = "Not reported"
        print "Weight: " + weight
        
        # create a list to hold the charges
        charges = []
        
        # get the charges
        bad = table.findAll('td')[10].stripped_strings
        
        # append them to the list
        for thing in bad:
            charges.append(thing)
        
        # kill the word "Charges"
        charges.pop(0)
        
        # if multiple charges, join them
        if len(charges) > 1:
            crime = ' | '.join(charges)
        elif len(charges) == 0:
            crime = "Not reported"
        elif len(charges) == 1:
            crime = charges[0]
        print crime
        
        # get bond
        try:
            bond = table.findAll('td')[11].get_text(strip=True).replace("Bond Amount","")
        except:
            bond = "Not reported"
        print "Bond: " + bond
        
        # get fines
        try:
            fines = table.findAll('td')[12].get_text().replace("Fines & Costs: ","")
        except:
            fines = "Not reported"
        print fines
        
        # get fresh
        try:
            findfresh = re.search('Data current as of \d\d/\d\d/\d\d\d\d', str(soup))
            fresh = findfresh.group().replace('Data current as of ','').strip()
        except:
            fresh = "Not reported" 
        print "Data current as of: " + fresh

        # put it all together
        Inmate.objects.create(inmate_id=inmate_id, proj_release=proj_release, last=last, rest=rest, crime=crime, age=age, sex=sex, race=race, height=height, weight=weight, facility=facility, admissiondate=admission, admissiontime=admissiontime, bond=bond, fines=fines, fresh=fresh)

        #fullrecord = (inmate_id, last, rest, crime, admission, proj_release, sex, race, age, height, weight, facility, bond, fines, fresh, "\n")
        
        f.write("\t".join(fullrecord))
        print "Record written."
            
        # navigate back
        mech.back()
        print "Returning ..."
        sleep(1)
            
    counter = 1
    while counter < 5:
        try:
            page = mech.open(baseurl)
        except:
            print "Couldn't open the page on try No. " + str(counter) + ". Stop sucking."
            counter += 1
            sleep(30)
        else:
            print "Back at the beginning. Opened the page."
            break
            
    sleep(1)
    
    html = page.read()
    print "Reading the page."
    
    soup = BeautifulSoup(html)
    print "Souping the page."

#f.flush()
#f.close()