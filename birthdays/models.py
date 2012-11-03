import datetime

from django.utils import timezone
from reminderduration import durations  # Table for determining reminder durations.
from django.db import models


class User(models.Model):
  login = models.PositiveIntegerField()
  pin = models.PositiveIntegerField()

  def __unicode__(self):
    return 'User(' + str(self.login) + ',' + str(self.pin) + ')'


class Birthday(models.Model):
  user = models.ForeignKey(User)
  last_letter = models.CharField(max_length=1)
  voice_name_url = models.URLField(max_length=500)
  date = models.DateField('birthday date')
  reminder_delta = models.PositiveIntegerField()

  def is_reminder(self):
    """Returns true when a birthday has a reminder."""
    self.date = self.date.replace(year=timezone.now().year)
    return self.date >= timezone.now().date() - durations[self.reminder_delta]  and \
           self.date <= timezone.now().date()

  def __unicode__(self):
    return 'Birthday:' + self.last_letter + '  date:' + str(self.date) + '  dur:' + str(durations[self.reminder_delta])