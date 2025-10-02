from django.urls import path
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
