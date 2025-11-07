# ✅ Function to send email
import os
from email.message import EmailMessage
import aiosmtplib
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path

async def send_email(contact):
    """Sends an email notification with contact form details."""
    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASS")

    BASE_DIR = Path(__file__).resolve().parent.parent  # goes up to your project root
    TEMPLATE_DIR = BASE_DIR / "templates"

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("email_template.html")

    # Render the template with contact data
    html_body = template.render(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        subject=contact.subject,
        message=contact.message,
        timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    # Plain-text fallback
    plain_body = f"""
    New message from {contact.name}

    Email: {contact.email}
    Phone: {contact.phone}
    Subject: {contact.subject}

    Message:
    {contact.message}
    """

    # Build email message
    msg = EmailMessage()
    msg["From"] = f"🌐 Portfolio<{sender}>"
    msg["To"] = receiver
    msg["Subject"] = f"📩 New Contact Message: {contact.subject}"

    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    # Send the email
    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=sender,
        password=password,
    )


async def send_otp_email(email: str, otp: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg["From"] = f"🌐 My Portfolio <{sender}>"
    msg["To"] = email
    msg["Subject"] = "🔐 Your OTP Verification Code"

    msg.set_content(f"Your OTP for verification is: {otp}\n\nIt will expire in 5 minutes.")

    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=sender,
        password=password,
    )