from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarouselItem, AchievementItem
from django.conf import settings

# Create your views here.



def home(request):
    carousel_items = CarouselItem.objects.all()
    achievement_item = AchievementItem.objects.all()
    context = {
        'carousel_items': carousel_items,
        'achievement_item': achievement_item
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def programs(request):
    return render(request, 'causes.html')

def events(request):
    return render(request, 'events.html')

def gallery(request):
    return render(request, 'gallery.html')

def videos(request):
  context = {
      'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
      'youtube_api_key': settings.YOUTUBE_API_KEY,
      'youtube_channel_id': settings.YOUTUBE_CHANNEL_ID,

  }
  return render(request, 'videos.html', context)

def contact(request):
    return render(request, 'contact.html')

def donate(request):
    return render(request, 'donate.html')