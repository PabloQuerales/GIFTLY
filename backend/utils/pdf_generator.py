from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter
import io
import random

# TAMAÑO REDISEÑADO: A5 (595 x 420 puntos)
A5_VERTICAL = (419.53, 350 ) 
POSTCARD = A5_VERTICAL

# Definimos nuestra paleta de colores para consistencia
COLOR_PRIMARY = colors.HexColor("#ff6f61") # Rojo/Coral
COLOR_ACCENT = colors.HexColor("#ffd54f") # Amarillo/Oro
COLOR_BACKGROUND = colors.HexColor("#fffdf7") # Marfil Suave
COLOR_TEXT_DARK = colors.HexColor("#333333") # Texto oscuro

# RUTA DEL LOGO (CORREGIDA para ser accedida desde app.py)
LOGO_PATH = "utils/g-logo.png"

def create_invitation_pdf(name, receiver, event_name, location, min_amount,organizer_name):
    """
    Genera una invitación en formato A5 (Media Carta), elegante y ampliada.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=POSTCARD)

    width, height = POSTCARD

    # Fondo color marfil suave
    c.setFillColor(COLOR_BACKGROUND)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # 🎀 Marco decorativo más grueso y elegante
    c.setStrokeColor(COLOR_PRIMARY)
    c.setLineWidth(6) # Marco un poco más grueso por el tamaño A5
    c.rect(0.5*cm, 0.5*cm, width - 1.0*cm, height - 1.0*cm)

    # 🎉 Confeti de Esquina Controlado 
    c.setFillColor(COLOR_ACCENT)
    confetti_points = [
        (width - 2.0*cm, height - 2.0*cm, 4), # Puntos un poco más grandes
        (width - 1.2*cm, height - 3.0*cm, 3),
        (width - 3.5*cm, height - 1.5*cm, 3),
    ]
    for x, y, size in confetti_points:
        c.circle(x, y, size, fill=1, stroke=0)
    
    # 🌟 DIBUJAR EL LOGO (Posición ajustada al nuevo tamaño)
    try:
        LOGO_WIDTH = 2.0 * cm  # <-- Nuevo Ancho: 4.0 cm
        LOGO_HEIGHT = 6.0 * cm # <-- Altura inicial (puedes dejar esta o ajustarla si quieres forzar un tamaño)
        ADJUSTMENT =  2.0 * cm
        X_POS = 0.8 * cm 
        Y_POS = height - 1.0 * cm - LOGO_HEIGHT + ADJUSTMENT 
        
        c.drawImage(LOGO_PATH, X_POS, Y_POS, width=LOGO_WIDTH, height=LOGO_HEIGHT, mask='auto', preserveAspectRatio=True)
        
    except (FileNotFoundError, OSError): # Capturamos OSError en caso de problemas con Reportlab/ruta
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(COLOR_PRIMARY)
        c.drawString(1.0 * cm, height - 1.5 * cm, "Giftly")
        
    # --- Bloque de Información ---

    # Título principal (Evento)
    c.setFont("Helvetica-Bold", 40) # Fuente más grande
    c.setFillColor(COLOR_PRIMARY)
    c.drawCentredString(width / 2, height - 3.5 * cm, f"{name}") 

    # Nombre del invitado (Protagonista)
    c.setFont("Helvetica", 12) # Fuente más grande
    c.setFillColor(COLOR_TEXT_DARK)
    c.drawCentredString(width / 2, height - 4.3 * cm, f"Has sido invitado/a por {organizer_name} a un intercambio de regalos ")
    
    # Línea separadora centrada
    c.setStrokeColor(COLOR_PRIMARY)
    c.setLineWidth(1.5)
    c.line(width / 2 - 6*cm, height - 5.2*cm, width / 2 + 6*cm, height - 5.2*cm)


    # --- Detalles del Evento (Izquierda) ---
    
    Y_START_DETAIL = height - 6.2 * cm # Punto de inicio movido hacia abajo

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(COLOR_TEXT_DARK)
    c.drawString(2 * cm, Y_START_DETAIL, "Te contamos más:")
    c.drawString(2 * cm, Y_START_DETAIL - 1 * cm, f"{event_name}")
    c.drawString(2 * cm, Y_START_DETAIL - 2 * cm, f"{location}")
    c.drawString(2 * cm, Y_START_DETAIL - 3 * cm, f"{min_amount}€")
    
    c.setFont("Helvetica", 9)
    c.drawString(2 * cm, Y_START_DETAIL - 0.5 * cm, f"El motivo es:")
    c.drawString(2 * cm, Y_START_DETAIL - 1.5 * cm, f"Será en:")
    c.drawString(2 * cm, Y_START_DETAIL - 2.5 * cm, f"El monto máximo del regalo:")


    # --- Receptor del Regalo (Derecha - Mayor Énfasis) ---
    
    # Recuadro de destaque para el receptor (Ajustado al nuevo tamaño)
    BOX_WIDTH = 6.0 * cm
    BOX_HEIGHT = 3.5 * cm
    X_BOX_START = width - 1 * cm - BOX_WIDTH
    Y_BOX_START = Y_START_DETAIL - BOX_HEIGHT + 0.3 * cm
    
    # Fondo suave del recuadro
    c.setStrokeColor(COLOR_ACCENT)
    c.rect(X_BOX_START, Y_BOX_START, BOX_WIDTH, BOX_HEIGHT, stroke=1, fill=0)
    
    # Título del Recuadro
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(COLOR_TEXT_DARK)
    c.drawCentredString(X_BOX_START + BOX_WIDTH/2, Y_BOX_START + BOX_HEIGHT - 0.7 * cm, "Te tocó regalarle a:")

    # Nombre del Receptor 
    c.setFont("Helvetica-Bold", 38) # Fuente más grande e impactante
    c.setFillColor(COLOR_PRIMARY) 
    c.drawCentredString(X_BOX_START + BOX_WIDTH/2, Y_BOX_START + 1.2 * cm, f"{receiver}")

    # Footer de Seguridad (Posición ajustada)
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#7d7d7d"))
    c.drawCentredString(width / 2, 1.2 * cm, "Archivo cifrado con tu nombre: Garantizamos la privacidad. Enviado por Giftly.")

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