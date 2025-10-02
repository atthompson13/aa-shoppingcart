from django.shortcuts import render, redirect, get_object_or_404
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
