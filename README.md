# 🚀 AI Website Builder (Python & Django)

An intelligent, full-stack web application powered by **Django** and **Google Gemini AI** that transforms simple business descriptions into complete, modern, and production-ready responsive single-page websites in seconds.

---

## ✨ Features

- ⚡ **Instant AI Generation**: Transforms business name, industry type, and description into rich website copy and structured HTML5 layout.
- 🤖 **Multi-Model Fallback Engine**: Uses fast Google Gemini Flash models (`gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-flash-latest`, `gemini-2.5-flash-lite`) with structured JSON schema output and intelligent error handling.
- 🎨 **Modern Design Architecture**: Generates standalone, mobile-responsive HTML5 pages equipped with Google Fonts, glassmorphism effects, gradient accents, hero sections, stats counters, service cards, testimonials, FAQ accordions, and call-to-action footers.
- 👤 **User Authentication**: Secure user registration, login, and session management.
- 📊 **Dashboard & Rate Limiting**: Real-time stats showing generated sites, daily generation count, and built-in rate-limiting (5 generations/day per user).
- 👁️ **Live Interactive Preview**: Integrated iframe previewer with raw HTML view mode.
- 💾 **One-Click Export**: Download the generated website as a clean, standalone `.html` file ready for deployment to GitHub Pages, Netlify, Vercel, or any static host.
- 🗑️ **Project Management**: Manage, view, download, or delete past generated websites.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 4.2+ / 5.x
- **AI Integration**: Google Gemini API (`generativelanguage.googleapis.com`)
- **Database**: SQLite (default, zero setup required)
- **Frontend**: Django Templates, Modern CSS (Glassmorphism & Dark UI), Vanilla JavaScript
- **Environment Management**: `python-dotenv`

---

## 📁 Project Structure

```text
ai-website-builder-python/
├── ai_website_builder_project/     # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Core settings & Gemini configurations
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py
├── builder/                        # Core AI Builder App
│   ├── migrations/                 # Database migrations
│   ├── admin.py                    # Django Admin configuration
│   ├── ai_service.py               # Gemini AI prompt & API integration logic
│   ├── forms.py                    # Auth & Business input forms
│   ├── models.py                   # Business & Website database models
│   ├── urls.py                     # App routing (dashboard, preview, export)
│   └── views.py                    # Views and business logic
├── templates/                      # HTML Templates
│   ├── base.html                   # Base layout with navbar & flash messages
│   ├── auth/                       # Login & Registration templates
│   │   ├── login.html
│   │   └── register.html
│   └── website/                    # App templates
│       ├── add_business.html       # Business input form
│       ├── dashboard.html          # User dashboard with stats & sites list
│       └── preview.html            # Interactive website previewer
├── static/                         # Static Assets
│   └── css/
│       └── styles.css              # Custom styling & glassmorphism theme
├── .env.example                    # Sample environment variables
├── manage.py                       # Django CLI utility
└── requirements.txt                # Python dependencies
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/ai-website-builder-python.git
cd ai-website-builder-python
```

### 3. Create and Activate a Virtual Environment

- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root by copying `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and provide your Google Gemini API key:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
GEMINI_API_KEY=your_gemini_api_key_here
```

> 🔑 **Get a Gemini API Key**: Obtain a free API key at [Google AI Studio](https://aistudio.google.com/).

### 6. Run Database Migrations
```bash
python manage.py migrate
```

### 7. (Optional) Create an Admin Superuser
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## ⚙️ Environment Variables

| Variable | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key | **Yes** | `""` |
| `SECRET_KEY` | Django secret key for session security | No | Development key |
| `DEBUG` | Enables/disables debug mode (`True`/`False`) | No | `True` |
| `GEMINI_API_URL` | API endpoint for Gemini generation | No | `gemini-flash-latest` endpoint |

---

## 📖 How It Works

1. **User Input**: The user provides a business name, category/industry, and description via the web form.
2. **AI Processing**: [builder/ai_service.py](file:///builder/ai_service.py) constructs an engineered prompt instructing Gemini to return a structured JSON response containing:
   - Optimized title and marketing tagline
   - About story and value propositions
   - Key service offerings
   - Complete, self-contained, responsive HTML5 code with embedded modern CSS
3. **Storage**: The generated site metadata and HTML code are stored in the database linked to the user's account.
4. **Live Preview & Download**: The user can preview the generated website inside a simulated browser view or download it directly as an `.html` file.

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more details.
