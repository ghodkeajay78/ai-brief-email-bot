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
Act as The AI Brief, a newsletter-style AI news summarizer.
Generate today’s AI Brief in Twitter thread format for {today}.
Include:
- 1 viral or trending story at the top with context and link
- 2-3 impactful model/tool releases with what they do, why it matters, and links
- 1 recent research paper or capability
- 2-3 short company news bites at the bottom
Make it insightful and engaging for AI developers.
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
    return response.choices[0
