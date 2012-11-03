from birthdays.models import Birthday, User
from django.contrib import admin

class BirthdayInline(admin.TabularInline):
  """Adds birthday inlines to the User Admin"""
  model = Birthday
  extra = 1
  readonly_fields = ['id']
  fields = ['id', 'last_letter',
            'voice_name_url',
            'date',
            'reminder_delta']

class UserAdmin(admin.ModelAdmin):
  """Admin interface for Users"""
  fieldsets = [
    ('User Info', {'fields': ['login','pin'] }),
  ]
  inlines = [BirthdayInline]

admin.site.register(User, UserAdmin)

# Just register Brithday. Nothing special done for them
admin.site.register(Birthday)
