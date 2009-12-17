from django.contrib import admin
from tempel.models import Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'language', 'created', 'active']

admin.site.register(Entry, EntryAdmin)

