# caps-cal-convert
This converts a public Google Calendar address into a .ics file

My favorite hockey team only provides their calendar as a Google Calendar link that you can subscribe to. I wanted to show the games on my [Inkycal](https://github.com/aceisace/Inkycal) which only supports direct links to ics files or local ics files.

I created a simple script that will take a Google Calendar public link and will create an ics file from that.

## Set-up
Copy `convert.py` and edit the first few lines.
1. Set your timezone
2. Go to google calendar, find the calendar in question from the list on the left side and click on "settings". Copy the Public URL into `public_url` in the python file.
3. Change the save file path if desired.

## Notes
- The file only goes through the next two-ish months of events to create the ics file because my Inkycal only shows a few weeks of events. If you want more events, you can change the number in the line `while c < 2:` to be something more and it will show more events.
- This will only work with public urls built and published with Google Calendar because it parses the html page that google calendar uses to show events. I recommend looking for an ics link for this calendar you want to see first, before using this. Most places will let you find the direct ics link, but in this case it was not available.
