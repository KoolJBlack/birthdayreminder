from django.conf.urls import patterns, include, url

urlpatterns = patterns('birthdays.views',
                       
  url(r'^login/$', 'login'),
  url(r'^new/$', 'new_user'),
  url(r'^getlist/$', 'get_birthdays_list'),
  url(r'^getpick/$', 'get_birthdays_pick'),
  url(r'^delete/$', 'delete_birthday'),
  url(r'^add/$', 'add_birthday'),
  url(r'^reminder/$', 'update_reminder'),

)