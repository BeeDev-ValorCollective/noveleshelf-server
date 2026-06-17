# NovelShelf Mail Server

Contact form and unsubscribe email service for the NovelShelf platform.

---

## Status

Built and deployed. Node/Express, hosted on iFast cPanel. Not currently planned to be folded into the Django API — kept as a standalone service, consistent with how other BeeDev client projects (e.g. SMTS) handle transactional email.

---

## What it does

### Contact form (`POST /api/sendContactMail`)
Accepts a contact form submission and routes it based on `contactType`:
- Novel eShelf business inquiries → client inbox
- Technical/BeeDev issues → BeeDev inbox
- `other` type → both inboxes via cc

The `from` display name and email subject line are both generated server-side from `contactType` (e.g. `Novel eShelf <contact@noveleshelf.com>` with subject `Business Inquiry — Novel eShelf`, vs `BeeDev Services <melissa@beedev-services.com>` with subject `Technical Issue — Novel eShelf`). The frontend does not send a subject — only `contactType`, and the server decides both the subject and the sending identity from that.

Protected by a captcha + honeypot pair (see below) to deter bot submissions.

### Unsubscribe (`POST /api/sendUnsubMail`)
Collects email (required) and a reason from a dropdown (required: too many emails, content not relevant, found what I needed, privacy concerns, other), plus optional first name, last name, and username for a friendlier confirmation email. No phone field — Novel eShelf is email-only, unlike other BeeDev client projects that also handle phone unsubscribes.

No captcha on this route — since it's a transactional action the user already initiated (clicking an unsubscribe link), spam protection wasn't considered necessary here.

### Captcha (`GET /api/captcha`)
A simple math-style captcha used only on the contact form. Frontend fetches a question/id pair on mount, displays the question, and sends the answer back with the form submission alongside a hidden honeypot field (`website`) that legitimate users never fill in. Captcha middleware rejects the submission with 400 on a wrong answer or a filled honeypot field, and the frontend should re-fetch a fresh captcha on failure.

---

## Architecture

Follows the same pattern as BeeDev's other Node mail services (e.g. SMTS):
- `controllers/mail.controller.js` — contact form logic, `getRouting()` determines recipients/from/subject per `contactType`
- `controllers/unsub.controller.js` — unsubscribe logic, separate file rather than added to the contact controller
- `models/mail.model.js` / `models/unsub.model.js` — simple data classes for each form's fields
- `routes/mail.routes.js` — both routes wired here, pulled into `server.js` under `/api`
- `captchaStore.js` / `captcha.middleware.js` — pure utility, reusable across projects, only attached to the contact route

---

## Environment variables

Required (exact names matter — a mismatch here is a common cause of 500s on send):
```
CONTACT_FROM_NAME       display name for outgoing contact form emails
CONTACT_FROM            reply-to address shown to recipients
CONTACT_EMAIL_USER      actual SMTP sending account
CONTACT_EMAIL_PASS      app password for the sending account (not the regular login password)
NOREPLY_EMAIL_USER      sending account used for unsubscribe confirmations
NOREPLY_EMAIL_PASS      app password for that account
EMAIL_HOST              smtp.gmail.com (Google Workspace)
EMAIL_PORT              465
EMAIL_SSL               true
```

`require("dotenv").config()` must be the very first line in `server.js` — if anything that depends on `process.env` (like CORS setup) runs before dotenv loads, those values silently come through as `undefined`.

---

## Deployment (iFast / cPanel)

Hosted at `hivemail-11.thehive-services.com`-style Passenger/cPanel setup (confirm current path/account for this specific project before deploying — the hosting account and path are client-specific and were not re-verified for Novel eShelf at the time this README was last updated).

General notes carried over from similar BeeDev mail server deployments:
- Runs under Phusion Passenger with Apache
- Startup file is `server.js`
- After any `.env` change, restart the app for the new values to take effect
- If you see unexplained 500s with env-dependent middleware (CORS, mail auth), check the order of `require("dotenv").config()` relative to everything else in `server.js` first

---

## Known gaps / not yet decided

- Exact current cPanel account/path for the Novel eShelf instance of this service should be confirmed and documented here rather than assumed from similar projects.
- No automated tests — testing has been done manually via Postman per change.

---

[← Back to Repository README](../README.md)