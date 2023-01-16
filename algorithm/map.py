import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.distance import distance

from mezza.models import Venue

# Global initialisation of the geocoder object
geolocator = Nominatim(user_agent="map-app", timeout=2)


def generateMap_loc_events(location_str, zoom, threshold, event_dict):

    # > *generate map with location and events*
    # > uses the location string, the zoom of the map, the surrounding 
    # threshold area, and the event dictionary - where each key is the class
    # of the event (standard, recommended)

    # > input threshold in km, library uses meteres > convert
    thrsh = int(threshold) * 1000

    # > recieve coordinates for the location
    location = geolocator.geocode(location_str)
    coord = [location.latitude, location.longitude]

    # > initialise map
    m = folium.Map(location=coord, zoom_start=zoom)

    # > create circle highligting the threshold
    folium.Circle(
        radius=thrsh,
        location=coord, 
        popup=location_str,
        color="crimson",
    ).add_to(m)

    # > populate the map with events from the dictionary 
    for event in event_dict.keys():

        # > recieve event string location data, return coordinates
        address = event.venue.address + ", " + event.venue.postcode
        location = geolocator.geocode(address)
        coord = [location.latitude, location.longitude]

        # > marker features add data
        popup = event.name
        tooltip = event.venue.name

        # > if standard = blue marker, else green
        if event_dict[event] == "standard":

            folium.Marker(
            coord, 
            popup=popup, 
            tooltip=tooltip, 
            icon=folium.Icon(color="blue"),
        ).add_to(m)

        elif event_dict[event] == "recommend":
	
            folium.Marker(
            coord, 
            popup=popup, 
            tooltip=tooltip, 
            icon=folium.Icon(color="green"),
        ).add_to(m)

    # > generate html representaiton of the map and return
    m = m._repr_html_()
    return m

# def generateMap_open_events(event_dict):

#     location = geolocator.geocode("glasgow, scotland")
#     coord = [location.latitude, location.longitude]
#     m = folium.Map(location=coord, zoom_start= 14.5)

#     for event in event_dict.keys():

#         address = event.venue.address + ", " + event.venue.postcode
#         location = geolocator.geocode(address)
#         coord = [location.latitude, location.longitude]

#         popup = event.name
#         tooltip = event.venue.name

#         if event_dict[event] == "standard":

#             folium.Marker(
#             coord, 
#             popup=popup, 
#             tooltip=tooltip, 
#             icon=folium.Icon(color="blue"),
#         ).add_to(m)

#         elif event_dict[event] == "recommend":
	
#             folium.Marker(
#             coord, 
#             popup=popup, 
#             tooltip=tooltip, 
#             icon=folium.Icon(color="green"),
#         ).add_to(m)
    
#     m = m._repr_html_()

#     return m

        


# def location_distance(talent, venue, threshold):

#     tal_location = geolocator.geocode(talent.location)
#     talent_coord = [tal_location.latitude, tal_location.longitude]

#     #ven_location = geolocator.geocode((venue.address + ", " + venue.postcode))
#     venue_coord = [ven_location.latitude, ven_location.longitude]

#     dst = distance(talent_coord, venue_coord)
    
#     return dst

def retrieve_close_venues(set, threshold, location):

    close_venues = []

    # > get search coordinates of search location 
    search_location = geolocator.geocode(location)
    search_coord = [search_location.latitude, search_location.longitude]

    # > for each venue, get the coordinates, and measure distance from search loc
    for venue in set:
        ven_location = geolocator.geocode((venue.address + ", " + venue.postcode))
        venue_coord = [ven_location.latitude, ven_location.longitude]

        dst = distance(search_coord, venue_coord)
        dst = str(dst)
        dst = float(dst[0: dst.index('.')+2])
        
        thrs = float(threshold)

        # > if the venue is within the area, add to close venues
        if(dst<thrs):
            close_venues.append(venue)

    return close_venues

# def generateMap_loc(location_str, zoom, threshold):

#     print(threshold)
#     thrsh = int(threshold) * 1000
    
#     print(thrsh)
#     print(type(thrsh))

#     location = geolocator.geocode(location_str)
#     coord = [location.latitude, location.longitude]

#     m = folium.Map(location=coord, zoom_start=zoom)

# 	#folium.LayerControl().add_to(m)

#     folium.Marker(
#         coord, 
#         popup=location_str, 
#         tooltip=location_str, 
#         icon=folium.Icon(color="blue"),
#     ).add_to(m)
    
#     folium.Circle(
#         radius=thrsh,
#         location=coord, 
#         popup=location_str,
#         color="crimson",
#     ).add_to(m)

#     m = m._repr_html_()

#     return m

def generateMap(zoom):

    # > generates the default map on the home screen
    m = folium.Map()
    m = m._repr_html_()

    return m

def generateMap_loc_venues(location_str, zoom, threshold, venues):
	
    # > * generate map with location and venues*

    # > recievs surrounding area in km, system uses meteres, convert
    thrsh = int(threshold) * 1000

    # > retreieve location info and return coordinates
    location = geolocator.geocode(location_str)
    coord = [location.latitude, location.longitude]
    m = folium.Map(location=coord, zoom_start=zoom)

    # > for all venuesin param, create marker, add to map
    for venue in venues:

        ven_loc = geolocator.geocode(venue.address)
        coord = [ven_loc.latitude, ven_loc.longitude]

        folium.Marker(
            coord, 
            #popup=venue.address, 
            popup= venue.address,
            tooltip=venue.name, 
            icon=folium.Icon(color="blue"),
        ).add_to(m)
    
    # > create surrounding area circle
    folium.Circle(
        radius=thrsh,
        location=coord, 
        popup=location_str,
        color="crimson",
    ).add_to(m)

    # > generate the HMTL representation of  the map and return
    m = m._repr_html_()
    return m
