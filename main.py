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
Act as The AI Brief, a newsletter-style AI digest for developers.

Create today's AI Brief for {today} in HTML format (not Markdown, not plaintext).
Include clear sections with:
1. A trending topic (headline, summary, link)
2. 2-3 major AI model/tool releases (what it does, why it matters, link)
3. A research highlight (paper, summary, impact, link)
4. 2-3 short news bites (bullet points, with links)

Format it with:
- ✅ HTML structure (no CSS file, just inline styles)
- ✅ Section headers using `<h2>` or bold tags
- ✅ Bullet points or boxed sections using `<ul>`, `<div>`, or emojis
- ✅ Optional small AI-related image URLs (if helpful or symbolic)

Tone: professional, clear, dev-focused — but visually appealing like a mini newsletter.
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

    # Attach as HTML
    body = MIMEText(content, 'html')
    msg.attach(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    content = get_ai_brief()
    send_email(content)
    print("✅ The AI Brief sent!")
