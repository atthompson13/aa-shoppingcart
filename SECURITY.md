# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

1. **Email:** atthompson13@users.noreply.github.com
2. **GitHub Private Security Advisory**

You should receive a response within 48 hours. If confirmed, we will:

1. Release a patch as soon as possible
2. Credit you in the security advisory (unless you prefer anonymity)
3. Notify users via release notes

## Security Best Practices

When deploying Shopping Cart:

- Keep Alliance Auth and dependencies up to date
- Use HTTPS/TLS for all connections
- Secure Discord webhook URLs
- Rotate ESI tokens regularly
- Follow Alliance Auth security guidelines
- Use strong database credentials
- Enable Django security middleware
- Configure ALLOWED_HOSTS properly

## Known Security Considerations

- ESI tokens stored in database (encrypted by django-esi)
- Discord webhook URLs should be private
- Assign user permissions carefully
- Contract IDs visible within your alliance

Thank you for helping keep Shopping Cart secure!
