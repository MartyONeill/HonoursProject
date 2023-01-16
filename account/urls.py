from django.urls import path
#from .views import register_talent
from . import views

# > URL patterns used throughout the site in format
# slug, reference to the view, name (for access in HTML template tags)

urlpatterns = [
   path('login', views.login, name='login'),
   path('logout', views.logout, name='logout'),

   path('register', views.register, name='register'),
   path('register_talent', views.register_talent.as_view(), name='register-talent'),
   path('register_venue', views.register_venue.as_view(), name='register-venue'),

   path('venue_profile/<venue_id>', views.venue_profile, name='profile-venue'),
   path('venue_update/<venue_id>', views.venue_update, name='update-venue'),

   path('talent_profile/<talent_id>', views.talent_profile, name='profile-talent'),
   path('talent_update/<talent_id>', views.talent_update, name='update-talent'),
]