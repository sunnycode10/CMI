from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CarouselItem, AchievementItem, ImageGalleryCategory, ImageGallery
from django.conf import settings
from .forms import NewsletterForm, ContactForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
# Create your views here.

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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

def gallery_view(request, category_slug=None):
    category = None
    categories = ImageGalleryCategory.objects.all()
    images = ImageGallery.objects.all()

    if category_slug:
        category = get_object_or_404(ImageGalleryCategory, slug=category_slug)
        images = images.filter(category=category)

    paginator = Paginator(images, 9)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'partials/gallery_images.html', {'images': images})

    context = {
        'category': category,
        'categories': categories,
        'images': images,
    }
    return render(request, 'gallery.html', context)

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
            
            # Render the email content from the template
            email_content = render_to_string('contact_email.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            })
            # Create the email
            email_message = EmailMultiAlternatives(
                subject,
                email_content,
                settings.EMAIL_HOST_USER,  # From email
                [settings.CONTACT_EMAIL, settings.ALT_CONTACT_EMAIL],  # To email
            )

            email_message.content_subtype = 'html'  # Main content is text/html

            # Send the email
            email_message.send()

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