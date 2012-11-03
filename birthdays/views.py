from birthdays.models import Birthday, User

from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404

import datetime

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
      raise Http404('Incorrect pin: ' + str(request_pin))
  # Handle incorrect login.
  except User.DoesNotExist:
      raise Http404('Login: ' + str(request_login) + 'not found')
  
  # return render_to_response('birthdays/login.html', {'login': u.login})
  return HttpResponse('Successful login! ' + str(u))


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
    raise Http404('Login unavailable: ' + str(request_login))
  # Login does not exist, so move on.
  except User.DoesNotExist:
      pass
  
  # Create new user with login and pin
  u = User(login=request_login, pin=request_pin)

  # Save new user to database
  u.save()
  
  return HttpResponse('Successful new user! ' + str(u))


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
  request_month = int(request.GET['month'])
  request_day = int(request.GET['day'])
  request_reminder_delta = int(request.GET['reminder_delta'])

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
  
  return HttpResponse('Birthday added! ' + str(b))


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
  
  return HttpResponse('Birthday deleted! ' + str(b))


def get_birthdays_list(request):
  """
  Returns a list of birthdays that fit the given query:
    loginID
    birthday_querey

  If no birthdays are found, returns empty list.
  If user does not exist, returns error.
  """
  return HttpResponse("get_birthdays_list page")


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
  return HttpResponse("get_birthdays_pick page")


def update_reminder(request):
  """
  Returns an acknowledgement if birthday's reminder was updated given:
    login
    birthdayID
    reminder_duration

  Returns error if user or birthday are not found.
  """
  return HttpResponse("update_reminder page")
