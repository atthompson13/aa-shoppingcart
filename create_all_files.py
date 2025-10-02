#!/usr/bin/env python3
"""
Alliance Auth Shopping Cart - COMPLETE Project Setup
Creates ALL files needed for the project
Author: atthompson13
Date: 2025-10-01
"""

import os
from pathlib import Path

def create_file(path, content):
    """Create a file with the given content, creating directories as needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✓ {path}")

def main():
    print("=" * 60)
    print("Alliance Auth Shopping Cart - COMPLETE Setup")
    print("Creating ALL project files...")
    print("=" * 60)
    print()

    file_count = 0

    # ============================================================
    # ROOT FILES
    # ============================================================
    print("\n[1/8] Creating root configuration files...")

    create_file("README.md", """# Alliance Auth Shopping Cart

A player-to-player shopping cart and contract marketplace for Alliance Auth.

## Features

* Dual workflow system (requester has items OR fulfiller buys items)
* ESI contract tracking
* Discord notifications
* Marketplace with filtering
* Fulfiller leaderboard
* Admin management tools

## Installation

Install: pip install allianceauth-shopping-cart

Add to INSTALLED_APPS: 'shopping_cart'

Run: python manage.py migrate shopping_cart

## License

MIT License - See LICENSE file
""")
    file_count += 1

    create_file("LICENSE", """MIT License

Copyright (c) 2025 atthompson13

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
    file_count += 1

    create_file(".gitignore", """__pycache__/
*.py[cod]
*.so
build/
dist/
*.egg-info/
.venv/
venv/
*.log
db.sqlite3
.env
.vscode/
.idea/
.DS_Store
Thumbs.db
""")
    file_count += 1

    create_file("pyproject.toml", """[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[project]
name = "allianceauth-shopping-cart"
description = "Player-to-player shopping cart and contract marketplace for Alliance Auth"
readme = "README.md"
license = { file = "LICENSE" }
authors = [{ name = "atthompson13" }]
requires-python = ">=3.8"
dependencies = [
    "allianceauth>=4.0.0",
    "allianceauth-app-utils>=1.13.0",
    "django-eveuniverse>=1.0.0",
    "django-esi>=4.0.0",
]
dynamic = ["version"]

[tool.hatch.version]
path = "shopping_cart/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["shopping_cart"]
""")
    file_count += 1

    create_file("Makefile", """.PHONY: help clean dev test

help:
\t@echo "Available targets:"
\t@echo "  dev    - Install development dependencies"
\t@echo "  clean  - Remove build artifacts"
\t@echo "  test   - Run tests"

clean:
\trm -rf dist build *.egg-info

dev:
\tpip install -e .[test]

test:
\ttox
""")
    file_count += 1

    create_file("tox.ini", """[tox]
isolated_build = true
skipsdist = true
usedevelop = true
envlist = django42

[testenv]
setenv = DJANGO_SETTINGS_MODULE = tests.test_settings
deps =
    allianceauth>=4.0.0
    coverage
install_command = pip install -e ".[test]" -U {opts} {packages}
commands =
    coverage run runtests.py shopping_cart -v 2
""")
    file_count += 1

    create_file("runtests.py", """#!/usr/bin/env python
import sys

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv.insert(1, "test"))
""")
    file_count += 1

    # ============================================================
    # SHOPPING_CART CORE FILES
    # ============================================================
    print("\n[2/8] Creating shopping_cart core files...")

    create_file("shopping_cart/__init__.py", '''"""Alliance Auth Shopping Cart"""
__version__ = "0.1.0"
__title__ = "Alliance Auth Shopping Cart"
default_app_config = "shopping_cart.apps.ShoppingCartConfig"
''')
    file_count += 1

    create_file("shopping_cart/apps.py", '''from django.apps import AppConfig

class ShoppingCartConfig(AppConfig):
    name = 'shopping_cart'
    label = 'shopping_cart'
    verbose_name = 'Shopping Cart'
''')
    file_count += 1

    create_file("shopping_cart/app_settings.py", '''from django.conf import settings

SHOPPING_CART_APP_NAME = getattr(settings, "SHOPPING_CART_APP_NAME", "Shopping Cart")
SHOPPING_CART_ENABLE_MARKETPLACE = getattr(settings, "SHOPPING_CART_ENABLE_MARKETPLACE", True)
SHOPPING_CART_ENABLE_LEADERBOARD = getattr(settings, "SHOPPING_CART_ENABLE_LEADERBOARD", True)
SHOPPING_CART_DISCORD_WEBHOOK_URL = getattr(settings, "SHOPPING_CART_DISCORD_WEBHOOK_URL", "")
SHOPPING_CART_NOTIFY_ON_NEW_REQUEST = getattr(settings, "SHOPPING_CART_NOTIFY_ON_NEW_REQUEST", True)
SHOPPING_CART_NOTIFY_ON_CLAIM = getattr(settings, "SHOPPING_CART_NOTIFY_ON_CLAIM", True)
SHOPPING_CART_FULFILLED_RETENTION_DAYS = getattr(settings, "SHOPPING_CART_FULFILLED_RETENTION_DAYS", 90)
SHOPPING_CART_ABANDONED_CART_DAYS = getattr(settings, "SHOPPING_CART_ABANDONED_CART_DAYS", 30)
SHOPPING_CART_PAGINATION_SIZE = getattr(settings, "SHOPPING_CART_PAGINATION_SIZE", 25)
SHOPPING_CART_DEFAULT_HUBS = getattr(settings, "SHOPPING_CART_DEFAULT_HUBS", ['Jita', 'Amarr', 'Dodixie', 'Rens', 'Hek'])
''')
    file_count += 1

    create_file("shopping_cart/constants.py", '''"""Constants for Shopping Cart"""

TRADE_HUBS = [
    ('Jita', 'Jita IV - Moon 4 - Caldari Navy Assembly Plant'),
    ('Amarr', 'Amarr VIII (Oris) - Emperor Family Academy'),
    ('Dodixie', 'Dodixie IX - Moon 20 - Federation Navy Assembly Plant'),
    ('Rens', 'Rens VI - Moon 8 - Brutor Tribe Treasury'),
    ('Hek', 'Hek VIII - Moon 12 - Boundless Creation Factory'),
]

STATUS_ICONS = {
    'pending': 'fa-clock',
    'claimed': 'fa-hand-rock',
    'contract_created': 'fa-file-contract',
    'contract_accepted': 'fa-handshake',
    'completed': 'fa-check-double',
    'cancelled': 'fa-times',
    'expired': 'fa-hourglass-end',
}

STATUS_COLORS = {
    'pending': 'warning',
    'claimed': 'info',
    'contract_created': 'primary',
    'contract_accepted': 'success',
    'completed': 'success',
    'cancelled': 'danger',
    'expired': 'default',
}
''')
    file_count += 1

    create_file("shopping_cart/decorators.py", '''from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

def permission_required_or_superuser(perm):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser or request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            messages.error(request, _('You do not have permission to access this page.'))
            return redirect('authentication:dashboard')
        return wrapped_view
    return decorator
''')
    file_count += 1

    create_file("shopping_cart/helpers.py", '''import re

def parse_eve_items(text):
    """Parse items from EVE copy format"""
    items = []
    lines = text.strip().split('\\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        match = re.match(r'(.+?)\\s+x([\\d,]+)', line)
        if match:
            name = match.group(1).strip()
            quantity = int(match.group(2).replace(',', ''))
            items.append({"name": name, "quantity": quantity})
            continue
        
        if '\\t' in line:
            parts = line.split('\\t')
            if len(parts) >= 2:
                name = parts[0].strip()
                try:
                    quantity = int(parts[1].replace(',', ''))
                    items.append({"name": name, "quantity": quantity})
                    continue
                except ValueError:
                    pass
        
        parts = line.rsplit(' ', 1)
        if len(parts) == 2:
            name = parts[0].strip()
            try:
                quantity = int(parts[1].replace(',', ''))
                items.append({"name": name, "quantity": quantity})
            except ValueError:
                pass
    
    return items

def format_isk(amount):
    if amount is None:
        return "0 ISK"
    return f"{amount:,} ISK"
''')
    file_count += 1

    create_file("shopping_cart/managers.py", '''from django.db import models

class ItemRequestManager(models.Manager):
    def pending(self):
        return self.filter(status='pending')
    
    def claimed(self):
        return self.filter(status='claimed')
    
    def completed(self):
        return self.filter(status='completed')
    
    def claimable(self):
        return self.filter(status='pending', fulfiller__isnull=True)
    
    def claimable_for_user(self, user):
        return self.claimable().exclude(user=user)
    
    def user_claims(self, user):
        return self.filter(fulfiller=user, status__in=['claimed', 'contract_created', 'contract_accepted'])
    
    def active(self):
        return self.exclude(status__in=['completed', 'cancelled', 'expired'])
''')
    file_count += 1

    # ============================================================
    # MODELS
    # ============================================================
    print("\n[3/8] Creating models.py...")

    create_file("shopping_cart/models.py", '''from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from allianceauth.eveonline.models import EveCharacter
from .managers import ItemRequestManager

class General(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('basic_access', 'Can access this app'),
            ('request_items', 'Can request items'),
            ('fulfill_requests', 'Can claim and fulfill item requests'),
            ('manage_requests', 'Can manage all item requests'),
        )

class ItemRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CLAIMED = 'claimed'
    STATUS_CONTRACT_CREATED = 'contract_created'
    STATUS_CONTRACT_ACCEPTED = 'contract_accepted'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_CLAIMED, _('Claimed')),
        (STATUS_CONTRACT_CREATED, _('Contract Created')),
        (STATUS_CONTRACT_ACCEPTED, _('Contract Accepted')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_EXPIRED, _('Expired')),
    ]
    
    REQUEST_TYPE_REQUESTER_HAS_ITEMS = 'requester_has_items'
    REQUEST_TYPE_FULFILLER_BUYS = 'fulfiller_buys'
    
    REQUEST_TYPE_CHOICES = [
        (REQUEST_TYPE_REQUESTER_HAS_ITEMS, _('I have the items')),
        (REQUEST_TYPE_FULFILLER_BUYS, _('Please buy items for me')),
    ]
    
    CONTRACT_ISSUER_REQUESTER = 'requester'
    CONTRACT_ISSUER_FULFILLER = 'fulfiller'
    
    CONTRACT_ISSUER_CHOICES = [
        (CONTRACT_ISSUER_REQUESTER, _('Requester Created Contract')),
        (CONTRACT_ISSUER_FULFILLER, _('Fulfiller Created Contract')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart_requests')
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE, related_name='shopping_cart_requests')
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPE_CHOICES, default=REQUEST_TYPE_REQUESTER_HAS_ITEMS)
    items_list = models.JSONField()
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    requester_price = models.BigIntegerField(null=True, blank=True)
    requester_collateral = models.BigIntegerField(default=0)
    requester_expiration_days = models.IntegerField(default=7)
    max_budget = models.BigIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    fulfiller = models.ForeignKey(User, null=True, blank=True, related_name='shopping_cart_fulfilled_requests', on_delete=models.SET_NULL)
    fulfiller_character = models.ForeignKey(EveCharacter, null=True, blank=True, related_name='shopping_cart_fulfilled_requests', on_delete=models.SET_NULL)
    claimed_at = models.DateTimeField(null=True, blank=True)
    fulfiller_price = models.BigIntegerField(null=True, blank=True)
    fulfiller_collateral = models.BigIntegerField(null=True, blank=True)
    fulfiller_expiration_days = models.IntegerField(null=True, blank=True)
    fulfiller_notes = models.TextField(blank=True)
    contract_id = models.BigIntegerField(null=True, blank=True, unique=True)
    contract_issuer = models.CharField(max_length=20, choices=CONTRACT_ISSUER_CHOICES, null=True, blank=True)
    contract_created_at = models.DateTimeField(null=True, blank=True)
    contract_accepted_at = models.DateTimeField(null=True, blank=True)
    contract_completed_at = models.DateTimeField(null=True, blank=True)
    esi_monitor_character = models.ForeignKey(EveCharacter, null=True, blank=True, related_name='shopping_cart_monitored_contracts', on_delete=models.SET_NULL)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ItemRequestManager()
    
    class Meta:
        default_permissions = ()
        ordering = ['-created_at']
    
    def __str__(self):
        items_summary = ', '.join([f"{item['name']} x{item['quantity']}" for item in self.items_list[:3]])
        if len(self.items_list) > 3:
            items_summary += '...'
        return f"#{self.id} - {items_summary}"
    
    @property
    def is_claimable(self):
        return self.status == self.STATUS_PENDING and not self.fulfiller
    
    @property
    def total_items_count(self):
        return len(self.items_list)
    
    @property
    def total_quantity(self):
        return sum(item.get('quantity', 0) for item in self.items_list)
    
    @property
    def status_badge_class(self):
        from .constants import STATUS_COLORS
        return STATUS_COLORS.get(self.status, 'default')
    
    @property
    def status_icon(self):
        from .constants import STATUS_ICONS
        return STATUS_ICONS.get(self.status, 'fa-question')
    
    def can_be_claimed_by(self, user):
        if not self.is_claimable:
            return False
        if user.is_superuser:
            return True
        if not user.has_perm('shopping_cart.fulfill_requests'):
            return False
        if self.user == user:
            return False
        return True
    
    def claim(self, user, character):
        if not self.can_be_claimed_by(user):
            raise ValueError("This request cannot be claimed by this user")
        self.fulfiller = user
        self.fulfiller_character = character
        self.claimed_at = timezone.now()
        self.status = self.STATUS_CLAIMED
        if self.request_type == self.REQUEST_TYPE_REQUESTER_HAS_ITEMS:
            self.esi_monitor_character = self.character
        self.save()
    
    def set_contract_created(self, contract_id, issuer):
        self.contract_id = contract_id
        self.contract_issuer = issuer
        self.contract_created_at = timezone.now()
        self.status = self.STATUS_CONTRACT_CREATED
        self.save()

class FulfillmentTracking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart_fulfillment_stats')
    total_fulfilled = models.IntegerField(default=0)
    total_volume = models.BigIntegerField(default=0)
    last_fulfilled = models.DateTimeField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_ratings = models.IntegerField(default=0)
    
    class Meta:
        default_permissions = ()
    
    def __str__(self):
        return f"{self.user.username} - {self.total_fulfilled} fulfilled"
''')
    file_count += 1

    # ============================================================
    # ADMIN
    # ============================================================
    print("\n[4/8] Creating admin.py...")

    create_file("shopping_cart/admin.py", '''from django.contrib import admin
from django.utils.html import format_html
from .models import ItemRequest, FulfillmentTracking

@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'request_type', 'created_at')
    list_filter = ('status', 'request_type', 'created_at')
    search_fields = ('user__username', 'character__character_name', 'contract_id')

@admin.register(FulfillmentTracking)
class FulfillmentTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_fulfilled', 'total_volume', 'rating')
    search_fields = ('user__username',)
''')
    file_count += 1

    # ============================================================
    # FORMS
    # ============================================================
    print("\n[5/8] Creating forms.py...")

    create_file("shopping_cart/forms.py", '''from django import forms
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
''')
    file_count += 1

    # ============================================================
    # URLS
    # ============================================================
    print("\n[6/8] Creating urls.py and auth_hooks.py...")

    create_file("shopping_cart/urls.py", '''from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_request, name='create_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('my-claimed/', views.my_claimed_orders, name='my_claimed_orders'),
    path('claim/<int:request_id>/', views.claim_request, name='claim_request'),
    path('cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
''')
    file_count += 1

    create_file("shopping_cart/auth_hooks.py", '''from django.utils.translation import gettext_lazy as _
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from . import urls

class ShoppingCartMenuItem(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(self, _('Shopping Cart'), 'fas fa-shopping-cart', 'shopping_cart:index', navactive=['shopping_cart:'])
    
    def render(self, request):
        if request.user.has_perm('shopping_cart.basic_access') or request.user.is_superuser:
            return MenuItemHook.render(self, request)
        return ''

@hooks.register('menu_item_hook')
def register_menu():
    return ShoppingCartMenuItem()

@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'shopping_cart', r'^shopping-cart/')
''')
    file_count += 1

    # ============================================================
    # VIEWS (Simple stubs for now)
    # ============================================================
    print("\n[7/8] Creating views.py and tasks.py...")

    create_file("shopping_cart/views.py", '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from .decorators import permission_required_or_superuser
from .models import ItemRequest, FulfillmentTracking
from .forms import CreateRequestForm

@permission_required_or_superuser('shopping_cart.basic_access')
def index(request):
    context = {
        'total_requests': ItemRequest.objects.filter(user=request.user).count(),
        'active_requests': ItemRequest.objects.filter(user=request.user).active().count(),
        'completed_requests': ItemRequest.objects.filter(user=request.user, status='completed').count(),
    }
    return render(request, 'shopping_cart/index.html', context)

@permission_required_or_superuser('shopping_cart.request_items')
def create_request(request):
    if request.method == 'POST':
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            ItemRequest.objects.create(
                user=request.user,
                character=request.user.profile.main_character,
                request_type=form.cleaned_data['request_type'],
                items_list=form.parsed_items,
                pickup_location=form.cleaned_data['pickup_location'],
                delivery_location=form.cleaned_data['delivery_location'],
                description=form.cleaned_data['description'],
                requester_price=form.cleaned_data.get('requester_price'),
                max_budget=form.cleaned_data.get('max_budget'),
            )
            messages.success(request, _('Request created successfully!'))
            return redirect('shopping_cart:my_requests')
    else:
        form = CreateRequestForm()
    return render(request, 'shopping_cart/create_request.html', {'form': form})

@permission_required_or_superuser('shopping_cart.request_items')
def my_requests(request):
    requests = ItemRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shopping_cart/my_requests.html', {'requests': requests})

@permission_required_or_superuser('shopping_cart.basic_access')
def request_detail(request, request_id):
    item_request = get_object_or_404(ItemRequest, id=request_id)
    return render(request, 'shopping_cart/request_detail.html', {'request': item_request})

@permission_required_or_superuser('shopping_cart.fulfill_requests')
def marketplace(request):
    requests = ItemRequest.objects.claimable_for_user(request.user)
    return render(request, 'shopping_cart/marketplace.html', {'requests': requests})

@permission_required_or_superuser('shopping_cart.fulfill_requests')
def my_claimed_orders(request):
    requests = ItemRequest.objects.user_claims(request.user)
    return render(request, 'shopping_cart/my_claimed_orders.html', {'requests': requests})

@permission_required_or_superuser('shopping_cart.fulfill_requests')
def claim_request(request, request_id):
    item_request = get_object_or_404(ItemRequest, id=request_id)
    item_request.claim(request.user, request.user.profile.main_character)
    messages.success(request, _('Request claimed!'))
    return redirect('shopping_cart:my_claimed_orders')

@permission_required_or_superuser('shopping_cart.basic_access')
def cancel_request(request, request_id):
    item_request = get_object_or_404(ItemRequest, id=request_id, user=request.user)
    item_request.status = ItemRequest.STATUS_CANCELLED
    item_request.save()
    messages.success(request, _('Request cancelled'))
    return redirect('shopping_cart:my_requests')

@permission_required_or_superuser('shopping_cart.basic_access')
def leaderboard(request):
    top_fulfillers = FulfillmentTracking.objects.all().order_by('-total_fulfilled')[:25]
    return render(request, 'shopping_cart/leaderboard.html', {'top_fulfillers': top_fulfillers})

@permission_required_or_superuser('shopping_cart.manage_requests')
def admin_dashboard(request):
    context = {
        'total_requests': ItemRequest.objects.count(),
        'pending_requests': ItemRequest.objects.pending().count(),
        'completed_requests': ItemRequest.objects.completed().count(),
    }
    return render(request, 'shopping_cart/admin_dashboard.html', context)
''')
    file_count += 1

    create_file("shopping_cart/tasks.py", '''import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def notify_new_request(request_id):
    logger.info(f"New request notification: {request_id}")

@shared_task
def monitor_contract_status(request_id):
    logger.info(f"Monitoring contract for request: {request_id}")
''')
    file_count += 1

    # ============================================================
    # MIGRATIONS
    # ============================================================
    print("\n[8/8] Creating migrations and template stubs...")

    create_file("shopping_cart/migrations/__init__.py", "# Migrations directory")
    file_count += 1

    create_file("shopping_cart/migrations/0001_initial.py", '''# Generated migration - placeholder
from django.db import migrations

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('eveonline', '0017_character_alliance_and_corp_update_get_or_create'),
    ]
    operations = [
        # Migration operations will be generated by Django
    ]
''')
    file_count += 1

    # ============================================================
    # TEMPLATE STUBS
    # ============================================================
    templates = [
        "shopping_cart/index.html",
        "shopping_cart/create_request.html",
        "shopping_cart/my_requests.html",
        "shopping_cart/request_detail.html",
        "shopping_cart/marketplace.html",
        "shopping_cart/my_claimed_orders.html",
        "shopping_cart/leaderboard.html",
        "shopping_cart/admin_dashboard.html",
        "shopping_cart/base.html"
    ]

    for template in templates:
        create_file(f"shopping_cart/templates/{template}", f'''<!-- {template} Template Placeholder -->
{{% extends "allianceauth/base.html" %}}
{{% load i18n %}}

{{% block page_title %}}{{% trans "Shopping Cart" %}}{{% endblock %}}

{{% block content %}}
<h1>{template.split('/')[-1].replace('.html', '').replace('_', ' ').title()}</h1>
<p>Template content goes here...</p>
{{% endblock %}}
''')
        file_count += 1

    # ============================================================
    # STATIC FILES STUBS
    # ============================================================
    create_file("shopping_cart/static/shopping_cart/css/shopping_cart.css", '''/* Shopping Cart CSS */
.shopping-cart-container {
    margin: 20px 0;
}

.request-card {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 15px;
}

.status-badge {
    display: inline-block;
    padding: 0.25em 0.6em;
    font-size: 75%;
    font-weight: 700;
    border-radius: 0.25rem;
}

.items-list {
    font-family: monospace;
    font-size: 0.9em;
}
''')
    file_count += 1

    create_file("shopping_cart/static/shopping_cart/js/shopping_cart.js", '''// Shopping Cart JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Shopping Cart JS loaded');
    
    // Add any interactive functionality here
    const requestForms = document.querySelectorAll('.request-form');
    requestForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Add form validation or processing here
        });
    });
});
''')
    file_count += 1

    # ============================================================
    # TESTS STUB
    # ============================================================
    create_file("tests/__init__.py", "# Tests package")
    file_count += 1

    create_file("tests/test_settings.py", '''"""Test settings for Shopping Cart"""
from allianceauth.project_template.project_name.settings.base import *

# Test database
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}

# Disable logging during tests
LOGGING_CONFIG = None

# Use fast password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Test-specific settings
SECRET_KEY = 'test-secret-key'
DEBUG = True

INSTALLED_APPS += [
    'shopping_cart',
]
''')
    file_count += 1

    create_file("tests/test_models.py", '''"""Test Shopping Cart models"""
from django.test import TestCase
from django.contrib.auth.models import User
from shopping_cart.models import ItemRequest

class ItemRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_item_request_creation(self):
        # Add actual tests here
        self.assertTrue(True)  # Placeholder
''')
    file_count += 1

    # ============================================================
    # SUMMARY
    # ============================================================
    print()
    print("=" * 60)
    print(f"✅ COMPLETE! Created {file_count} files")
    print("=" * 60)
    print()
    print("Project structure:")
    print("├── Root config: README.md, LICENSE, .gitignore, pyproject.toml")
    print("├── Build: Makefile, tox.ini, runtests.py")
    print("├── shopping_cart/")
    print("│   ├── Core: __init__.py, apps.py, app_settings.py, constants.py")
    print("│   ├── Models: models.py (ItemRequest, FulfillmentTracking)")
    print("│   ├── Utils: helpers.py, decorators.py, managers.py")
    print("│   ├── Django: admin.py, urls.py, auth_hooks.py")
    print("│   ├── templates/shopping_cart/ (9 HTML files)")
    print("│   └── static/shopping_cart/css/ & js/")
    print("└── tests/")
    print()
    print("Next steps:")
    print("1. Review all created files")
    print("2. Run: git add .")
    print("3. Run: git commit -m 'Initial complete project setup'")
    print("4. Run: git push origin main")
    print()
    print("Note: Templates and static files have placeholders.")
    print("You may want to add full HTML/CSS/JS content later.")
    print()

if __name__ == "__main__":
    main()