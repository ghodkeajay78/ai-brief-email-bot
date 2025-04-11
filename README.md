# The AI Brief Email Bot

This bot sends a daily AI news summary in Twitter-thread style, created by GPT-4, straight to your email.

## Features
- Uses GPT-4 to write AI newsletter content
- Runs automatically every day at 9 AM IST via GitHub Actions
- Sends a styled email to a configured address

## Setup

1. Upload the files in this repo (`main.py`, `requirements.txt`, `.github/workflows/daily.yml`)
2. Go to **Settings > Secrets > Actions** and add the following secrets:
   - `OPENAI_API_KEY`
   - `EMAIL`
   - `EMAIL_PASSWORD` (use a Gmail App Password)
   - `TO_EMAIL`

3. You're done! GitHub Actions will run daily and email you the newsletter.

Enjoy your daily dose of AI ✨

