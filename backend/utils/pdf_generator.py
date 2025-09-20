from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
import io

def create_invitation_pdf(name, receiver, event_name, location, min_amount):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # 🔹 Página 1: Portada con nombre del invitado
    c.setFillColor(colors.HexColor("#ff6f00"))  # color mostaza
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 5*cm, f"{name}")
    c.setFont("Helvetica", 24)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width/2, height - 6*cm, "¡Estás invitado a Giftly! 🎁")

    # Decoración de portada
    c.setFillColor(colors.HexColor("#fce4ec"))  # rosa suave
    for y in range(int(height - 7*cm), int(height - 10*cm), -20):
        c.circle(width/2, y, 10, fill=1, stroke=0)

    c.showPage()

    # 🔹 Página 2: Detalles del evento
    c.setFillColor(colors.HexColor("#ff6f00"))
    c.setFont("Helvetica-Bold", 26)
    c.drawString(2*cm, height - 3*cm, event_name)

    c.setFont("Helvetica", 18)
    c.setFillColor(colors.black)
    c.drawString(2*cm, height - 5*cm, f"Lugar: {location}")
    c.drawString(2*cm, height - 6*cm, f"Monto mínimo del regalo: {min_amount}€")
    c.drawString(2*cm, height - 7*cm, f"Participantes: {name} → {receiver}")

    # Decoración lateral
    c.setFillColor(colors.HexColor("#ffe082"))  # mostaza suave
    for i in range(5):
        c.rect(width - 3*cm, height - (3+i)*cm, 1*cm, 1*cm, fill=1, stroke=0)

    c.showPage()

    # 🔹 Página 3: Receptor del regalo
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.HexColor("#ff6f00"))
    c.drawString(2*cm, height - 3*cm, "¡Te ha tocado regalar a:")

    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(colors.HexColor("#1976d2"))  # azul para receptor
    c.drawCentredString(width/2, height - 6*cm, receiver)

    # Decoración: emojis navideños
    emojis = ["🎄", "🎁", "✨", "❄️"]
    for i, emoji in enumerate(emojis):
        c.setFont("Helvetica-Bold", 36)
        c.drawString(2*cm + i*3*cm, 2*cm, emoji)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def protect_pdf(pdf_buffer, password):
    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    protected_buffer = io.BytesIO()
    writer.write(protected_buffer)
    protected_buffer.seek(0)
    return protected_buffer