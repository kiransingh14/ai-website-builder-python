import json
import logging
import re
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

SUPPORTED_MODELS = [
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-flash-latest',
    'gemini-2.5-flash-lite',
]


def generate_website_content(business):
    """
    Calls Google Gemini API with intelligent fallback across fast Flash models
    to generate complete, modern responsive website content and HTML.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in .env or settings.")

    prompt = f"""
You are an award-winning web designer and full-stack developer. Generate a complete, high-converting, and visually stunning responsive homepage for the following business.

Business Details:
- Name: {business.name}
- Type: {business.type}
- Description: {business.description}

You MUST return STRICT JSON ONLY (no markdown backticks, no text before or after).
The JSON schema MUST match:
{{
  "title": "{business.name} - {business.type}",
  "tagline": "A compelling 1-sentence value proposition",
  "about": "Engaging 2-3 paragraphs describing the company story, quality, and commitment.",
  "services": ["Detailed service 1", "Detailed service 2", "Detailed service 3", "Detailed service 4"],
  "html": "<!DOCTYPE html>...complete standalone HTML5 document..."
}}

Requirements for the 'html' field:
1. Complete self-contained HTML5 code with <head>, <style>, <body>.
2. Link to Google Fonts (e.g. 'Plus Jakarta Sans' or 'Outfit' or 'Inter').
3. Modern luxury/tech styling: smooth CSS gradients, glassmorphism cards, glowing badges, elegant typography, flex/grid layouts, mobile-responsive breakpoints, interactive hover states.
4. Sections to include:
   - Header with brand logo & navigation links + CTA button
   - Hero section with badge, powerful headline, subtitle, and 2 CTA buttons
   - Stats / Metrics strip (e.g. '99.8% Satisfaction', '15k+ Happy Clients', '5★ Rated')
   - Services / Offerings Grid (4-6 modern cards with icons/emojis and descriptive text)
   - About Us Story section with feature highlights
   - Testimonials / Reviews grid
   - FAQ Accordion / Grid
   - Final CTA banner
   - Modern footer with copyright & links
5. Ensure valid CSS and all quotes inside the HTML string are properly escaped for JSON.
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }

    last_error = None

    for model_name in SUPPORTED_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=50)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        raw_text = parts[0].get('text', '').strip()
                        parsed = _clean_and_parse_json(raw_text)
                        if parsed and isinstance(parsed, dict) and parsed.get('title'):
                            return _ensure_defaults(parsed, business)
            else:
                logger.warning(f"Model {model_name} returned status {response.status_code}: {response.text[:200]}")
        except Exception as e:
            logger.warning(f"Failed attempt with model {model_name}: {e}")
            last_error = e

    # Fallback attempt without responseMimeType if structured JSON mode failed
    for model_name in SUPPORTED_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        simple_payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(url, json=simple_payload, headers=headers, timeout=50)
            if response.status_code == 200:
                data = response.json()
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                parsed = _clean_and_parse_json(raw_text)
                if parsed and isinstance(parsed, dict):
                    return _ensure_defaults(parsed, business)
        except Exception as e:
            last_error = e

    raise ValueError(f"Unable to generate website content via Gemini AI: {last_error}")


def _clean_and_parse_json(raw_text):
    text = raw_text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try finding json block inside text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return None


def _ensure_defaults(data, business):
    if not data.get('title'):
        data['title'] = f"{business.name} - {business.type}"
    if not data.get('tagline'):
        data['tagline'] = f"Excellence in {business.type}"
    if not data.get('about'):
        data['about'] = business.description
    if not data.get('services'):
        data['services'] = ["Custom Solutions", "Premium Quality", "24/7 Support"]
    if not data.get('html'):
        data['html'] = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{business.name}</title>
    <style>body {{ font-family: sans-serif; padding: 40px; background: #0f172a; color: white; }}</style>
</head>
<body>
    <h1>{business.name}</h1>
    <p>{business.description}</p>
</body>
</html>"""
    return data
