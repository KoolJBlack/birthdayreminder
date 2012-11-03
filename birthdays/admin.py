from birthdays.models import Birthday, User
from django.contrib import admin

class BirthdayInline(admin.TabularInline):
  """Adds birthday inlines to the User Admin"""
  model = Birthday
  extra = 1

class UserAdmin(admin.ModelAdmin):
  """Admin interface for Users"""
  fieldsets = [
    ('User Info', {'fields': ['login','pin'] }),
    #('Birthdays', {'fields': [''], 'classes': ['collapse']}),
  ]
  inlines = [BirthdayInline]

admin.site.register(User, UserAdmin)

# Just register Brithday. Nothing special done for them
admin.site.register(Birthday)
