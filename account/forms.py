from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django.forms import ModelForm
from multiselectfield import MultiSelectFormField, MultiSelectField

from .models import AccountTags, User, Venue, Talent

# > Custom model mulitple choice field for use with the account tags functionality
class CustomMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, tag):
        return '%s' %tag.title


class VenueRegisterForm(UserCreationForm):

    # > Fields for registering with as Venue

    name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)
    postcode = forms.CharField(max_length=50)

    # > Account tags using the custom method created, queries the 
    # AccountTags model for all instances of tags
    account_tags = CustomMMCF(
        queryset=AccountTags.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = User

    # > Saving into the database, initially creating the parent
    # object, user, then the Venue object ontop of that
    @transaction.atomic
    def save(self):

        user = super().save(commit=False)
        user.is_venue = True
        user.email = self.cleaned_data.get('email')
        user.save()

        venue = Venue.objects.create(user=user)
        venue.name = self.cleaned_data.get('name')
        venue.description = self.cleaned_data.get('description')
        venue.phone = self.cleaned_data.get('phone')
        venue.address = self.cleaned_data.get('address')
        venue.postcode = self.cleaned_data.get('postcode')
        #venue.tags = self.cleaned_data.get('tags')
        #venue.tag_select = self.cleaned_data.get('tag_select')

        for tag in self.cleaned_data.get('account_tags'):
            venue.account_tags.add(tag)

        venue.save()

        return user

class TalentRegisterForm(UserCreationForm):

    # > Talent Fields in registration
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    instrument = forms.CharField(max_length=50)
    location = forms.CharField(max_length=50)

    account_tags = CustomMMCF(
        queryset=AccountTags.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = User
    
    # > Saving into the database, initially creating the parent
    # object, user, then the Venue object ontop of that
    @transaction.atomic
    def save(self):

        user = super().save(commit=False)
        user.is_talent = True
        user.email = self.cleaned_data.get('email')
        user.save()

        talent = Talent.objects.create(user=user)
        talent.first_name = self.cleaned_data.get('first_name')
        talent.last_name = self.cleaned_data.get('last_name')
        talent.description = self.cleaned_data.get('description')
        talent.location = self.cleaned_data.get('location')
        talent.instrument = self.cleaned_data.get('instrument')

        for tag in self.cleaned_data.get('account_tags'):
            talent.account_tags.add(tag)

        talent.save()

        return user


class VenueUpdateForm(ModelForm):

    # > Passed into the update_venue page, fields required for updating,
    # and the types of input (charfield, decimal field etc)

    class Meta:
        model = Venue 

        fields = (
            'name', 
            'description', 
            'phone',
            #'email',  
            'address', 
            'postcode', 
            'account_tags')

        name = forms.CharField(required=True)
        description = forms.CharField(widget=forms.Textarea)
        phone = forms.DecimalField(required=True ,max_digits=7, decimal_places=2)
        #email = forms.CharField(max_length=50)
        address = forms.CharField(max_length=50)
        postcode = forms.CharField(max_length=50)

        account_tags = CustomMMCF(
            queryset=AccountTags.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

class TalentUpdateForm(ModelForm):

    # > Passed into the update_venue page, fields required for updating,
    # and the types of input (charfield, decimal field etc)
	
    class Meta:
        model = Talent 

        fields = (
            'first_name', 
            'last_name',
            'description', 
            'instrument',  
            'location', 
            'account_tags')

        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        description = forms.CharField(widget=forms.Textarea)
        instrument = forms.CharField(max_length=50)
        location = forms.CharField(max_length=50)

        account_tags = CustomMMCF(
            queryset=AccountTags.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )