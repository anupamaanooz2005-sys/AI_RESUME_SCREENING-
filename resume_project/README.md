# ResumeAI Screener

AI-powered resume screening Django app with **Candidate Portal** and **HR Dashboard**.

## URLs

| Route | Page |
|-------|------|
| `http://127.0.0.1:8000/` | Home / Landing |
| `http://127.0.0.1:8000/candidate/` | Candidate Portal |
| `http://127.0.0.1:8000/hr/` | HR Dashboard |
| `http://127.0.0.1:8000/admin/` | Django Admin |

## Setup (first time)

```bash
# 1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. (Optional) Create admin user
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

## Project Structure

```
resume_project/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created after migrate
├── media/uploads/          ← uploaded resumes stored here
├── resume_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── screening/
    ├── ai.py               ← NLP engine (keyword extraction, scoring)
    ├── views.py            ← candidate, hr_dashboard, hr_analyze, share
    ├── models.py           ← Resume, Prediction, HRSession
    ├── urls.py             ← URL routing
    └── templates/screening/
        ├── base.html       ← shared nav, CSS, share modal
        ├── home.html       ← landing page
        ├── candidate.html  ← candidate upload + result
        ├── hr.html         ← HR bulk upload + AJAX ranking
        └── share.html      ← shared link landing
```

## Features

### Candidate Portal (`/candidate/`)
- Upload PDF, DOC, DOCX, or TXT resume
- AI predicts job category (12 categories)
- Shows match score %, category breakdown bars
- Lists skills found (green) and missing skills (red)

### HR Dashboard (`/hr/`)
- Bulk upload multiple resumes at once
- Filter by job category
- Add required keywords/skills as chips (press Enter)
- Set minimum match score threshold (slider)
- AJAX analysis — no page reload
- Ranked table with final score, keyword hits, top skills
- Below-threshold candidates shown separately

### Share Feature
- Share button in nav copies current URL
- WhatsApp, Email, LinkedIn share shortcuts
- `/share/` landing page for invited users

## Extending

- **Better NLP**: Replace keyword matching in `ai.py` with spaCy or sentence-transformers
- **Export**: Add CSV export of HR results
- **Auth**: Add login for HR portal using Django's built-in auth
- **Email**: Use Django's email backend to notify candidates
