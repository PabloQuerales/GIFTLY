from flask import Flask, request, jsonify
from config import Config
from utils.email_sender import send_invitation_email
from utils.pdf_generator import create_invitation_pdf, protect_pdf
from utils.santa_logic import generate_secret_santa
from flask_cors import CORS
import json
import logging
import traceback
import os
from threading import Thread

app = Flask(__name__)

# Configuración CORS
allowed_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS", 
    "http://localhost:5173,https://giftly-zeta.vercel.app"
).split(",")
CORS(app, origins=allowed_origins, supports_credentials=True)

logging.basicConfig(level=logging.INFO)

# Función que realiza la lógica pesada en background
def async_send_invitations(data):
    try:
        # ⚡ IMPORTANTE: crear contexto de Flask para poder usar Flask-Mail
        with app.app_context():
            participantsName = data.get("participantsName", [])
            organizer_email = data.get("organizer_email")
            organizer_name = data.get("organizer_name")
            event_name = data.get("event_name", "Evento Giftly")
            location = data.get("location", "Lugar no especificado")
            event_type = data.get("event_type", None)
            min_amount = data.get("min_amount", 20)

            # Normalizar participantsName si viene como string JSON
            if isinstance(participantsName, str):
                try:
                    participantsName = json.loads(participantsName)
                except Exception:
                    logging.error("participantsName debe ser un array JSON o lista de objetos")
                    return

            # Validación básica
            if not participantsName or len(participantsName) < 2 or not organizer_email:
                logging.error("Datos insuficientes para generar invitaciones")
                return

            # Normalizar participantes
            normalized = []
            for idx, p in enumerate(participantsName):
                if isinstance(p, dict) and "name" in p and p["name"]:
                    normalized.append({"name": str(p["name"]), "id": p.get("id")})
                else:
                    logging.error(f"Participante inválido en índice {idx}")
            participantsName = normalized

            # Generar sorteo
            pairs = generate_secret_santa(participantsName)

            # Crear PDFs protegidos
            pdf_buffers = []
            for participant in participantsName:
                name = participant["name"]
                receiver = pairs[name]
                pdf = create_invitation_pdf(
                    name=name,
                    receiver=receiver,
                    event_name=event_name,
                    location=location,
                    min_amount=min_amount,
                    organizer_name=organizer_name
                )
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
                <p>Tu evento <strong>{event_name}</strong> está listo 🎉</p>
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
                    <strong>Lugar:</strong> {location}
                </p>
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
            # Enviar correo
            send_invitation_email(
                recipients=[organizer_email],
                subject=f"Invitaciones Giftly 🎁 - {event_name}",
                body_html=html_template,
                attachments=pdf_buffers
            )
            logging.info(f"Invitaciones enviadas a {organizer_email} ({len(pdf_buffers)} PDFs)")

    except Exception as e:
        logging.error("Error en async_send_invitations: %s", traceback.format_exc())

@app.route("/ping")
def ping():
    return "pong", 200

@app.route('/send-invitations', methods=['POST', 'OPTIONS'])
def send_invitations():
    # Responder preflight OPTIONS
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Request must be JSON and Content-Type: application/json"}), 400

        # Lanzar la tarea en background
        Thread(target=async_send_invitations, args=(data,), daemon=True).start()

        # Responder inmediatamente
        return jsonify({
            "status": "queued",
            "message": "Las invitaciones se están procesando en segundo plano"
        }), 200

    except Exception as e:
        logging.error("Error en /send-invitations: %s", traceback.format_exc())
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
