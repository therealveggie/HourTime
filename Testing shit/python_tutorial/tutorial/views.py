from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import *
from tutorial.outlookservice import get_me,get_my_messages
from tutorial.outlookservice import get_my_events

import datetime


try:
	import argparse
	flags = tools.argparser.parse_args([])
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
from tkinter import *
from math import *

start1=[]
start2=[]
end1=[]
end2=[]


hardstart = [2,10,30,100]
hardend = [5,20,70,150]

hardstart2 = [3,20,70,200]
hardend2= [15,60,100,250]


user = 0
sign_in_url=""
# Create your views here.
import pdb
def home(request):
  global user
  if request.GET.get('ggbtn'):
  	if user==0:
  		user=1
  		start1,end1=google()
  		person="the other person"
  	elif user==1:
  		start2 , end2 = google()
  		return final(request)
  
  redirect_uri = request.build_absolute_uri(reverse('getoken'))
  sign_in_url = get_signin_url(redirect_uri)
  pdb.set_trace()
  if user==0:
  		person="your"
  if user==1:
  		person="the other person's"
  return render(request, 'tutorial/home.html', {'sign_in_url':sign_in_url, 'person':person} )
  #return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def getoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('getoken'))
  token = get_token_from_code(auth_code, redirect_uri)


  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']
  expiration = int(time.time()) + expires_in - 300
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  request.session['user_email'] = user['mail']
  return HttpResponseRedirect(reverse('events'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('getoken')))
  user_email = request.session['user_email']
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('home'))
  else:
    messages = get_my_messages(access_token, user_email)
    context= {'messages': messages['value']}
    return render(request, 'tutorial/mail.html', context)

def final(request):
	context=intersect(start1,end1,start2,end2)
	return render(request, 'tutorial/events.html', {'events':context})


def events(request):
  global user,start1,start2,end1,end2
  access_token = get_access_token(request, request.build_absolute_uri(reverse('getoken')))
  user_email = request.session['user_email']
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('home'))
  else:

    events = get_my_events(access_token, user_email)
    unrefined = { 'events': events['value'] } 
    start,end = refine(unrefined)
    if user==0:
    	user=1
    	start1=start
    	end1=end
    	return HttpResponseRedirect('https://login.windows.net/common/oauth2/logout?post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F')
    	#return render(request, 'tutorial/home.html', {'sign_in_url':sign_in_url, 'person':'the other person\'s'})
    else:
    	start2=start
    	end2=end
    return final(request)

def refine(source):
	import pdb
	result = []
	start_time=[]
	end_time=[]

	for event in source['events']:
		string= event['start']['dateTime']
		pdb.set_trace()
		if string[:8]=="2018-02-" and (int(string[8:10])>=19 and  int(string[8:10])<=25):
			day=int(string[8:10])
			hour, minute = map(int,string[11:16].split(':'))
			day-=19
			day*=24
			hour+=day-6
			hour*=60
			minute+=hour
			start_time.append(minute)
			
			string = event['end']['dateTime']
			day=int(string[8:10])
			hour, minute = map(int,string[11:16].split(':'))
			day-=19
			day*=24
			hour+=day-6
			hour*=60
			minute+=hour
			end_time.append(minute)

			event['subject']=str(minute)
			result.append(event)
		
	return start_time,end_time


def intersect (startTime,endTime, startTime2, endTime2, *args):
    freeTime =[]
    freeTime2 = []
    freeMixed = []

        
    for i in range (0, len(startTime)-1):
        freeTime+= list(range(endTime[i], 1+startTime[i+1]))
    for i in range(len(startTime2)-1):
        freeTime2+= list(range(endTime2[i], 1+ startTime2[i+1]))
        
    max1= freeTime[len(freeTime)-1]
    max2= freeTime2[len(freeTime2)-1]

    min1= startTime[0]
    min2= startTime2[0]

    while (max1<=10080):
        freeTime.append(max1)
        max1=max1+1
    while (max2<=10080):
        freeTime2.append(max2)
        max2=max2+1

    while (min1 > 0):
        freeTime.append(min1)
        min1=min1-1
    while (min2 > 0):
        freeTime2.append(min2)
        min2=min2-1
        

    intersect =sorted(list(set(freeTime) & set(freeTime2)))
    theArray=[]

    for i in range(0,len(intersect)-1):
        if (intersect[i+1] - intersect[i] != 1):
        
            h1 =str(int(intersect[i]/60))
            r1 =str(int(intersect[i]%60))
            
            h2 =str(int(intersect[i+1]/60))
            r2 =str(int(intersect[i+1]%60))
            
            p1 = h1+":"+r1
            p2 =h2+":"+r2
            together = p1 +" to " +p2
            #print(rd)
           

            freeMixed.append({"date": "TBI", "start": p1, "end": p2})
        
            
        i=i+1
    return freeMixed

			
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
def google():
	import pdb
	pdb.set_trace()
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	maxResults=False
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	
	eventsResult = service.events().list(
		calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
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
	
	day=0
	
	
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
		
		# if(theHour[counter-1]>theHour[counter]):
			 # break
		#if(theDate){
		#20
		
		if(int(getDateElements[2]) ==20):
			totalMins[counter] =totalMins[counter]+(60*24)
			day =20
			
		if(int(getDateElementsE[2]) ==20):
			totalMinsE[counter] =totalMinsE[counter]+(60*24)
			day =20
			
		#21
		if(int(getDateElements[2]) ==21):
			totalMins[counter] =totalMins[counter]+(60*48)
			day =21
			
		if(int(getDateElementsE[2]) ==21):
			totalMinsE[counter] =totalMinsE[counter]+(60*48)
			day =21
			
		#22
		if(int(getDateElements[2]) ==22):
			totalMins[counter] =totalMins[counter]+(72*60)
			day =22
			
		if(int(getDateElementsE[2]) ==22):
			totalMinsE[counter] =totalMinsE[counter]+(72*60)
			day =22
			
			
		#23
		if(int(getDateElements[2]) ==23):
			totalMins[counter] =totalMins[counter]+(60*96)
			day =23
			
		if(int(getDateElementsE[2]) ==23):
			totalMinsE[counter] =totalMinsE[counter]+(60*96)
			day =23
			
		#24
		if(int(getDateElements[2]) ==24):
			totalMins[counter] =totalMins[counter]+(60*120)
			day =24
			
		if(int(getDateElementsE[2]) ==24):
			totalMinsE[counter] =totalMinsE[counter]+(60*120)
			day =24
		
		#25
		if(int(getDateElements[2]) ==25):
			totalMins[counter] =totalMins[counter]+(60*144)
			day =25
			
		if(int(getDateElementsE[2]) ==25):
			totalMinsE[counter] =totalMinsE[counter]+(60*144)
			day =25
		#print(getDateElements[2])
		
		rebuiltDate ="2018" + "-"+"02"+"-"+str(day)
		
		counter+=1
	return totalMins,totalMinsE