# ------------ Django system imports ------------

from django.shortcuts import render, redirect

from django.contrib.auth import (authenticate, 
                                login as auth_login, 
                                logout as auth_logout)

from django.contrib import messages

from django.views.generic import CreateView

# -------- Developer Made Imports -----------------

from .models import User, Talent, Venue

from mezza.models import Event

from .forms import (TalentRegisterForm, 
                    VenueRegisterForm, 
                    VenueUpdateForm, 
                    TalentUpdateForm )

# ------------- Other Imports ---------------------

import pandas as pd

import folium
from folium.plugins import MarkerCluster

from geopy.geocoders import Nominatim

def talent_profile(request, talent_id):
    
    # > accepts talent ID, fetches object, populates profile, 
    # returns profile page 

    talent = Talent.objects.get(pk=talent_id)
    upcoming_events = talent.confirmed_events.all()
    t_id = talent_id

    return render(request, 'talent_profile.html', 
        {'talent':talent, 
        't_id':t_id, 
        'upcoming_events':upcoming_events})

def talent_update(request, talent_id):
	
    # > accepts talent ID, fetches objects, populates form, returns form

    talent = Talent.objects.get(pk=talent_id)
    form = TalentUpdateForm(request.POST or None, instance=talent)

    # > update profile, only if valid input
    if form.is_valid():
        form.save()
        return redirect('profile-talent', request.user.id)

    return render(request, 'talent_update.html',
        {'talent' : talent,
        'form' : form})


def venue_profile(request, venue_id):

    # > accepts venue ID, fetches object, populates profile, 
    # > collects all Venues Events, returns list, create template

    venue = Venue.objects.get(pk=venue_id)
    events = Event.objects.filter(venue=venue_id)
    

    # ------------ Folium --------------- #

    # > initialise geocoder, used for retrieveing coordinates
    geolocator = Nominatim(user_agent="map-app", timeout=2)

    # > create address = input param for geocoder, return coord
    address = venue.address + ", " + venue.postcode
    location = geolocator.geocode(address)
    coord = [location.latitude, location.longitude]

    # > initialise map with coordinates, add venue as marker
    m = folium.Map(location=coord, zoom_start= 16)
    popup = venue.address
    tooltip = venue.name
    folium.Marker( coord, popup=popup, color="blue", tooltip=tooltip).add_to(m)

    # > return HTML representation of populated map
    m=m._repr_html_()

    # ---------------------------------- #

    # > return events, venue and map to the template
    return render(request, 'venue_profile.html', 
                {'venue':venue, 
                'map':m, 
                'events':events})


def venue_update(request, venue_id):
	
    # > accepts venue ID, fetches objects, populates form, returns form

    venue = Venue.objects.get(pk=venue_id)
    form = VenueUpdateForm(request.POST or None, instance=venue)

    # > update venue details if input is correct
    if form.is_valid():
        form.save()
        return redirect('profile-venue', request.user.id)

    return render(request, 'venue_update.html',
        {'venue' : venue,
        'form' : form})


def logout(request):

    auth_logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')


def login(request):

    # > recieve username, password,

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # > authenticate
        user = authenticate(request, username=username, password=password)

        # > login or return error
        if user is not None:
            auth_login(request, user)

            print(request.user.is_authenticated) 

            messages.success(request, ("You have been logged in, welcome!"))

            return redirect('home')

        else:
            messages.success(request, ("There was an error logging in, try again."))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {})

class register_talent(CreateView):

    # > assign super-class object, talentform and template
    model = User
    form_class = TalentRegisterForm
    template_name = 'talent_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'talent'
        return super().get_context_data(**kwargs)

    # > if form is valid, create the talent profile
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('home')

class register_venue(CreateView):
   
    # > assign super-class object, talentform and template
    model = User
    form_class = VenueRegisterForm
    template_name = 'venue_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'venue'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        
        # > if form is valid, create the talent profile
        user = form.save()
        auth_login(self.request, user)
        return redirect('home')

