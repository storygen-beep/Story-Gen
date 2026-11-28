# Lead agent (MVP skeleton)

An AI lead agent for businesses, starting with Dubai real-estate agencies on WhatsApp.
There is one shared engine, and each business has a **playbook** that tells it
what to ask, who counts as a hot lead, who to hand leads to, and which rules to follow.

This lives in a folder of the Story-Gen repo for now and will move to its own repo later.

## Apps

| App | Tables |
|---|---|
| `accounts` | Organization (an agency), Agent (a team member) |
| `playbooks` | IndustryTemplate, Playbook, PlaybookVersion, KnowledgeItem |
| `leads` | Lead, Inquiry, Handoff, FollowUpTask, LeadEvent |
| `messaging` | Channel (a WhatsApp number), MessageTemplate, Conversation, Message, plus the WhatsApp webhook |

Playbook content is a versioned JSON document. The Dubai real-estate template is at
`playbooks/templates_data/real_estate_dubai.json`.

## Run locally

```bash
cd leadgen
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_templates
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver      # admin at http://localhost:8000/admin/
.venv/bin/python manage.py test
```

SQLite is used locally. Configuration comes from environment variables:
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` and `WHATSAPP_VERIFY_TOKEN`.

## WhatsApp webhook

`/webhooks/whatsapp/` handles:
- Meta's verification handshake (GET)
- incoming messages (POST), stored as a Lead plus a Message; duplicate deliveries are ignored.

It does not yet check Meta's signature header. Add that before going live.

## Built so far

- [x] Data model and admin
- [x] Real-estate playbook template
- [x] WhatsApp webhook: receive and store messages

## Not built yet

- [ ] Sending messages (Cloud API) and the first-reply template
- [ ] AI reply and answer extraction (Claude API)
- [ ] Rules checker
- [ ] Scoring
- [ ] Handoff with a backup timer
- [ ] Follow-ups (Celery)
- [ ] Portal email intake
- [ ] Voice-note transcription
- [ ] Webhook signature check
