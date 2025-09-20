from flask import Flask, request, jsonify
from config import Config
from utils.email_sender import mail, send_invitation_email
from utils.pdf_generator import create_invitation_pdf, protect_pdf
from utils.santa_logic import generate_secret_santa

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)

@app.route('/send-invitations', methods=['POST'])
def send_invitations():
    data = request.get_json()
    participants = data.get("participants", [])
    organizer_email = data.get("organizer_email")

    if not participants or len(participants) < 2:
        return jsonify({"error": "Se necesitan al menos 2 participantes"}), 400

    if not organizer_email:
        return jsonify({"error": "Se necesita un correo electrónico del organizador"}), 400

    # 🔀 Generar sorteo seguro
    pairs = generate_secret_santa(participants)

    pdf_buffers = []
    for participant in participants:
        name = participant["name"]
        receiver = pairs[name]

        # Crear PDF
        pdf = create_invitation_pdf(
            name=name,
            receiver=receiver,
            event_name="Evento familiar de intercambio de Navidad 🎄",
            location="Casa de los abuelos",
            min_amount=20
        )

        # Proteger PDF con contraseña = nombre del participante
        protected_pdf = protect_pdf(pdf, password=name)
        pdf_buffers.append((f"Invitacion_{name}.pdf", protected_pdf))

    # HTML del correo
    html_template = f"""
    <div style="font-family: 'Helvetica', sans-serif; color: #333; background-color: #fff3e0; padding: 20px; border-radius: 15px;">
        <h1 style="color: #ff6f00; text-align: center;">¡Hola! 🎁</h1>
        <p style="font-size: 16px;">Se han generado las invitaciones para el evento. Cada PDF tiene contraseña con el nombre del destinatario.</p>
        <p style="font-size: 16px;">Reenvía las invitaciones a cada participante correspondiente.</p>
    </div>
    """

    # Enviar correo al organizador con todos los PDFs
    for filename, pdf_buffer in pdf_buffers:
        send_invitation_email(
            recipients=[organizer_email],
            subject="Invitaciones Giftly 🎁",
            body_html=html_template,
            pdf_buffer=pdf_buffer,
            filename=filename
        )

    return jsonify({"status": "success", "sent_to": organizer_email}), 200

if __name__ == "__main__":
    app.run(debug=True)