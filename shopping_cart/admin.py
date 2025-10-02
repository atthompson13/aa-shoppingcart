from django.contrib import admin
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
