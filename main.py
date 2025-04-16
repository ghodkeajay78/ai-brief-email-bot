import os
import openai
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def fetch_latest_ai_trends():
    params = {
        "q": "latest AI trends today",
        "api_key": SERP_API_KEY,
        "num": 5
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    if "organic_results" in results:
        articles = results["organic_results"][:5]
        trend_snippets = ""
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No Title")
            link = article.get("link", "")
            snippet = article.get("snippet", "")
            trend_snippets += f"{i}. <b>{title}</b><br>{snippet}<br><a href='{link}'>{link}</a><br><br>"
        return trend_snippets
    else:
        return "No trends available."

def generate_prompt(ai_trends_html):
    today = datetime.now().strftime('%B %d, %Y')
    return f"""
You are The AI Brief, an HTML newsletter for developers covering real AI news, model releases, tools, research, and trends.

Today is {today}. Use the real trends below in your content where relevant:

{ai_trends_html}

Now write the full newsletter in clean HTML format (no markdown, no placeholder text). It should:

- 🧠 Include at least 4 *real or plausible* stories relevant to developers
- 🔥 Include 1 viral/trending AI news story with context and a real or plausible link
- 🛠 Highlight 2–3 AI tools or models (name, use case, capability, demo or GitHub link)
- 🧪 Include 1 research paper or capability with a brief summary and how it can be used
- 🧵 Share 1 cool thing developers are building with AI (e.g., open source project or unique use)
- 📬 End with 2–3 short news bites and a subscription link (Google Form)
- Include section headers using `<h2>` and style it like a modern, readable newsletter
- Use light background, readable fonts, and clean layout with emojis for each section

Start with a full-width AI-themed lightweight banner image at the top (link to Unsplash or similar).
Return only clean, usable HTML — no markdown, no lorem ipsum, no filler.
"""

def get_ai_brief():
    ai_trends_html = fetch_latest_ai_trends()
    prompt = generate_prompt(ai_trends_html)

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

def send_email(content):
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"The AI Brief — {datetime.now().strftime('%b %d')}"

    clean_content = content.strip().removeprefix("'''html").removeprefix("```html").strip("`'")
    body = MIMEText(clean_content, 'html')
    msg.attach(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    content = get_ai_brief()
    send_email(content)
    print("✅ The AI Brief with SerpAPI trends sent!")
