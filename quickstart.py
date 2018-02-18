from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from dateutil.parser import parse

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
def get_credentials():
	"""Gets valid user credentials from storage.
	If nothing has been stored, or if the stored credentials are invalid, 
	the OAuth2 flow is completed to obtain the new credentials.Returns: Credentials,
	the obtained credential."""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir): os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

	

theStartYear ="0000"
def main():
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
    
	eventsResult = service.events().list(
		calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
		orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	#print(type(events))
   # print(type(events()))
	if not events:
		print('No upcoming events found.')
	#print(events[0].keys())	
	theYear=[]
	theDay=[]
	theMonth=[]
	theHour=[]
	theMinute=[]
	convertedMinutes=[]
	
	
	theDate=[]
	theTime=[]
	totalMins=[]
	
	
	
	theYearE=[]
	theDayE=[]
	theMonthE=[]
	theHourE=[]
	theMinuteE=[]
	convertedMinutesE=[]
	
	
	theDateE=[]
	theTimeE=[]
	totalMinsE=[]
	
	
	
	
	counter =0;
	# for event in events:
		# start = event['start'].get('dateTime', event['start'].get('date'))
		# end = event['end'].get('dateTime', event['end'].get('date'))
		# print(start, event['summary'])
		# print(end, event['summary'])
	i=0
	for event in events:
	
		start = event['start'].get('dateTime', event['start'].get('date'))
		end = event['end'].get('dateTime', event['end'].get('date'))

		#start set
		
		
		#removes the "T"
		afterSplit =start.split("T")
		#removes the "-"
		splitTime = afterSplit[1].split("-")
		
		#splits the time elements up
		getTimeElements = splitTime[0].split(":")
		#splits the date elements
		getDateElements = afterSplit[0].split("-")
		theHour.append(int(getTimeElements[0]))
		
		#print(theHour[counter])
		theMinute.append(int(getTimeElements[1]))
		convertedMinutes.append(int(getTimeElements[0])*60)
		totalMins.append(theMinute[counter]+convertedMinutes[counter])
		print(theHour[counter])
		#end set
		
		#removes the "T"
		afterSplitE =end.split("T")
		#removes the "-"
		splitTimeE = afterSplitE[1].split("-")
		#splits the time elements up
		getTimeElementsE = splitTimeE[0].split(":")
		#splits the date elements
		getDateElementsE = afterSplitE[0].split("-")
		theHourE.append(int(getTimeElementsE[0]))
		theMinuteE.append(int(getTimeElementsE[1]))
		convertedMinutesE.append(int(getTimeElementsE[0])*60)
		totalMinsE.append(theMinuteE[counter]+convertedMinutesE[counter])
		
		
		
		counter+=1


			
		
		# print(convertedMinutes)\
		#print(totalMins)
		#print(totalMinsE)
		
		
		
		#convertedMinutes.append(theMinute[counter]*60)
		#print(convertedMinutes)
		# print(theHour)
		# print(theMinute)
		
		# hourToMinute =theHour[counter]*60
		# counter+=counter
		# print(hourToMinute)
		
		#the hours of the elements
		#print(getTimeElements)
		#theHour.append(getTimeElements)
		#theMinutes.append(getTimeElements)
		#print(getDateElements)
		#print(start)
		#print(theHour[counter][0])
		
		#
		# print(
		# counter+=1
		#print(afterSplit)
		# print(splitTime)
		# print(getTimeElements)
		
		#theHour[event]=getTimeElements[0]
	#	theDate,theTime= zip(*(s.split("T") for s in start))
		#print(event['summary'])
		#print(type(start))
		#print(end, event['summary'])
	#for event in events:
		
        #theStartYear=0
       # temp=0
        #print( "hlll")
        #for x in range(0,3):
         #   theStartYear+=temp[x]
		#int(theStartYear)
		#parseStart = parse(start)
		#print(parseStart.year())
		# print(parseStart.weekday())
		# for x in range(0,3):
			# global theStartYear
			# theStartYear+=start[x]
			
		# theStartYear =start[0]+start[1]+start[2]+start[3]
		# theEndYear =end[0]+end[1]+end[2]+end[3]		
		# theStartMonth = start[5]+start[6]
		# theEndMonth = end[5]+end[6]
		
		
		# theStartTime=start[11]+start[12]+start[13]+start[14]+start[15]
		# theEndTime = end[11]+end[12]+end[13]+start[14]+start[15]
        #y=end
		
		# print( "Start Time : ", theStartTime, "Start Year: ", theStartYear,"Start Month:", theStartMonth, "End Year:", theEndYear,"End Month:", theEndMonth,"End Time: ", theEndTime)
if __name__ == '__main__':
	main()
