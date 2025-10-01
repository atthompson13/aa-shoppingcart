# Alliance Auth Shopping Cart

A player-to-player shopping cart and contract marketplace for Alliance Auth that enables item requests and fulfillment through EVE Online contracts tracked via ESI.

## Features

- **Dual Workflow System**
  - Workflow A: Requester has items and creates contract
  - Workflow B: Fulfiller buys items and creates contract  
  
- **ESI Contract Tracking**
  - Automatic contract monitoring via EVE ESI
  - Auto-detection of contract acceptance and completion
  - Real-time status updates

- **Discord Integration**
  - Notifications when requests are claimed
  - Direct messages with contract details
  - Webhook notifications for marketplace activity

- **User Features**
  - Paste items directly from EVE (copy/paste support)
  - Set pickup and delivery locations
  - Browse marketplace of available requests
  - Track your requests and fulfilled orders
  - Leaderboard for top fulfillers

- **Permissions System**
  - basic_access - Can access the app
  - request_items - Can create and submit requests
  - fulfill_requests - Can claim and fulfill orders
  - manage_requests - Admin management
  - Superuser bypass for all permissions

## Installation

### Prerequisites

- Alliance Auth >= 4.0.0
- Python >= 3.8
- Redis (for Celery)

### Step 1: Install Package

```bash
pip install allianceauth-shopping-cart
```

### Step 2: Configure Settings

Add to your `local.py`:

```python
INSTALLED_APPS += [
    'shopping_cart',
]

# Shopping Cart Settings
SHOPPING_CART_APP_NAME = "Shopping Cart"
SHOPPING_CART_DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
```

### Step 3: Run Migrations

```bash
python manage.py migrate shopping_cart
```

### Step 4: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 5: Restart Services

```bash
supervisorctl restart myauth:
```

### Step 6: Configure Permissions

Grant permissions to appropriate groups in Alliance Auth admin.

## Configuration

All settings are optional and have sensible defaults:

```python
# Display
SHOPPING_CART_APP_NAME = "Shopping Cart"

# Features
SHOPPING_CART_ENABLE_MARKETPLACE = True
SHOPPING_CART_ENABLE_LEADERBOARD = True

# Notifications
SHOPPING_CART_DISCORD_WEBHOOK_URL = ""
SHOPPING_CART_NOTIFY_ON_CLAIM = True
SHOPPING_CART_NOTIFY_ON_CONTRACT = True

# Retention (days)
SHOPPING_CART_FULFILLED_RETENTION_DAYS = 90
SHOPPING_CART_PENDING_REMINDER_DAYS = 7

# Pagination
SHOPPING_CART_PAGINATION_SIZE = 25

# Trading Hubs
SHOPPING_CART_DEFAULT_HUBS = ['Jita', 'Amarr', 'Dodixie', 'Rens', 'Hek']
```

## Usage

### For Requesters

1. Navigate to Shopping Cart from the menu
2. Click "Create Request"
3. Choose request type:
   - "I have items" - You'll create the contract
   - "Please buy items" - Fulfiller will buy and create contract
4. Paste items from EVE (Ctrl+C in cargo/inventory)
5. Set pickup and delivery locations
6. Set price/collateral or budget
7. Submit request

### For Fulfillers

1. Navigate to Marketplace from the menu
2. Browse available requests
3. Claim a request
4. Follow workflow based on request type:
   - If requester has items: Wait for contract, then accept it
   - If you're buying items: Buy items, create contract, enter contract ID

### Contract Tracking

The app automatically:
- Monitors contracts via ESI
- Detects when contracts are accepted
- Updates status when contracts complete
- Marks requests as fulfilled

## Development

### Setup Development Environment

```bash
git clone https://github.com/atthompson13/aa-shoppingcart.git
cd aa-shoppingcart
python -m venv venv
source venv/bin/activate
pip install -e .[test]
```

### Run Tests

```bash
make test
```

### Build Package

```bash
make package
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Issues: https://github.com/atthompson13/aa-shoppingcart/issues
- Discord: [Your Discord Server]

## Credits

Developed by atthompson13 for the Alliance Auth community.

## Screenshots

[Coming soon]