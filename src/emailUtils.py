import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from logger import get_logger

logger = get_logger(__name__)

def send_email_with_attachment(sender_email, app_password, recipient_email, subject, body, attachment_path):
    logger.info(f"Sending email with attachment to {recipient_email}...")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(attachment_path)}",
    )

    message.attach(part)
    text = message.as_string()

    # Log in to SMTP server and send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, text)
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Error occurred while sending email: {e}")
