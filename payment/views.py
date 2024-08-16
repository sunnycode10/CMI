from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Payment
from app.models import Newsletter
from django.urls import reverse
from .paystack import Paystack
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        data = request.POST
        full_name = data.get('full_name')
        email = data.get('email')
        amount = data.get('amount')
        donate_as = data.get('donate_as')
        currency = data.get('currency')

        if not all([full_name, email, amount, donate_as, currency]):
            return JsonResponse({'errors': 'All fields are required.'}, status=400)

        try:
            amount = int(amount)
        except ValueError:
            return JsonResponse({'errors': 'Invalid amount.'}, status=400)

        payment = Payment.objects.create(
            full_name=full_name,
            email=email,
            amount=amount,
            donate_as=donate_as,
            currency=currency,
        )

        paystack = Paystack()
        payment_data = {
            'email': payment.email,
            'amount': payment.amount_value(),
            'currency': payment.currency,
            'reference': payment.ref,
            'callback_url': request.build_absolute_uri(reverse('verify_payment', args=[payment.ref]))
        }

        status, result = paystack.initialize_payment(payment_data)
        if status:
            payment_url = result.get('authorization_url')
            return JsonResponse({'payment_url': payment_url})
        else:
            # Log the response for debugging purposes
            print(result)
            return JsonResponse({'errors': 'Payment initialization failed. Please try again.', 'details': result}, status=400)

    return JsonResponse({'errors': 'Invalid request method.'}, status=405)

def verify_payment(request, ref):
    try:
        payment = Payment.objects.get(ref=ref)
        verified = payment.verify_payment()

        if verified:
            # Add email to newsletter and set has_made_donation to True
            newsletter_entry, created = Newsletter.objects.get_or_create(email=payment.email)
            if created:
                newsletter_entry.has_made_donation = True
                newsletter_entry.save()
            else:
                newsletter_entry.has_made_donation = True
                newsletter_entry.save()

            context = {'payment': payment}
            return render(request, 'thankyou_for_donation.html', context)
        else:
            messages.warning(request, "Oops, your payment could not be verified. Please contact your bank.")
            return redirect('/')
    except Payment.DoesNotExist:
        messages.warning(request, 'Payment not found for this reference number.')
        return JsonResponse({'error_message': 'Payment not found'})