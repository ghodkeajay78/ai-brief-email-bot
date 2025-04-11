import os
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def generate_prompt():
    today = datetime.now().strftime('%B %d, %Y')
    return f"""
You are The AI Brief — a highly visual, developer-focused daily AI newsletter generator.

Create a complete HTML email for {today} with:
✅ Full HTML layout — clean, readable, email-safe HTML
✅ Inline CSS (no external styles)
✅ Start with a full-width AI-themed banner image at the top
✅ Section headers with emojis/icons (🔥 🧠 🧪 🧵 📬)
✅ Up to 6 sections:
  1. 🔥 Trending story (summary, why it matters, and image)
  2. 🧠 New AI model/tool #1 — what it does, why it’s useful for devs, how it compares, demo or link
  3. 🛠️ New tool #2 or updated feature
  4. 🧪 Research highlight (plus potential impact)
  5. 🧵 What developers are building (cool GitHub project or creative usage)
  6. 📬 Quick bites (5-8 short items: funding, launches, partnerships)

Use elements like:
- `<style>` tag for basic typography, background, container style
- `<div>`, `<h2>`, `<p>`, `<ul>` for layout
- `<img src="..." style="width:100%;">` for images
- Clear spacing and section separation

Tone: Dev-smart, engaging, not overly formal — feels like a clean Substack issue.
Only return valid HTML. Do NOT include triple quotes, markdown, or code blocks.
"""

def get_ai_brief():
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": generate_prompt()}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def send_email(content):
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"The AI Brief — {datetime.now().strftime('%b %d')}"

    # Remove leading '''html or ```html if accidentally included
    clean_content = content.strip().removeprefix("'''html").removeprefix("```html").strip("`'")

    # Attach as HTML
    body = MIMEText(clean_content, 'html')
    msg.attach(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    content = get_ai_brief()
    send_email(content)
    print("✅ The AI Brief sent!")
