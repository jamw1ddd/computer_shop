from django import forms
from .models import PhoneSubscription,Order

class PhoneSubscriptionForm(forms.ModelForm):
    class Meta:
        model = PhoneSubscription
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': "Raqamingizni kiriting"})
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'tel']