from birthdays.models import Birthday, User

from django.http import HttpResponse
from django.http import Http404

from django.shortcuts import render_to_response

from reminderduration import months  # Table for getting the numeric value of a month

import datetime

from helper import is_int
from reminderduration import month_to_index
from reminderduration import index_to_month


def index(request):
  """
  Returns an acknowledgement if birthday is created given:
    login
    last_letter
    voice_name_url
    date
    reminder_duration

  Returns error if any of the data is invalid
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_last_letter = request.GET['last_letter']
  request_voice_name_url = request.GET['voice_name_url']
  request_month = month_to_index(request.GET['month'])
  request_day = int(request.GET['day'])
  request_reminder_delta = request.GET['reminder_delta']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Create new birthday
  d = datetime.date(year = 2012,
                       month = request_month,
                       day = request_day)
  b = Birthday(user = u,
               last_letter = request_last_letter,
               voice_name_url = request_voice_name_url,
               date = d,
               reminder_delta = request_reminder_delta)

  # Save new birthday
  month = index_to_month(b.date.month)
  day = b.date.day
  return render_to_response('birthdays/index.xml', 
                            {'name': b.voice_name_url,
                             'letter': b.last_letter,
                             'month': month,
                             'day': day,
                             'reminder': b.reminder_delta})


def login(request):
  """
  Returns an acknowledgement if user successfully logins with:
    login
    pin
  
  Else, if login is not present on server, returns error message.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_pin = request.GET['pin']
  
  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
    # Check for correct pin.
    if u.pin != int(request_pin):
      print u.pin
      print request_pin
      return render_to_response('birthdays/login_fail.xml', 
                              {'reason':'pin',
                               'num':u.pin})  # Handle incorrect login.
  except User.DoesNotExist:
      return render_to_response('birthdays/login_fail.xml', 
                              {'reason':'login',
                               'num':request_login})  # Handle incorrect login.
        
  return render_to_response('birthdays/login.xml', 
                            {'login':u.login})

def new_user(request):
  """
  Returns an acknowledgement if new user is successfully created given:
    login
    pin
  
  Else, returns error message describing why user could not login.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_pin = request.GET['pin']

  # Login must be 6 digits and pin must be 3
  if len(str(request_login)) != 6 or len(str(request_pin)) != 3:
    raise Http404('Login invalid')

  # Check to see if login is already used.
  try:
    u = User.objects.get(login=request_login)
    # If we've reached this point, the login is already used.
    return render_to_response('birthdays/new_fail.xml', 
                            {'num':request_login})  # Handle incorrect login.  # Login does not exist, so move on
  except User.DoesNotExist:
    # The login is free, so move on.
    pass
  
  # Create new user with login and pin
  u = User(login=request_login, pin=request_pin)

  # Save new user to database
  u.save()
  
  return render_to_response('birthdays/new.xml', 
                          {'login':u.login})  # Handle incorrect login.  # Login does not exist, so move on


def add_birthday(request):
  """
  Returns an acknowledgement if birthday is created given:
    login
    last_letter
    voice_name_url
    date
    reminder_duration

  Returns error if any of the data is invalid
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_last_letter = request.GET['last_letter']
  request_voice_name_url = request.GET['voice_name_url']
  request_month = month_to_index(request.GET['month'])
  request_day = int(request.GET['day'])
  request_reminder_delta = request.GET['reminder_delta']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Create new birthday
  d = datetime.date(year = 2012,
                       month = request_month,
                       day = request_day)
  b = Birthday(user = u,
               last_letter = request_last_letter,
               voice_name_url = request_voice_name_url,
               date = d,
               reminder_delta = request_reminder_delta)

  # Save new birthday
  b.save()
  
  return render_to_response('birthdays/add.xml')


def delete_birthday(request):
  """
  Returns an acknowledgement if birthday is deleted given:
    login
    birthdayID

  Returns error if user or birthday are not found.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_birthday_id = request.GET['birthday_id']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Get birthday from user
  try: 
    b = u.birthday_set.get(pk=request_birthday_id)
  except Birthday.DoesNotExist:
    raise Http404('Login: ' + str(request_login) +
                  ' has no birthday_id: ' + request_birthday_id)

  # Delete the birthday
  b.delete()
  
  return render_to_response('birthdays/delete.xml')


def get_birthdays(u, request_birthday_query):
  """ Returns list of birthdays from user that fit query"""
  # Get birthdays from user using query
  try:
    
    if (request_birthday_query in months):
      print 'Its month'
      # If request_birthday_query is int, filter by month,
      request_birthday_query = months[request_birthday_query]
      birthdays = u.birthday_set.all()
      birthdays = filter(lambda x: x.is_month(request_birthday_query),
                         birthdays)
      
    elif (request_birthday_query == 'all'):
      print 'Its all'
      # If request_birthday_query == all, don't filter,
      birthdays = u.birthday_set.all()

    else:
      print 'Its letter'
      # Else, filter by letter
      birthdays = u.birthday_set.filter(last_letter=request_birthday_query)
      
  except Birthday.DoesNotExist:
    raise Http404('Login: ' + str(request_login) +
                  ' has no birthdays that fit query ' +
                  request_birthday_id)
  
  return birthdays


def get_birthdays_list(request):
  """
  Returns a list of birthdays that fit the given query:
    loginID
    birthday_querey

  If no birthdays are found, returns empty list.
  If user does not exist, returns error.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_birthday_query = request.GET['birthday_query']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Get birthdays from user using query
  birthdays = get_birthdays(u, request_birthday_query)
  num_birthdays = len(birthdays)
   
  return render_to_response('birthdays/list.xml', 
                           {'birthdays':birthdays,
                            'num_birthdays':num_birthdays})    
  

def get_birthdays_pick(request):
  """
  When birthday_num = -1,
  Returns a list of birthdays that fit the given query:
    login
    birthday_querey
    birthday_num = -1

  Else,
  Returns birthdayID for a given birthday in an ordered query:
    login
    birthday_querey
    birthday_num = #

  If no birthdays are found, returns empty list.
  If user does not exist, returns error.
  If birthday number is not pickable in query, returns error.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']
  request_birthday_query = request.GET['birthday_query']
  #request_birthday_num = int(request.GET['birthday_num'])

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Get birthdays from user using query
  birthdays = get_birthdays(u, request_birthday_query)


  # Just list the birthdays like normal until the user picks one.
  num_birthdays = len(birthdays)
  if num_birthdays:
    return render_to_response('birthdays/listpick.xml', 
                             {'birthdays':birthdays,
                              'num_birthdays':num_birthdays})
  else:
    return render_to_response('birthdays/no_found.xml',)
    

def update_reminder(request):
  """
  Returns an acknowledgement if birthday's reminder was updated given:
    login
    birthdayID
    reminder_delta

  Returns error if user or birthday are not found.
  """
  request_login = request.GET['login']
  request_birthday_id = request.GET['birthday_id']
  request_reminder_delta = request.GET['reminder_delta']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Get birthday from user
  try: 
    b = u.birthday_set.get(pk=request_birthday_id)
  except Birthday.DoesNotExist:
    raise Http404('Login: ' + str(request_login) +
                  ' has no birthday_id: ' + request_birthday_id)

  # Update reminder
  b.reminder_delta = request_reminder_delta
  b.save()
  
  return render_to_response('birthdays/update.xml',
                            {'reminder':b.reminder_delta})


def get_reminders(request):
  """
  Returns a list of birthdays with reminders for user:
    loginID

  If user does not exist, returns error.
  """
  # Get request parameters
  print 'REQUEST: ',request.body, request.GET
  
  request_login = request.GET['login']

  # Retrieve user based on login, or raise error.
  try:
    u = User.objects.get(login=request_login)
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')

  # Get all the birthdays
  birthdays = get_birthdays(u, 'all')
  
  # Filter out only those that have reminders
  birthdays = [b for b in birthdays if b.is_reminder()]
  num_birthdays = len(birthdays)
   
  return render_to_response('birthdays/reminders.xml', 
                           {'birthdays':birthdays,
                            'num_birthdays':num_birthdays})
