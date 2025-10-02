from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import ItemRequest
from .helpers import parse_eve_items

class CreateRequestForm(forms.Form):
    request_type = forms.ChoiceField(
        choices=ItemRequest.REQUEST_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label=_('Request Type'),
        initial=ItemRequest.REQUEST_TYPE_REQUESTER_HAS_ITEMS,
    )
    
    items_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': _('Paste items from EVE')}),
        label=_('Items (paste from EVE)'),
    )
    
    pickup_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    requester_price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}))
    requester_collateral = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}))
    requester_expiration_days = forms.IntegerField(initial=7, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '14'}))
    max_budget = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    def clean_items_text(self):
        items_text = self.cleaned_data.get('items_text')
        if not items_text:
            raise ValidationError(_('Please paste items from EVE'))
        items_list = parse_eve_items(items_text)
        if not items_list:
            raise ValidationError(_('Could not parse any items'))
        self.parsed_items = items_list
        return items_text

class SubmitContractIDForm(forms.Form):
    contract_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}))

class FulfillerContractForm(forms.Form):
    contract_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}))
    collateral = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}))
    expiration_days = forms.IntegerField(initial=7, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '14'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
