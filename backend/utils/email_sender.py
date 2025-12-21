import os
import base64
import logging
from io import BytesIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDGRID_SENDER_EMAIL")  # debe estar verificado en SendGrid


def send_invitation_email(recipients, subject, body_html, attachments=None):
    if not SENDGRID_API_KEY or not SENDER_EMAIL:
        raise RuntimeError("Faltan variables SENDGRID_API_KEY o SENDGRID_SENDER_EMAIL")

    message = Mail(
        from_email=Email(SENDER_EMAIL),
        to_emails=[To(email) for email in recipients],
        subject=subject,
        html_content=body_html
    )

    # Adjuntar PDFs
    if attachments:
        for filename, pdf_buffer in attachments:
            if isinstance(pdf_buffer, BytesIO):
                encoded_file = base64.b64encode(pdf_buffer.getvalue()).decode()

                attachment = Attachment(
                    FileContent(encoded_file),
                    FileName(filename),
                    FileType("application/pdf"),
                    Disposition("attachment")
                )
                message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"Email enviado con SendGrid. Status: {response.status_code}")
    except Exception as e:
        logging.error("Error enviando email con SendGrid", exc_info=True)
        raise