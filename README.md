# Alliance Auth Shopping Cart

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.0+](https://img.shields.io/badge/django-4.0+-green.svg)](https://www.djangoproject.com/)
[![Alliance Auth](https://img.shields.io/badge/allianceauth-4.0+-purple.svg)](https://gitlab.com/allianceauth/allianceauth)

> A comprehensive player-to-player shopping cart and contract marketplace system for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth).

Enable your EVE Online alliance members to create item requests and have them fulfilled by other players, with automatic contract tracking via ESI integration.

**Author:** atthompson13  
**Last Updated:** 2025-10-02 04:00:32 UTC

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Permissions](#permissions)
- [ESI Setup](#esi-setup)
- [Discord Integration](#discord-integration)
- [Celery Tasks](#celery-tasks)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Support](#support)
- [License](#license)

---

## 🎯 Overview

Shopping Cart enables two distinct workflows for item requests:

### Workflow A: Requester Has Items
1. Player has items and needs them delivered
2. Creates request with pickup/delivery locations and reward
3. Fulfiller claims the request
4. Requester creates courier contract to fulfiller
5. System tracks contract via ESI and auto-completes

### Workflow B: Fulfiller Buys Items
1. Player needs items purchased and delivered
2. Creates request with shopping list and maximum budget
3. Fulfiller buys items from market
4. Fulfiller creates contract to requester
5. System tracks acceptance and completion

---

## ✨ Features

### Core Functionality
- 🛒 **Dual Workflow System** - Support for both courier and shopping requests
- 📝 **Easy Request Creation** - Copy/paste items directly from EVE Online
- 🏪 **Marketplace** - Browse and claim available requests
- 👤 **Request Management** - Track your own requests and fulfillments
- 📊 **Admin Dashboard** - Comprehensive statistics and management tools
- 🏆 **Leaderboard** - Recognizes top fulfillers with statistics

### Automation & Integration
- 🤖 **ESI Contract Tracking** - Automatic status updates via ESI API
- ✅ **Auto-Completion** - Requests complete automatically when contracts finish
- 🔔 **Discord Notifications** - Real-time updates via webhooks
- ⚙️ **Background Tasks** - Celery-powered automatic monitoring
- 🔄 **Status Monitoring** - Contracts checked every 10 minutes

### User Experience
- 🎨 **Responsive Design** - Mobile-friendly Bootstrap interface
- 🔐 **Permission System** - Granular access control
- 📱 **Interactive UI** - Real-time form validation and updates
- 🌍 **Location Support** - Pre-populated trade hub locations
- 💰 **ISK Formatting** - Clear financial displays

---

## 📦 Requirements

| Requirement | Minimum Version |
|-------------|----------------|
| Alliance Auth | 4.0.0 |
| Python | 3.8 |
| Django | 4.0 |
| PostgreSQL or MySQL | Latest stable |

**Python Dependencies:**
- `allianceauth>=4.0.0,<5.0.0`
- `allianceauth-app-utils>=1.18.0`
- `django-eveuniverse>=1.0.0`
- `django-esi>=4.0.0`

---

## 🚀 Installation

### Step 1: Install Package

**From GitHub:**
```bash
pip install git+https://github.com/atthompson13/aa-shoppingcart.git
```

**From PyPI (after publishing):**
```bash
pip install allianceauth-shopping-cart
```

**For Development:**
```bash
git clone https://github.com/atthompson13/aa-shoppingcart.git
cd aa-shoppingcart
pip install -e .
```

### Step 2: Configure Django Settings

Edit your Alliance Auth settings file (typically `myauth/settings/local.py`):

```python
# Add to INSTALLED_APPS
INSTALLED_APPS += [
    'shopping_cart',
]
```

# add to requirements.txt

allianceauth-shopping-cart==0.1.0

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 5: Configure Celery Tasks (Required)

Add the following to your `myauth/settings/local.py`:

```python
from celery.schedules import crontab

# Shopping Cart - Monitor active contracts every 10 minutes
CELERYBEAT_SCHEDULE['shopping_cart_monitor_active_contracts'] = {
    'task': 'shopping_cart.tasks.monitor_all_active_contracts',
    'schedule': crontab(minute='*/10'),
}

# Shopping Cart - Cleanup old requests daily at 3 AM UTC
CELERYBEAT_SCHEDULE['shopping_cart_cleanup_old_requests'] = {
    'task': 'shopping_cart.tasks.cleanup_old_requests',
    'schedule': crontab(minute=0, hour='3'),
}

# Shopping Cart - Expire abandoned requests daily at 4 AM UTC
CELERYBEAT_SCHEDULE['shopping_cart_expire_abandoned_requests'] = {
    'task': 'shopping_cart.tasks.expire_abandoned_requests',
    'schedule': crontab(minute=0, hour='4'),
}
```

**Customization Options:**

- **Change monitoring frequency:**
  ```python
  # Every 5 minutes (more frequent)
  'schedule': crontab(minute='*/5'),
  
  # Every 30 minutes (less frequent)
  'schedule': crontab(minute='*/30'),
  ```

- **Change cleanup time:**
  ```python
  # Run at midnight UTC
  'schedule': crontab(minute=0, hour='0'),
  ```

### Step 6: Restart Services

**Using Supervisor:**
```bash
supervisorctl restart myauth:
supervisorctl restart myauth-beat:
supervisorctl restart myauth-worker:
```

**Using Systemd:**
```bash
systemctl restart allianceauth
systemctl restart allianceauth-beat
systemctl restart allianceauth-worker
```

**Using Docker:**
```bash
docker-compose restart allianceauth
docker-compose restart allianceauth-beat
docker-compose restart allianceauth-worker
```

### Step 7: Verify Installation

1. Log in to Alliance Auth
2. Check if "Shopping Cart" appears in the navigation menu
3. Click on it to access the app
4. Try creating a test request

**Verify Celery Tasks:**
```bash
# Check Celery beat logs
tail -f /var/log/supervisor/myauth-beat.log

# You should see:
# [INFO] Scheduler: Sending due task shopping_cart_monitor_active_contracts
```

---

## ⚙️ Configuration

All settings are **optional** and have sensible defaults. Add these to your `local.py` to customize:

### Basic Settings

```python
# App Display Name
SHOPPING_CART_APP_NAME = "Shopping Cart"

# Feature Toggles
SHOPPING_CART_ENABLE_MARKETPLACE = True
SHOPPING_CART_ENABLE_LEADERBOARD = True
```

### Discord Notifications

```python
# Discord Webhook URL (optional)
SHOPPING_CART_DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"

# Notification Events
SHOPPING_CART_NOTIFY_ON_NEW_REQUEST = True
SHOPPING_CART_NOTIFY_ON_CLAIM = True
SHOPPING_CART_NOTIFY_ON_COMPLETION = True
```

### Data Retention

```python
# How long to keep completed requests (days)
SHOPPING_CART_FULFILLED_RETENTION_DAYS = 90

# When to mark unclaimed requests as abandoned (days)
SHOPPING_CART_ABANDONED_CART_DAYS = 30
```

### UI Customization

```python
# Items per page in lists
SHOPPING_CART_PAGINATION_SIZE = 25

# Default trade hub locations for quick selection
SHOPPING_CART_DEFAULT_HUBS = [
    'Jita IV - Moon 4 - Caldari Navy Assembly Plant',
    'Amarr VIII (Oris) - Emperor Family Academy',
    'Dodixie IX - Moon 20 - Federation Navy Assembly Plant',
    'Rens VI - Moon 8 - Brutor Tribe Treasury',
    'Hek VIII - Moon 12 - Boundless Creation Factory',
]
```

### Advanced Settings

```python
# ESI Monitoring
SHOPPING_CART_CONTRACT_CHECK_INTERVAL = 600  # seconds (10 minutes)

# Security
SHOPPING_CART_REQUIRE_MAIN_CHARACTER = True
SHOPPING_CART_ALLOW_CROSS_ALLIANCE = False
```

---

## 📖 Usage Guide

### Creating a Request

#### For Requesters:

1. **Navigate to Shopping Cart**
   - Click "Shopping Cart" in the main navigation menu
   - Click the "Create New Request" button

2. **Choose Request Type**
   - **"I have the items"** - You own the items and need them delivered (Workflow A)
   - **"Please buy items for me"** - You need someone to purchase items (Workflow B)

3. **Add Items**
   - Open EVE Online
   - Select items in your inventory (or create a list)
   - Press `Ctrl+C` to copy
   - Paste into the "Items" field
   - Supported formats:
     ```
     Tritanium x1,000
     Tritanium	1000
     1000 Tritanium
     ```

4. **Set Locations**
   - Enter pickup location (where items are or should be bought)
   - Enter delivery location (final destination)
   - Can use trade hub shortcuts

5. **Set Financial Terms**
   - **Workflow A:** Enter reward ISK and optional collateral
   - **Workflow B:** Enter maximum budget you're willing to pay

6. **Add Notes (Optional)**
   - Special instructions
   - Preferred delivery times
   - Contact information

7. **Submit Request**
   - Review all details
   - Click "Create Request"
   - Request appears in marketplace immediately

### Fulfilling a Request

#### For Fulfillers:

1. **Browse Marketplace**
   - Navigate to Shopping Cart → Marketplace
   - View all available (unclaimed) requests
   - Filter by type, location, or reward

2. **Review Request Details**
   - Click on a request to view full details
   - Check items list, locations, and terms
   - Verify you can fulfill the requirements

3. **Claim Request**
   - Click "Claim This Request" button
   - Confirm the claim
   - Request moves to your "My Claimed Orders" list

4. **Coordinate with Requester**
   - Use in-game mail or Discord
   - Arrange pickup (Workflow A) or confirm shopping list (Workflow B)

5. **Execute the Request**

   **Workflow A (Requester Has Items):**
   - Coordinate pickup location and time
   - Wait for requester to create courier contract
   - Accept contract in-game
   - Deliver items to destination
   - System auto-completes when contract finishes

   **Workflow B (You Buy Items):**
   - Purchase items from market
   - Transport to delivery location
   - Create item exchange contract to requester
   - Submit contract ID on request page
   - System tracks acceptance and completion

6. **Earn Recognition**
   - Completed requests add to your statistics
   - Climb the fulfiller leaderboard
   - Build reputation in your alliance

### Managing Your Requests

#### View Your Requests
- **My Requests** - See all requests you've created
- **My Claimed Orders** - See requests you're fulfilling

#### Request Status Flow
```
pending → claimed → contract_created → contract_accepted → completed
                                                          ↘ expired
                                      ↘ cancelled
```

#### Actions Available
- **Cancel** - Cancel pending requests (before claimed)
- **View Details** - See full information and timeline
- **Track Contract** - Monitor ESI-tracked contracts
- **Update Notes** - Add information for fulfiller

---

## 🔐 Permissions

Shopping Cart uses a four-tier permission system:

| Permission | Codename | Description | Recommended For |
|------------|----------|-------------|----------------|
| **Basic Access** | `basic_access` | View app and browse marketplace | All members |
| **Request Items** | `request_items` | Create and manage item requests | Members who need items |
| **Fulfill Requests** | `fulfill_requests` | Claim and fulfill orders | Trusted haulers/traders |
| **Manage Requests** | `manage_requests` | Full admin access to all requests | Leadership/Admins |

### Assigning Permissions

#### Via Django Admin:

1. Navigate to **Django Admin** (usually `/admin/`)
2. Go to **Authentication and Authorization** → **Groups**
3. Select or create a group (e.g., "Members", "Logistics")
4. Find permissions under `shopping_cart | general`
5. Add desired permissions to the group
6. Assign users to the group

#### Via Alliance Auth States:

1. Navigate to **Django Admin** → **Authentication** → **States**
2. Edit a state (e.g., "Member" state)
3. Add Shopping Cart permissions to the state
4. All users in that state automatically get permissions

### Permission Inheritance

- **Superusers** automatically have all permissions
- Permissions are cumulative (higher permissions include lower ones)
- Users without `basic_access` cannot see the app in navigation

---

## 🔑 ESI Setup

For automatic contract tracking, users must authorize ESI tokens.

### Required Scope

- `esi-contracts.read_character_contracts.v1`

This allows the app to:
- Read contract information
- Monitor contract status
- Detect acceptance and completion
- Auto-update request status

### Adding ESI Token (For Users)

1. **Navigate to ESI Token Management**
   - Alliance Auth Dashboard
   - Click **Services** → **Add ESI Token**

2. **Select Character**
   - Choose the character you'll use for contracts
   - This is usually your main trading/hauling character

3. **Authorize Scopes**
   - EVE SSO login page appears
   - Check that `esi-contracts.read_character_contracts.v1` is listed
   - Click **Authorize**

4. **Verify Token**
   - Token appears in your token list
   - Status should show "Valid"
   - Expiration date displayed

### Token Usage

- **Requesters:** Need token if creating contracts (Workflow A)
- **Fulfillers:** Need token if creating contracts (Workflow B)
- **Monitoring:** System uses tokens to track contract status
- **Privacy:** Only contract info is read, no other data accessed

### Troubleshooting ESI

**Token Not Working:**
- Verify scope is correct
- Check token is not expired
- Refresh token in Alliance Auth
- Re-authorize if needed

**Contract Not Tracked:**
- Ensure ESI monitoring character is set
- Verify contract is created by correct character
- Check Celery workers are running
- Wait for next monitoring cycle (max 10 minutes)

---

## 🔔 Discord Integration

Enable real-time notifications to keep your alliance informed.

### Setup Discord Webhook

#### 1. Create Webhook in Discord

1. Open Discord and navigate to your server
2. Go to **Server Settings** → **Integrations**
3. Click **Webhooks** → **New Webhook**
4. Configure webhook:
   - **Name:** "Shopping Cart Bot"
   - **Channel:** Choose notification channel (e.g., #logistics)
   - **Avatar:** Optional custom icon
5. Click **Copy Webhook URL**

#### 2. Configure in Alliance Auth

Add to your `local.py`:

```python
SHOPPING_CART_DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/123456789/abcdefghijklmnop"
```

#### 3. Customize Notifications

```python
# Enable/disable specific notification types
SHOPPING_CART_NOTIFY_ON_NEW_REQUEST = True   # New request created
SHOPPING_CART_NOTIFY_ON_CLAIM = True         # Request claimed
SHOPPING_CART_NOTIFY_ON_COMPLETION = True    # Request completed
SHOPPING_CART_NOTIFY_ON_CANCELLATION = False # Request cancelled
```

### Notification Examples

**New Request Created:**
```
🛒 New Request #42
User: JohnDoe created a new request
Type: Requester Has Items | Items: 5 items
Route: Jita IV → Amarr VIII
```

**Request Claimed:**
```
✋ Request #42 Claimed
Fulfiller: JaneDoe claimed the request
Original Requester: JohnDoe
```

**Request Completed:**
```
✅ Request #42 Completed!
Contract has been completed
Requester: JohnDoe | Fulfiller: JaneDoe
```

### Webhook Security

- Keep webhook URL private
- Regenerate if compromised (Discord server settings)
- URL contains authentication token
- Do not commit URL to public repositories

---

## ⚙️ Celery Tasks

Shopping Cart includes background tasks for automation.

### Periodic Tasks

| Task | Schedule | Purpose |
|------|----------|---------|
| `shopping_cart_monitor_active_contracts` | Every 10 minutes | Check contract status via ESI |
| `shopping_cart_cleanup_old_requests` | Daily at 3:00 AM UTC | Remove old completed/cancelled requests |
| `shopping_cart_expire_abandoned_requests` | Daily at 4:00 AM UTC | Mark old pending requests as expired |

### Configuration

Tasks are configured in `local.py` as shown in [Step 5 of Installation](#step-5-configure-celery-tasks-required).

### Manual Task Execution

You can manually trigger tasks from Django shell:

```python
from shopping_cart.tasks import monitor_contract_status, cleanup_old_requests

# Monitor specific request
monitor_contract_status.delay(request_id=42)

# Run cleanup now
cleanup_old_requests.delay()
```

### Verify Celery is Running

```bash
# Check Celery worker status
supervisorctl status myauth-worker

# Check Celery beat status (scheduler)
supervisorctl status myauth-beat

# View Celery logs
tail -f /var/log/supervisor/myauth-worker.log
tail -f /var/log/supervisor/myauth-beat.log
```

### Task Logs

You should see entries like:
```
[INFO] Scheduler: Sending due task shopping_cart_monitor_active_contracts
[INFO] Task shopping_cart.tasks.monitor_all_active_contracts[abc-123] succeeded
```

---

## 🔧 Troubleshooting

### Installation Package Not Found Error

**Issue:** `ERROR: Could not find a version that satisfies the requirement shopping_cart==0.1.0`

**Cause:** Mismatch between package name and app name in configuration.

**Solution:**
- **For GitHub installation:** Use `allianceauth-shopping-cart==0.1.0` in requirements.txt
- **App name in INSTALLED_APPS:** Always use `'shopping_cart'` (the Python module name)
- **Package name for pip:** Use `allianceauth-shopping-cart` (from pyproject.toml)

```bash
# In requirements.txt (for Alliance Auth)
allianceauth-shopping-cart==0.1.0

# In local.py INSTALLED_APPS
INSTALLED_APPS += [
    'shopping_cart',  # Python module name, not package name
]
```

### App Not Showing in Menu

**Possible Causes:**
- User doesn't have `basic_access` permission
- App not in `INSTALLED_APPS`
- Services not restarted after installation

**Solutions:**
```bash
# Verify settings
python manage.py diffsettings | grep shopping_cart

# Check permissions
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='yourname')
>>> user.has_perm('shopping_cart.basic_access')

# Restart services
supervisorctl restart myauth:
```

### Cannot Create Requests

**Possible Causes:**
- Missing `request_items` permission
- No main character set
- Form validation errors

**Solutions:**
- Assign `request_items` permission
- Set main character in profile
- Check for JavaScript errors (F12 developer console)

### Contract Tracking Not Working

**Possible Causes:**
- Missing ESI token
- Wrong scope on token
- Celery not running
- Monitoring character not set

**Solutions:**
```bash
# Check Celery is running
supervisorctl status myauth-worker
supervisorctl status myauth-beat

# Verify ESI token
python manage.py shell
>>> from esi.models import Token
>>> Token.objects.filter(character_id=YOUR_CHAR_ID).require_scopes(['esi-contracts.read_character_contracts.v1']).require_valid().first()

# Manually trigger monitoring
>>> from shopping_cart.tasks import monitor_contract_status
>>> monitor_contract_status.delay(request_id=42)
```

### Celery Tasks Not Running

**Possible Causes:**
- Celery beat not running
- Tasks not added to `CELERYBEAT_SCHEDULE`
- Syntax error in `local.py`

**Solutions:**
```bash
# Check Celery beat status
supervisorctl status myauth-beat

# Restart Celery beat
supervisorctl restart myauth-beat

# Check logs for errors
tail -f /var/log/supervisor/myauth-beat.log

# Verify configuration
python manage.py shell
>>> from django.conf import settings
>>> 'shopping_cart_monitor_active_contracts' in settings.CELERYBEAT_SCHEDULE
True
```

### Database Migration Errors

**Issue:** Migration fails with foreign key error

**Solution:**
```bash
# Ensure eveonline app is migrated first
python manage.py migrate eveonline

# Then migrate shopping_cart
python manage.py migrate shopping_cart
```

### Static Files Not Loading

**Issue:** CSS/JS not working, pages look broken

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify STATIC_ROOT setting
python manage.py findstatic shopping_cart/css/shopping_cart.css

# Check web server (nginx/apache) static file serving
```

### Discord Notifications Not Sending

**Possible Causes:**
- Invalid webhook URL
- Webhook deleted in Discord
- Network connectivity issues

**Solutions:**
```bash
# Test webhook manually
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message"}'

# Check logs for errors
tail -f /var/log/allianceauth/allianceauth.log | grep shopping_cart
```

### Performance Issues

**Issue:** Slow page loads or timeouts

**Solutions:**
- Enable database query caching
- Increase gunicorn workers
- Optimize PostgreSQL settings
- Check Celery queue backlog

```bash
# Check Celery queue length
python manage.py shell
>>> from celery import current_app
>>> current_app.control.inspect().active_queues()
```

---

## 💻 Development

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/atthompson13/aa-shoppingcart.git
cd aa-shoppingcart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=shopping_cart --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with Black
black shopping_cart/

# Sort imports
isort shopping_cart/

# Lint with Flake8
flake8 shopping_cart/ --max-line-length=119

# Type checking (if using mypy)
mypy shopping_cart/
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Testing Against Multiple Versions

```bash
# Install tox
pip install tox

# Run tests against all environments
tox

# Run specific environment
tox -e py311-django42
```

### Building Documentation

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Build docs
cd docs
make html

# View docs
open _build/html/index.html
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Reporting Bugs

1. Check [existing issues](https://github.com/atthompson13/aa-shoppingcart/issues)
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (AA version, Python version, etc.)
   - Relevant log output

### Suggesting Features

1. Check [existing feature requests](https://github.com/atthompson13/aa-shoppingcart/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Create new issue with:
   - Clear description of feature
   - Use cases and benefits
   - Implementation ideas (optional)

### Submitting Pull Requests

1. **Fork the repository**
2. **Create feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes:**
   - Follow existing code style
   - Add tests for new features
   - Update documentation
   - Keep commits focused and atomic
4. **Run tests:**
   ```bash
   pytest
   black shopping_cart/
   flake8 shopping_cart/
   ```
5. **Commit changes:**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to fork:**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Create Pull Request** on GitHub

### Code Style Guidelines

- Follow **PEP 8**
- Use **Black** for formatting (line length: 119)
- Add **docstrings** to functions and classes
- Keep functions **focused and small**
- Write **meaningful commit messages**
- Add **type hints** where appropriate

### Development Principles

- **Test coverage:** Aim for >80% coverage
- **Documentation:** Update docs with new features
- **Backwards compatibility:** Don't break existing functionality
- **Performance:** Consider scalability
- **Security:** Validate all user input

---

## 📝 Changelog

### [0.1.0] - 2025-10-02

#### Added
- Initial production release
- Dual workflow system (requester has items OR fulfiller buys)
- Complete Django app with 16 Python modules
- 9 responsive HTML templates with Bootstrap
- ESI contract tracking and auto-completion
- Discord webhook notifications
- Celery background tasks for automation
- Permission system (basic_access, request_items, fulfill_requests, manage_requests)
- Fulfiller leaderboard with statistics
- Admin dashboard for management
- EVE item parser (copy/paste from game)
- Database migrations
- Comprehensive documentation

#### Technical
- Python 3.8+ support
- Django 4.0+ compatibility
- Alliance Auth 4.0+ integration
- PostgreSQL/MySQL support
- Celery task queue
- ESI API integration

---

## 🆘 Support

### Getting Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/atthompson13/aa-shoppingcart/issues)
- **Alliance Auth Discord:** [Join the community](https://discord.gg/allianceauth)
- **Documentation:** You're reading it! Check sections above

### Useful Links

- **Repository:** https://github.com/atthompson13/aa-shoppingcart
- **Alliance Auth Docs:** https://allianceauth.readthedocs.io/
- **EVE ESI Docs:** https://esi.evetech.net/ui/

### Before Asking for Help

1. Check this README thoroughly
2. Review [Troubleshooting](#troubleshooting) section
3. Check existing GitHub issues
4. Check Alliance Auth logs:
   ```bash
   tail -f /var/log/allianceauth/allianceauth.log
   ```
5. Include relevant error messages and logs when asking

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

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
```

See [LICENSE](LICENSE) file for full text.

---

## 🙏 Acknowledgments

- **Alliance Auth Team** - For the amazing platform
- **EVE Online Community** - For inspiration and feedback
- **Contributors** - Everyone who helps improve this project

Special thanks to:
- django-esi developers
- django-eveuniverse developers
- Bootstrap framework
- All beta testers

---

## 🗺️ Roadmap

Future enhancements being considered:

- [ ] Advanced marketplace filtering and sorting
- [ ] User rating system for fulfillers
- [ ] In-app messaging between requester and fulfiller
- [ ] Price calculation helpers using ESI market data
- [ ] Automatic item volume calculations
- [ ] Multi-contract support for large requests
- [ ] Request templates for common orders
- [ ] Enhanced statistics dashboard
- [ ] Export functionality (CSV, Excel)
- [ ] API endpoints for third-party integrations
- [ ] Mobile app (potential)

Want to see something specific? [Open a feature request!](https://github.com/atthompson13/aa-shoppingcart/issues/new)

---

<div align="center">

**Made with ❤️ for the EVE Online community**

**Author:** atthompson13  
**Last Updated:** 2025-10-02 04:00:32 UTC

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/atthompson13/aa-shoppingcart/issues) · [Request Feature](https://github.com/atthompson13/aa-shoppingcart/issues) · [View Releases](https://github.com/atthompson13/aa-shoppingcart/releases)

</div>





