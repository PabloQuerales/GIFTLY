from flask import Flask, request, jsonify
from config import Config
from utils.email_sender import mail, send_invitation_email
from utils.pdf_generator import create_invitation_pdf, protect_pdf
from utils.santa_logic import generate_secret_santa
from flask_cors import CORS
import json
import logging
import traceback
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
mail.init_app(app)

logging.basicConfig(level=logging.INFO)

with open("static/logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

logo_html = f'<img src="data:image/png;base64,{encoded_logo}" alt="Giftly" style="width:120px; height:auto; margin-bottom:20px;">'

@app.route('/send-invitations', methods=['POST'])
def send_invitations():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Request must be JSON and Content-Type: application/json"}), 400

        # Extraer campos
        participantsName = data.get("participantsName", [])
        organizer_email = data.get("organizer_email")
        organizer_name = data.get("organizer_name")
        event_name = data.get("event_name", "Evento Giftly")
        location = data.get("location", "Lugar no especificado")
        event_type = data.get("event_type", None)
        min_amount = data.get("min_amount", 20)  # opcional

        # Robustez: si participantsName llegó como string JSON
        if isinstance(participantsName, str):
            try:
                participantsName = json.loads(participantsName)
            except Exception:
                return jsonify({"error": "participantsName debe ser un array JSON o lista de objetos"}), 400

        # Validaciones
        if not isinstance(participantsName, list) or len(participantsName) < 2:
            return jsonify({"error": "Se necesitan al menos 2 participantes en participantsName"}), 400

        if not organizer_email:
            return jsonify({"error": "Se necesita un correo electrónico del organizador (organizer_email)"}), 400

        # Normalizar: asegurar que cada participante tenga 'name'
        normalized = []
        for idx, p in enumerate(participantsName):
            if isinstance(p, dict) and "name" in p and p["name"]:
                normalized.append({"name": str(p["name"]), "id": p.get("id")})
            else:
                return jsonify({"error": f"Cada participante debe ser un objeto con clave 'name' (error en índice {idx})"}), 400

        participantsName = normalized

        # Generar sorteo seguro
        pairs = generate_secret_santa(participantsName)

        # Crear PDFs y protegerlos
        pdf_buffers = []
        for participant in participantsName:
            name = participant["name"]
            receiver = pairs[name]

            pdf = create_invitation_pdf(
                name=name,
                receiver=receiver,
                event_name=event_name,
                location=location,
                min_amount=min_amount
            )

            protected_pdf = protect_pdf(pdf, password=name)
            pdf_buffers.append((f"Invitacion_{name}.pdf", protected_pdf))

        # Mantener el mismo HTML y estilos que tenías antes
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
            {logo_html}
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

        # Enviar correo al organizador con todos los PDFs adjuntos
        send_invitation_email(
            recipients=[organizer_email],
            subject=f"Invitaciones Giftly 🎁 - {event_name}",
            body_html=html_template,
            attachments=pdf_buffers
        )

        return jsonify({"status": "success", "sent_to": organizer_email, "count": len(pdf_buffers)}), 200

    except Exception as e:
        logging.error("Error en /send-invitations: %s", traceback.format_exc())
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)