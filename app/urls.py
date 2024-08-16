from django.urls import path
from django.conf.urls.static import static

from .views import *
from payment.views import *

urlpatterns = [
  path('', home, name='home'),
  path('about-us', about, name='about'),
  path('our-programs', programs, name='programs'),
  path('events', events, name='events'),
  
  path('gallery', gallery_view, name='gallery'),
  path('gallery/<slug:category_slug>/', gallery_view, name='gallery_by_category'),

  path('videos', videos, name='videos'),
  path('contact-us', contact, name='contact'),
  path('donation', donate, name='donate'),
  path('initiate-payment/', initiate_payment, name='initiate_payment'),
  path('verify-payment/<str:ref>/', verify_payment, name='verify_payment'),

  path('contact/success/', contact_success, name='contact_success'),
  path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
  


  

]