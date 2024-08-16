from django.db import models
import secrets
from .paystack import Paystack


class Payment(models.Model):
  NAIRA = 'NGN'
  DOLLAR = 'USD'

  CURRENCY_CHOICES = (
    (NAIRA, 'NGN'),
    (DOLLAR, 'USD')
  )
  INDIVIDUAL = 'individual'
  MINISTRY = 'ministry'
  ORGANISATION = 'organisation'

  DONATE_AS_CHOICES = (
    (INDIVIDUAL, 'individual'),
    (MINISTRY, 'ministry'),
    (ORGANISATION, 'organisation')
  )

  amount = models.IntegerField(blank=True, null=True)
  ref = models.CharField(max_length=250)
  email = models.EmailField(max_length=250)
  full_name = models.CharField(max_length=250)
  verified = models.BooleanField(default=False)
  currency = models.CharField(max_length=25, choices=CURRENCY_CHOICES)
  donate_as = models.CharField(max_length=25, choices=DONATE_AS_CHOICES, default=INDIVIDUAL)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.full_name} - {self.amount}'

  def save(self, *args, **kwargs):
    while not self.ref:
      ref = secrets.token_urlsafe(50)
      object_with_similar_ref = Payment.objects.filter(ref=ref)
      if not object_with_similar_ref:
        self.ref = ref

    super().save(*args, **kwargs)

  def amount_value(self):
    return int(self.amount) * 100

  def verify_payment(self):
    paystack = Paystack()
    status, result = paystack.verify_payment(self.ref)
    if status:
      if result['amount'] / 100 == self.amount:
        self.verified = True
        self.save()
    if self.verified:
      return True
    else:
      return False
