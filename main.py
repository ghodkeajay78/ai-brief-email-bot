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
You are The AI Brief, an HTML newsletter for developers covering real AI news, model releases, tools, research, and trends.

Write today's AI Brief for {today} in full HTML format (no markdown, no placeholder text, no lorem ipsum). It should:

- 🧠 Include at least 4 *real or plausible* stories relevant to developers
- 🔥 Include 1 viral/trending AI news story with context and a real or plausible link
- 🛠 Highlight 2–3 AI tools or models (name, use case, capability, demo or GitHub link)
- 🧪 Include 1 research paper or capability with a brief summary and how it can be used
- 🧵 Share 1 cool thing developers are building with AI (e.g., open source project or unique use)
- 📬 End with 2–3 short news bites and a subscription link (Google Form)
- Include section headers using `<h2>` and style it like a modern, readable newsletter
- Use light background, readable fonts, and clean layout with emojis for each section

Use a clean light background color (#f7f9fc). Add a small banner image at the top (unsplash or similar, <100KB) using <img>, not background-image.
Return only clean, usable HTML — no markdown, no lorem ipsum, no filler.
"""

def get_ai_brief():
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": generate_prompt()}
        ],
        temperature=0.5
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
