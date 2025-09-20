from flask_mail import Message, Mail

mail = Mail()

def send_invitation_email(recipients, subject, body_html, pdf_buffer, filename):
    msg = Message(subject, recipients=recipients)
    msg.html = body_html
    msg.attach(filename, "application/pdf", pdf_buffer.read())
    mail.send(msg)
