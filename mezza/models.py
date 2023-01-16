from django.db import models
from multiselectfield import MultiSelectField
from account.models import Venue, Talent, User, AccountTags
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput



class Event(models.Model):
    
	# > Attributes of Event
    name = models.CharField('Event Name', max_length=120)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField('Event Date')
    wage = models.DecimalField('Event Wage',max_digits=7, decimal_places=2)

    # signifies if the Event is taking applications or not
    is_open = models.BooleanField(default=False)
    
    # > The Venue where the Event will be hosted - the event owner
    venue = models.ForeignKey(Venue, blank=False, null=False, on_delete=models.CASCADE)
    
    # > the relationships that are used within the handshake between Talent and Venue through the Event
    applicants = models.ManyToManyField(Talent, related_name='event_applicants', blank=True)# null=True)
    offers = models.ManyToManyField(Talent, related_name='event_offers', blank=True)
    talent = models.ForeignKey(Talent, related_name='event_talent', blank=True, null=True, on_delete=models.SET_NULL)

    # > Many-to-Many field linking to the tags for the event
    event_tags = models.ManyToManyField(AccountTags)

    def __str__(self):
       return self.name