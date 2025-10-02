"""Test Shopping Cart models"""
from django.test import TestCase
from django.contrib.auth.models import User
from shopping_cart.models import ItemRequest

class ItemRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_item_request_creation(self):
        # Add actual tests here
        self.assertTrue(True)  # Placeholder
