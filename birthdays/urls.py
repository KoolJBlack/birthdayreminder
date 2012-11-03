from django.conf.urls import patterns, include, url

urlpatterns = patterns('birthdays.views',
                       
  url(r'^login/$', 'login'),
  url(r'^new/$', 'new_user'),
  url(r'^add/$', 'add_birthday'),
  url(r'^delete/$', 'delete_birthday'),
  url(r'^list/$', 'get_birthdays_list'),
  url(r'^pick/$', 'get_birthdays_pick'),
  url(r'^update/$', 'update_reminder'),

)