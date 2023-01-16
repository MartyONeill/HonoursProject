from mmap import ACCESS_COPY
from django.contrib import admin
from .models import User, Venue, Talent, AccountTags

admin.site.register(User)

# > Overriding the standard admin pages with a new format more suitable 
# for the business needs.

@admin.register(AccountTags)
class AccountTagsAdmin(admin.ModelAdmin):
	list_display = ('title',)
	ordering = ('title',)
	search_fields = ('title',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'phone')
	ordering = ('name',)
	search_fields = ('name', 'address')

@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = ( 'last_name','first_name', 'instrument')
    ordering = ('last_name',)
