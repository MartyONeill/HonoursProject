from django.urls import path
from . import views

# > URL patterns used throughout the site in format
# slug, reference to the view, name (for access in HTML template tags)

urlpatterns = [
    path('', views.home, name='home'),


    path('open_events', views.open_events, name="open-events"),
    path('create_event', views.create_event, name='create-event'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('event_page/<event_id>', views.event_page, name='event-page'),

    path('application_success/<event_id>', views.application_success, name='application-success'),
    path('talent_offered/<talent_id>/<event_id>', views.talent_offered, name='talent-offered' ),
    path('talent_accepted/<talent_id>/<event_id>', views.talent_accepted, name='talent-accepted' ),

    path('venue_events/<venue_id>', views.venue_events, name='venue-events'),
    path('talent_events/<talent_id>', views.talent_events, name='talent-events'),

    path('all_venues/', views.all_venues, name='all-venues'),
]