# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Security vulnerabilities should not be publicly disclosed until they have been addressed.

### 2. Report Privately

Email security details to: **security@ai-whisperers.com**

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies by severity

### 4. Disclosure Policy

- We will acknowledge your report within 48 hours
- We will provide a detailed response within 7 days
- We will work with you to understand and resolve the issue
- We will publicly disclose the vulnerability after a fix is released

## Security Best Practices

### API Keys

- **Never** commit API keys to the repository
- Use `.env` files (already in `.gitignore`)
- Rotate keys regularly
- Use environment-specific keys

### Dependencies

- Keep dependencies up to date
- Run `pip audit` regularly
- Review security advisories

### Data Protection

- Encrypt sensitive data at rest
- Use HTTPS for all API calls
- Implement rate limiting
- Validate all inputs

## Known Security Considerations

### API Key Exposure

- Ensure `.env` files are never committed
- Use GitHub secret scanning
- Rotate keys if exposed

### AI Provider Security

- API keys are transmitted over HTTPS
- No sensitive data is logged
- Responses are not cached with sensitive info

### Video Generation

- Veo 3.1 API uses Google Cloud authentication
- Service account credentials should be secured
- Videos are stored locally by default

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1) and documented in [CHANGELOG.md](CHANGELOG.md).

## Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who report vulnerabilities.

---

**Last Updated**: 2024-11-26
