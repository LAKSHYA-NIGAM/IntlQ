# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| `main`  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in **IntlQ**, please follow responsible disclosure practices:

1. **Do NOT open a public GitHub Issue** for security vulnerabilities.
2. **Email** the maintainer directly at: `lakshyanigam20@gmail.com`
   - Subject: `[SECURITY] IntlQ - <brief description>`
   - Include: steps to reproduce, potential impact, and suggested fix (if any).
3. You will receive an acknowledgement within **48 hours**.
4. We aim to release a patch within **7 days** for confirmed critical vulnerabilities.

## Security Best Practices for Contributors

- Never commit API keys, tokens, passwords, or `.env` files.
- Use environment variables for all secrets (see `.env.example`).
- Validate and sanitize all user inputs before processing.
- Keep dependencies up to date — run `pip-audit` regularly.
- Avoid logging sensitive data (tokens, PII, passwords).

## Known Security Controls

- Interview responses processed locally without external API calls
- No personally identifiable information logged
- Flask session data encrypted with SECRET_KEY
- Input length limits prevent memory exhaustion

---

We appreciate responsible disclosure and will credit reporters in our release notes (unless anonymity is requested).
