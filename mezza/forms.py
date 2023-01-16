from django import forms
from django.forms import ModelForm
from django.db import transaction
from .models import Venue, Event, AccountTags

from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput

class SearchMap(forms.Form):
	location = forms.CharField(max_length=99)	

class DateInput(forms.DateInput):
	input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
        input_type = 'datetime'

class CustomMMCF(forms.ModelMultipleChoiceField):

	# > used for accessing the event tag options
	
    def label_from_instance(self, tag):
        return '%s' %tag.title

class EventForm(ModelForm):

	# > Passed into the create and update Event pages, fields required
    # and the types of input (charfield, decimal field etc)

	class Meta:
		model = Event 

		fields = (
			'name', 
			'event_date', 
			'wage',
			'description',  
			'event_tags')

		widgets = {
			'event_date' : DateInput(),
		}

		name = forms.CharField(required=True)
		description = forms.CharField(widget=forms.Textarea)
		wage = forms.DecimalField(required=True ,max_digits=7, decimal_places=2)
		event_date = forms.DateTimeField(widget=DateInput)
		
		event_tags = CustomMMCF(
			queryset=AccountTags.objects.all(),
		)
