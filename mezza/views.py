# from calendar import c
# from cgi import test

# ------------ Django system imports ------------
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# -------- Developer Made Imports -----------------

from .models import Event, Talent, Venue
from .forms import EventForm

#from algorithm.preprocess import preprocess

from algorithm.match import (#tf_idf, 
                        #normalise, 
                        #toDataFrame, 
                        #normalise, 
                        recommended_events, 
                        create_corpus)

from algorithm.map import (generateMap, 
                        #generateMap_open_events, 
                        #generateMap_loc, 
                        #generateMap_loc_pop,
                        generateMap_loc_venues,
                        #location_distance2,
                        generateMap_loc_events, 
                        retrieve_close_venues)

from algorithm.clustering import cluster


import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.distance import distance
#from pandas.io import read_frame

#all_venues = Venue.objects.all()


def all_venues(request):

    # > displays all venues within a given threshold, 
    # or fetches and uses the talents default location

    default_threshold = 3

    talent_obj = Talent.objects.get(pk=request.user.id)
    all_venues = Venue.objects.all()

    if request.GET.get('search'):

        # > if searching get data, get venues, populate map,

        location = request.GET.get('search')
        threshold = request.GET.get('thresh')

        venues_close = retrieve_close_venues(all_venues, threshold, location)

        m = generateMap_loc_venues(location, 12, threshold, venues_close)

        # > return close venues, map, location and threshold info to autofill 
        return render(request, 'mezza/venues.html', {
            "venues" : venues_close, 
            "map": m, 
            "autofill_loc" : location,
            "autofill_thresh" : threshold})

    venues_close = retrieve_close_venues(all_venues, default_threshold, talent_obj.location )
    m = generateMap_loc_venues(talent_obj.location, 12, default_threshold, venues_close)

    # > return close venues, map, location and threshold info to autofill 
    return render(request, "mezza/venues.html", {
        "venues" : all_venues, 
        "map" : m,
        "autofill_loc" : talent_obj.location,
        "autofill_thresh" : default_threshold})


def talent_accepted(request, talent_id, event_id):

    # > when job is accepted, move event from offers into accepted work
    event = Event.objects.get(pk=event_id)
    talent_obj = Talent.objects.get(pk=talent_id)

    talent_obj.confirmed_events.add(event)
    talent_obj.offers.remove(event)
    talent_obj.save()

    event.talent = talent_obj
    event.offers.remove(talent_obj)
    event.is_open = False
    event.save()

    return render(request, "redirections/talent_accepted.html", {})


def talent_offered(request, talent_id, event_id):

    # > talent changes from applicant to an offer holder
    event = Event.objects.get(pk=event_id)
    talent = Talent.objects.get(pk=talent_id)

    talent.offers.add(event)
    talent.applications.remove(event)
    talent.save()

    event.offers.add(talent)
    event.applicants.remove(talent)
    event.save()

    return render(request, "redirections/talent_offered.html", {})

def application_success(request, event_id):

    # > talent is added as applicant into Event
    event = Event.objects.get(pk=event_id)
    talent = Talent.objects.get(pk=request.user.id)

    event.applicants.add(talent)
    event.save()

    talent.applications.add(event)
    talent.save()

    return render(request, "redirections/application_success.html", {})

def talent_events(request, talent_id):

    # > returns webpage of all of talents event data (applications/accepted/offers)
    talent = Talent.objects.get(pk=request.user.id)

    talent_applications = talent.applications.all()
    talent_offers = talent.offers.all()
    talent_events = talent.confirmed_events.all()

    return render(request, 'mezza/talent_events.html',
                {'talent_applications' : talent_applications, 
                'talent_offers' : talent_offers,
                'talent_events' : talent_events})

def venue_events(request, venue_id):

    # > get all events that the venue is running

    all_events = Event.objects.filter(venue=venue_id)

    # > split them between open jobs (talent applying)
    open_events = []

    for event in all_events:
        if event.is_open:
            open_events.append(event)

    # > and closed jobs -> talent accepted / jobs closed
    closed_events = []

    for event in all_events:
        if not event.is_open:
            closed_events.append(event)

    # > return all Events
    return render(request, 'mezza/venue_events.html', 
                {'closed_events': closed_events,
                'open_events': open_events})

def event_page(request, event_id):

    # > returns standard event page
    event = Event.objects.get(pk=event_id)

    return render(request, 'mezza/event_page.html',
        {'event' : event,})


def create_event(request):

    # > create event page
    submitted = False

    if request.method == "POST":

        form = EventForm(request.POST)
        userid = request.user.id

        # > if form is valid, save the event otherwise disband
        if form.is_valid():
            event = form.save(commit=False)
            event.venue = request.user.venue
            event.is_open = True
            event.save()

            for tag in form.cleaned_data.get('event_tags'):
                event.event_tags.add(tag)

            return HttpResponseRedirect('/create_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    # > return the form and the status of the form
    return render(request, 'mezza/create_event.html', {
        'form':form,  
        'submitted':submitted})

def update_event(request, event_id):

    # > update event, retrieve event and form
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)

    # > if valid, save
    if form.is_valid():
        form.save()
        return redirect('venue-events', request.user.id)

    return render(request, 'mezza/update_event.html',
        {'event' : event,
        'form' : form})



def open_events(request):

    # > storing the Event objects
    open_events_list = []
    recommended_events_list = []
    all_events_dict = {}

    talent_obj = Talent.objects.get(pk=request.user.id)
    all_venues = Venue.objects.all()

    # ----------- Recommending ----------------- #

    # > if a search has been made wihtin the page, then: 
    if request.GET.get('search'):

        # > getting location and surrounding area data from form
        location = request.GET.get('search')
        threshold = request.GET.get('distance')

        # collecting close venues
        venues_close = retrieve_close_venues(all_venues, threshold, location)

        # > initialisng list to store close events
        events_close = []

        # > for each venue, retrieve their events
        for venue in venues_close:
            for event in venue.event_set.all():
                events_close.append(event)

        if len(events_close) == 0:

            # > if there arent any events, populate map, using any venues 
            # within threshold and return

            m = generateMap_loc_venues(location, 12, threshold, venues_close)

            return render(request, 'mezza/open_events.html', 
                    {'autofill_loc' : location,
                    'map' : m})

        elif len(events_close) < 20:

            # > if there are less than 20 Events, use the cosine-similarity recommender

            keys, names, corpus = create_corpus(talent_obj, events_close)

            recommended_events_list = recommended_events(keys, corpus)

        else:

            # > if there are 20 or more events, use cluster analysis

            keys, names, corpus = create_corpus(talent_obj, events_close)

            dataframe = cluster(keys, names, corpus)

            for id in dataframe["ID"].values.tolist():
                recommended_events_list.append(Event.objects.get(pk=id))
        # -------------------------------------------#

        
        for event in events_close:

            # > identify open events, and assign them to the 'standard' key
            if event.is_open and not (event in recommended_events_list):
                open_events_list.append(event)
                all_events_dict[event] = "standard"

        # > give recommended events they key 'recommend'
        for event in recommended_events_list:
            all_events_dict[event] = "recommend"

        # --------Creating Map ------------------------ #

        # > generate map with the events dictionary
        m = generateMap_loc_events(location, 12, threshold, all_events_dict)
        
        return render(request, 'mezza/open_events.html', 
        {'open_events_list':open_events_list,
        'recommended_events_list': recommended_events_list, 
        'autofill_loc' : location,
        'autofill_thresh' : threshold,
        'map' : m})

    else:
        location = talent_obj.location
        threshold = 3

        venues_close = retrieve_close_venues(all_venues, threshold, location)

        events_close = []

        for venue in venues_close:
            for event in venue.event_set.all():
                events_close.append(event)

        print(location, events_close)

        keys, names, corpus = create_corpus(talent_obj, events_close)

        if len(events_close) == 0:
	
            m = generateMap_loc_venues(location, 12, threshold, venues_close)

            return render(request, 'mezza/open_events.html', 
                    {#'open_events_list':open_events_list,
                    #'recommended_events_list': recommended_events_list, 
                    'autofill_loc' : location,
                    'autofill_thresh' : threshold,
                    'map' : m})

        elif len(events_close) < 20:

            recommended_events_list = recommended_events(keys, corpus)

        else:
            # perform kmeans 
            dataframe = cluster(keys, names, corpus)

            #print(dataframe["ID"].values.tolist())

            for id in dataframe["ID"].values.tolist():
                recommended_events_list.append(Event.objects.get(pk=id))
            

        # -------------------------------------------#

        for event in events_close:

            if event.is_open and not (event in recommended_events_list):
                open_events_list.append(event)
                all_events_dict[event] = "standard"

        for event in recommended_events_list:
            all_events_dict[event] = "recommend"

        # --------Creating Map ------------------------ #

        # > generating the map with location and events (loc_events)
        m = generateMap_loc_events(location, 12, threshold, all_events_dict)

        return render(request, 'mezza/open_events.html', 
            {'open_events_list':open_events_list,
            'recommended_events_list': recommended_events_list, 
            'autofill_loc' : location,
            'autofill_thresh' : threshold,
            'map' : m})


def home(request):

    # > home page, generate the map to be displayed
    # > if the search bar is used, render the search and redirect into Venues.html 

    default_threshold = 5
    all_venues = Venue.objects.all()

    if request.GET.get('search'):
	
        location = request.GET.get('search')
        venues_close = retrieve_close_venues(all_venues, default_threshold, location)
        m = generateMap_loc_venues(location, 13, default_threshold, venues_close)

        return render(request, 'mezza/venues.html', 
                    {"venues" : venues_close, 
                    "map": m, 
                    "autofill_loc" : location,})
                    #"autofill_thresh" : 3})

    else:
        # > generate default map
        m = generateMap(20)
        return render(request, 'mezza/index.html', {"map": m})


# def open_events(request):
	
#     # > storing the Event objects
#     open_events_list = []
#     recommended_events_list = []
#     all_events_dict = {}

#     talent_obj = Talent.objects.get(pk=request.user.id)
#     all_venues = Venue.objects.all()

#     # ----------- Recommending ----------------- #

#     # > if a search has been made wihtin the page, then: 
#     if request.GET.get('search'):

#         # > getting location and surrounding area data from form
#         location = request.GET.get('search')
#         threshold = request.GET.get('distance')

#         # collecting close venues
#         venues_close = location_distance2(all_venues, threshold, location)

#         # > initialisng list to store close events
#         events_close = []

#         # > for each venue, retrieve their events
#         for venue in venues_close:
#             for event in venue.event_set.all():
#                 events_close.append(event)

#         if len(events_close) == 0:

#             # > if there arent any events, populate map, using any venues 
#             # within threshold and return

#             m = generateMap_loc_pop(location, 12, threshold, venues_close)

#             return render(request, 'mezza/open_events.html', 
#                     {'autofill_loc' : location,
#                     'map' : m})

#         elif len(events_close) < 20:

#             # > if there are less than 20 Events, use the cosine-similarity recommender

#             keys, names, corpus = create_corpus(talent_obj, events_close)

#             recommended_events_list = recommended_events(keys, corpus)

#         else:

#             # > if there are 20 or more events, use cluster analysis

#             keys, names, corpus = create_corpus(talent_obj, events_close)

#             dataframe = cluster(keys, names, corpus)

#             for id in dataframe["ID"].values.tolist():
#                 recommended_events_list.append(Event.objects.get(pk=id))
#         # -------------------------------------------#

        
#         for event in events_close:

#             # > identify open events, and assign them to the 'standard' key
#             if event.is_open and not (event in recommended_events_list):
#                 open_events_list.append(event)
#                 all_events_dict[event] = "standard"

#         # > give recommended events they key 'recommend'
#         for event in recommended_events_list:
#             all_events_dict[event] = "recommend"

#         # --------Creating Map ------------------------ #

#         # > generate map with the events dictionary
#         m = generateMap_loc_events(location, 12, threshold, all_events_dict)
        
#         return render(request, 'mezza/open_events.html', 
#         {'open_events_list':open_events_list,
#         'recommended_events_list': recommended_events_list, 
#         'autofill_loc' : location,
#         'autofill_thresh' : threshold,
#         'map' : m})

#     else:
#         location = talent_obj.location
#         threshold = 3

#         venues_close = location_distance2(all_venues, threshold, location)

#         events_close = []

#         for venue in venues_close:
#             for event in venue.event_set.all():
#                 events_close.append(event)

#         print(location, events_close)

#         keys, names, corpus = create_corpus(talent_obj, events_close)

#         if len(events_close) == 0:
	
#             m = generateMap_loc_pop(location, 12, threshold, venues_close)

#             return render(request, 'mezza/open_events.html', 
#                     {#'open_events_list':open_events_list,
#                     #'recommended_events_list': recommended_events_list, 
#                     'autofill_loc' : location,
#                     'autofill_thresh' : threshold,
#                     'map' : m})

#         elif len(events_close) < 20:

#             recommended_events_list = recommended_events(keys, corpus)

#         else:
#             # perform kmeans 
#             dataframe = cluster(keys, names, corpus)

#             #print(dataframe["ID"].values.tolist())

#             for id in dataframe["ID"].values.tolist():
#                 recommended_events_list.append(Event.objects.get(pk=id))
            

#         # -------------------------------------------#

#         for event in events_close:

#             if event.is_open and not (event in recommended_events_list):
#                 open_events_list.append(event)
#                 all_events_dict[event] = "standard"

#         for event in recommended_events_list:
#             all_events_dict[event] = "recommend"

#         # --------Creating Map ------------------------ #

#         # > generating the map with location and events (loc_events)
#         m = generateMap_loc_events(location, 12, threshold, all_events_dict)

#         return render(request, 'mezza/open_events.html', 
#             {'open_events_list':open_events_list,
#             'recommended_events_list': recommended_events_list, 
#             'autofill_loc' : location,
#             'autofill_thresh' : threshold,
#             'map' : m})