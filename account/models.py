from multiprocessing import Event as Eve
from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


class AccountTags(models.Model):

    # > Model used to store all account tags, used in many-to-many
    # relationships with objects.
    # 'Title' represents the name of the tag, 'tags' represents
    # the dataset of related tags  

    title = models.CharField(max_length=255)
    tags= models.TextField(blank=True)

    def __str__(self):
    		return self.title

class User(AbstractUser):

    # > parent user class, identifying type of user and email address
    # of child users

    is_venue = models.BooleanField(default=False)
    is_talent = models.BooleanField(default=False)

    email = models.CharField(max_length = 100)

class Venue(models.Model):

    # > Attributes of Venues, linking to parent userclass to access PK, 
    # linking to account_tags to access backend keywords
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Venue Name', max_length = 120)
    description = models.TextField(blank=True)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    address = models.CharField(max_length=300, blank=True)
    postcode = models.CharField('Post code', max_length=10, blank=True) 

    account_tags = models.ManyToManyField(AccountTags)

    def __str__(self):
    		return self.name


class Talent(models.Model):

    # > Attributes of Talent, linking to parent userclass to access PK, 
    # linking to account_tags to access backend keywords
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.CharField(blank=True, max_length=999)
    instrument = models.CharField(max_length=50,)
    location = models.CharField(max_length=100, blank=True)

    account_tags = models.ManyToManyField(AccountTags)

    # > Event references for use in the Talent-Venue handshake functionality
    applications = models.ManyToManyField("mezza.Event", related_name='talent_applications', blank=True)
    offers = models.ManyToManyField("mezza.Event", related_name='talent_offers', blank=True)
    confirmed_events = models.ManyToManyField("mezza.Event", related_name='talent_confirmed', blank=True)

    def __str__(self):
    		return self.first_name + self.last_name

