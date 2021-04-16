from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Order

class OrderForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Order
        fields = ['first_name',
        'last_name',
        'start_date',
        'end_date',
        'location',
        'num_of_traveller',
        'phone']
