from django.conf import settings
import requests

class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co/'

    def initialize_payment(self, payment_data):
        path = 'transaction/initialize'
        headers = {
            'Authorization': f'Bearer {self.PAYSTACK_SK}',
            'Content-Type': 'application/json'
        }

        url = self.base_url + path
        response = requests.post(url, json=payment_data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        
        response_data = response.json()
        return response_data['status'], response_data['message']

    def verify_payment(self, ref):
        path = f'transaction/verify/{ref}'
        headers = {
            'Authorization': f'Bearer {self.PAYSTACK_SK}',
            'Content-Type': 'application/json'
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        
        response_data = response.json()
        return response_data['status'], response_data['message']