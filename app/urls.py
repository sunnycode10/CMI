from django.urls import path
from django.conf.urls.static import static

from .views import *


urlpatterns = [
  path('', home, name='home'),
  path('about-us', about, name='about'),
  path('our-programs', programs, name='programs'),
  path('events', events, name='events'),
  path('gallery', gallery, name='gallery'),
  path('videos', videos, name='videos'),
  path('contact-us', contact, name='contact'),
  path('donation', donate, name='donate'),
  


  

]