from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import StaticCharge

class StaticChargeForm(ModelForm):
    class Meta:
        model = StaticCharge
        fields = ['min_amount', 'max_amount', 'description', 'identifier']