from django.db import models
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
