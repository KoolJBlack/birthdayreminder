from datetime import timedelta
import calendar

# This table resolves duration indices to actual time deltas for
# determining if a birthday needs a reminder.

durations = {'none':timedelta(days=0),
             'day':timedelta(days=1),
             'week':timedelta(days=7),
             'month':timedelta(days=30)}
             
months= {'january':1,
         'february':2,
         'march':3,
         'arpril':4,
         'may':5,
         'june':6,
         'july':7,
         'august':8,
         'september':9,
         'october':10,
         'november':11,
         'december':12}

def index_to_month(index):
  return calendar.month_name[index].lower()

def month_to_index(month):
  return months[month]




