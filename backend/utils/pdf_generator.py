# utils/pdf_generator.py
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
import io
import random

# Tamaño postal: 6x4 pulgadas
POSTCARD = (6 * 72, 4 * 72)  # 432 x 288 puntos

def create_invitation_pdf(name, receiver, event_name, location, min_amount):
    """
    Genera una invitación en formato postal (6x4 pulgadas, horizontal).
    Estilo tipo tarjeta regalo (con marco decorativo y detalles festivos).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=POSTCARD)

    width, height = POSTCARD

    # Fondo color marfil
    c.setFillColor(colors.HexColor("#fffdf7"))
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # 🎀 Marco decorativo
    c.setStrokeColor(colors.HexColor("#ff6f61"))
    c.setLineWidth(3)
    c.rect(0.4*cm, 0.4*cm, width - 0.8*cm, height - 0.8*cm)

    # 🎉 Detalles tipo confeti (esquinas)
    c.setFillColor(colors.HexColor("#ffd54f"))  # amarillo suave
    for i in range(20):
        x = random.randint(10, int(width-10))
        y = random.randint(10, int(height-10))
        c.circle(x, y, 2, fill=1, stroke=0)

    # Nombre del invitado (protagonista)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.HexColor("#ff6f61"))
    c.drawCentredString(width / 2, height - 1.5 * cm, f"{name}")

    # Subtítulo
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width / 2, height - 2.5 * cm, "¡Estás invitado a Giftly! 🎁")

    # Línea separadora
    c.setStrokeColor(colors.HexColor("#ff6f61"))
    c.setLineWidth(1.5)
    c.line(1*cm, height - 3.2*cm, width - 1*cm, height - 3.2*cm)

    # Detalles del evento (lado izquierdo)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.black)
    c.drawString(1.2 * cm, height - 4.4 * cm, event_name)

    c.setFont("Helvetica", 9)
    c.drawString(1.2 * cm, height - 5.2 * cm, f"Lugar: {location}")
    c.drawString(1.2 * cm, height - 5.8 * cm, f"Monto mínimo: {min_amount}€")

    # Receptor del regalo (lado derecho destacado)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#1976d2"))
    c.drawRightString(width - 1.2 * cm, height - 4.8 * cm, f"Debes regalar a: {receiver}")

    # Footer
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.HexColor("#7d7d7d"))
    c.drawCentredString(width / 2, 0.9 * cm, "Archivo cifrado: solo el destinatario debe abrirlo")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def protect_pdf(pdf_buffer, password):
    """
    Protege con contraseña un io.BytesIO que contiene un PDF.
    Devuelve un nuevo io.BytesIO protegido.
    """
    try:
        pdf_buffer.seek(0)
    except Exception:
        pass

    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    protected_buffer = io.BytesIO()
    writer.write(protected_buffer)
    protected_buffer.seek(0)
    return protected_buffer