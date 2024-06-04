from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarouselItem, AchievementItem
from django.conf import settings
from .forms import NewsletterForm, ContactForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                settings.EMAIL_HOST_USER,  # From email
                [settings.CONTACT_EMAIL, 'cmioutreachministry@gmail.com'],  # To email
            )

            request.session['contact_form_submitted'] = True

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def donate(request):
    return render(request, 'donate.html')



@csrf_exempt
def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Thank you for subscribing!'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'errors': 'Invalid request'}, status=400)

def contact_success(request):
    if not request.session.get('contact_form_submitted'):
        return redirect('/')
    request.session['contact_form_submitted'] = False
    return render(request, 'contact_success.html')