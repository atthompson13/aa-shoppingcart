# Alliance Auth Shopping Cart

A comprehensive player-to-player shopping cart and contract marketplace system for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.0+](https://img.shields.io/badge/django-4.0+-green.svg)](https://www.djangoproject.com/)
[![Alliance Auth](https://img.shields.io/badge/allianceauth-4.0+-purple.svg)](https://gitlab.com/allianceauth/allianceauth)

## Overview

Shopping Cart enables EVE Online players in your alliance to create item requests and have them fulfilled by other members. It supports two distinct workflows and features automatic contract tracking via ESI integration.

## Features

### 🛒 Dual Workflow System

**Workflow A: Requester Has Items**
- Player has items and needs them delivered
- Creates request with pickup/delivery locations
- Fulfiller claims request and coordinates pickup
- Requester creates courier contract
- System tracks contract via ESI and auto-completes

**Workflow B: Fulfiller Buys Items**
- Player needs items purchased and delivered
- Creates request with shopping list and budget
- Fulfiller buys items and creates contract
- System tracks acceptance and completion

### 🎯 Core Functionality

- **Item Request Creation** - Easy-to-use forms with EVE item paste support
- **Marketplace** - Browse and claim available requests
- **Request Management** - Track your requests and fulfillments
- **ESI Contract Tracking** - Automatic status updates via ESI API
- **Discord Notifications** - Real-time updates via webhooks
- **Fulfiller Leaderboard** - Gamification and recognition system
- **Admin Dashboard** - Comprehensive management tools

### 🔐 Permission System

- `basic_access` - View and access the app
- `request_items` - Create item requests
- `fulfill_requests` - Claim and fulfill orders
- `manage_requests` - Full administrative control

### 🤖 Automation

- Automatic contract status monitoring (every 10 minutes)
- Auto-completion when contracts finish
- Automatic cleanup of old requests (configurable)
- Expired request handling for abandoned carts

## Screenshots

*Coming soon - screenshots of marketplace, request details, and leaderboard*

## Requirements

- Alliance Auth 4.0.0 or higher
- Python 3.8 or higher
- Django 4.0 or higher
- PostgreSQL or MySQL (recommended)

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

**Quick Install:**
```bash
pip install git+https://github.com/atthompson13/aa-shoppingcart.git
