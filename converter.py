import base64
import requests
from bs4 import BeautifulSoup
import random, string
import datetime

# Set things about your file
timezone = 'America/New_York'
partial_url = "https://calendar.google.com/calendar/u/0/htmlembed?src=nhl_23_%2557ashington%2B%2543apitals%23sports@group.v.calendar.google.com&ctz=America/New_York"
where_to_save_ics = "/home/pi/caps-cal-convert/converted.ics"

# get the first date of the month
today = datetime.date.today()
nextmonth = int(today.strftime("%m"))+1
if nextmonth < 10:
	nextmonth = "0"+str(nextmonth)
else:
	nextmonth = str(nextmonth)

date_in_url = today.strftime("%Y%m")+"01" + "/" + today.strftime("%Y")+nextmonth+"01"
#print(date_in_url)

# in the future edit the date so it's the start of today's month
url = partial_url+"&dates="+date_in_url

first_month = requests.get(url)
first_month.encoding = 'utf-8'
first_month_soup = BeautifulSoup(first_month.text, 'html.parser')

nextbutton = first_month_soup.find_all('a')[2]
next_url = nextbutton['href']

second_month = requests.get(next_url)
second_month.encoding = 'utf-8'
second_month_soup = BeautifulSoup(second_month.text, 'html.parser')

# iterates through every game this month
soup = first_month_soup
c = 0

events = []
while c < 2:
	print(c)
	for i in soup.find_all('a', {"class": "event-link"}):
		event = {}
		#print(i)
		
		# get event title
		event_title = i.find_all('span')[1].get_text()
		print('event title', event_title)
		event['SUMMARY:'] = event_title
		
		# gets the event url 
		idtext = i["href"]
		idforurl = idtext[6:len(idtext)]
		url_front = "https://www.google.com/calendar/event?action=VIEW&"
		event_url = url_front + idforurl

		# calls the event url
		event_html = requests.get(event_url)
		event_html.encoding = 'utf-8'
		event_soup = BeautifulSoup(event_html.text, 'html.parser')

		# parses the event html to get the start time
		event_times = event_soup.find_all('table')[1].find_all('time')

		start_time = event_times[0]['datetime']
		end_time = event_times[1]['datetime']
		print('start', start_time)
		print('end', end_time)
		event['DTSTAMP:'] = start_time
		event['DTSTART:'] = start_time
		event['DTEND:'] = end_time

		print("")

        # checks to make sure that the event is not already in the list (each month shows events from the last week of the previous month and from the first week of the next month)
		if event not in events:
			events.append(event)
	soup = second_month_soup
	c = c + 1

# creates a random uid for the event
# if the uid is the same as any other events, that event will not be displayed because of how ics works
# also, I added this to the event list after, because before I need to compare events to see if they're the same as previous events and if there's a unqiue uid it will not work
for i in events:
	x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
	i['UID:'] = x + '@outlook.com'
	
# the beginning of the ics file is always the same
full_text = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//CSV to iCal Convertor//Chimbori, https://ical.chimbori.com//EN\nCALSCALE:GREGORIAN\nX-WR-CALNAME;VALUE=TEXT:sample\nX-WR-TIMEZONE:'+timezone+'\n'

# for each event in the list, add all the info to the text
for i in events:
	full_text = full_text + 'BEGIN:VEVENT\n'
	full_text = full_text + 'SUMMARY:'+ i['SUMMARY:'] + '\n'
	full_text = full_text + 'DTSTAMP:'+ i['DTSTAMP:'] + '\n'
	full_text = full_text + 'DTSTART:'+ i['DTSTART:'] + '\n'
	full_text = full_text + 'DTEND:'+ i['DTEND:'] + '\n'
	full_text = full_text + 'UID:'+ i['UID:'] + '\n'
	full_text = full_text + 'END:VEVENT\n'
# don't foget to end the file with this line
full_text = full_text + 'END:VCALENDAR'

print(full_text)

# write to text file
file1 = open(where_to_save_ics,"w") 
file1.write(full_text)
file1.close()


