import datetime

from django.utils import timezone
from dateutil.relativedelta import relativedelta
from reminderduration import durations  # Table for determining reminder durations.
from reminderduration import months  # Table for getting the numeric value of a month


from django.db import models

from reminderduration import index_to_month


class User(models.Model):
  login = models.PositiveIntegerField()
  pin = models.PositiveIntegerField()

  def __unicode__(self):
    return 'User(' + str(self.login) + ',' + str(self.pin) + ')'

  def __str__(self):
    return str(self.__unicode__())


class Birthday(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User)
  last_letter = models.CharField(max_length=1)
  voice_name_url = models.URLField(max_length=500)
  date = models.DateField('birthday date')
  reminder_delta = models.CharField(max_length=10)

  def is_reminder(self):
    """Returns true when a birthday has a reminder."""
    self.date = self.date.replace(year=timezone.now().year)
    thisyear = self.date
    nextyear = self.data + relativedelta(years=1)
    return timezone.now().date() >= thisyear - durations[self.reminder_delta]  and \
           timezone.now().date() <= thisyear or \
           timezone.now().date() >= nextyear - durations[self.reminder_delta]  and \
           timezone.now().date() <= nextyear

  def is_month(self, month):
    return self.date.month == month

  def month_name(self):
    return index_to_month(self.date.month)

  def __unicode__(self):
    return 'Birthday:' + self.last_letter + '  date:' + str(self.date) + '  dur:' + str(durations[self.reminder_delta])

  def __str__(self):
    return str(self.__unicode__())