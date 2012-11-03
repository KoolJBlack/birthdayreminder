from birthdays.models import Birthday, User

from django.template import Context, loader
from django.http import HttpResponse


def login(request):
  """
  Returns an acknowledgement if user successfully logins with:
    login
    pin
  
  Else, if login is not present on server, returns error message.
  """
  return HttpResponse("login page")


def new_user(request):
  """
  Returns an acknowledgement if new user is successfully created given:
    login
    pin
  
  Else, returns error message describing why user could not login.
  """
  return HttpResponse("new_user page")


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
  return HttpResponse("add_birthday page")


def delete_birthday(request):
  """
  Returns an acknowledgement if birthday is deleted given:
    login
    birthdayID

  Returns error if user or birthday are not found.
  """
  return HttpResponse("delete_birthday page")


def update_reminder(request):
  """
  Returns an acknowledgement if birthday's reminder was updated given:
    login
    birthdayID
    reminder_duration

  Returns error if user or birthday are not found.
  """
  return HttpResponse("update_reminder page")
