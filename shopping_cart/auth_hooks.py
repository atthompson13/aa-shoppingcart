from django.utils.translation import gettext_lazy as _
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
