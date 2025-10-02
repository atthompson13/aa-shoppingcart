"""Constants for Shopping Cart"""

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
