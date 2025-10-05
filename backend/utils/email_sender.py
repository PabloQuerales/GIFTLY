from flask_mail import Message, Mail
from io import BytesIO

mail = Mail()

def send_invitation_email(recipients, subject, body_html, attachments=None):
    msg = Message(subject, recipients=recipients)
    msg.html = body_html

    if attachments:
        for filename, pdf_buffer in attachments:
            if isinstance(pdf_buffer, BytesIO):
                msg.attach(
                    filename,
                    "application/pdf",
                    pdf_buffer.getvalue()
                )

    mail.send(msg)