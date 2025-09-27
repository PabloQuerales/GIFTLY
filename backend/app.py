from flask import Flask, request, jsonify
from config import Config
from utils.email_sender import mail, send_invitation_email
from utils.pdf_generator import create_invitation_pdf, protect_pdf
from utils.santa_logic import generate_secret_santa
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
mail.init_app(app)

@app.route('/send-invitations', methods=['POST'])
def send_invitations():
    data = request.get_json()
    participantsName = data.get("participantsName", [])
    organizer_email = data.get("organizer_email")
    organizer_name = data.get("organizer_name")

    if not participantsName or len(participantsName) < 2:
        return jsonify({"error": "Se necesitan al menos 2 participantes"}), 400

    if not organizer_email:
        return jsonify({"error": "Se necesita un correo electrónico del organizador"}), 400

    # 🔀 Generar sorteo seguro
    pairs = generate_secret_santa(participantsName)

    pdf_buffers = []
    for participant in participantsName:
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
    <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 0;
            }}
            .container {{
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            padding: 30px;
            text-align: center;
            }}
            h1 {{
            color: #ff6f61;
            }}
            h2 {{
            color: #333333;
            font-size: 20px;
            margin-top: 25px;
            }}
            p {{
            font-size: 16px;
            color: #333333;
            line-height: 1.5;
            }}
            ul {{
            text-align: left;
            margin: 20px auto;
            max-width: 400px;
            padding-left: 0;
            list-style-position: inside;
            }}
            li {{
            margin-bottom: 10px;
            color: #555555;
            }}
            .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #999999;
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <h1>Hola {organizer_name}!</h1>
            <p>Tu evento está listo 🎉</p>
            <p>
                Adjunto a este correo encontrarás las invitaciones en formato PDF para cada uno de los participantes.
                Ahora te corresponde a ti, como organizador, hacerles llegar sus respectivas invitaciones.
            </p>

            <h2>Instrucciones Importantes</h2>
            <ul>
                <li>
                    Cada archivo PDF está **cifrado con el nombre del participante**. Esto significa que solo la persona a la que le envíes el archivo podrá abrirlo sin problemas, garantizando la privacidad de los resultados.
                </li>
                <li>
                    Asegúrate de enviar a cada participante **únicamente su invitación**. Así evitamos confusiones y que alguien pueda abrir una invitación por error.
                </li>
            </ul>

            <p>
                Una vez que todos reciban su invitación, podrán descubrir a quién deben regalar.
            </p>
            <p>Te deseamos mucho éxito con tu evento y esperamos que todos lo disfruten.🎁</p>

            <div class="footer">
                <p>Enviado con ❤️ por Giftly</p>
            </div>
        </div>
        </body>
        </html>
            """

# Enviar un único correo al organizador con TODOS los PDFs adjuntos
    send_invitation_email(
        recipients=[organizer_email],
        subject="Invitaciones Giftly 🎁",
        body_html=html_template,
        attachments=pdf_buffers  # 👈 ahora pasamos la lista de (filename, pdf_buffer)
    )

    return jsonify({"status": "success", "sent_to": organizer_email}), 200

if __name__ == "__main__":
    app.run(debug=True)