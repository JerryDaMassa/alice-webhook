from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("Dados Alice")
sheet = spreadsheet.worksheet("Página1")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    nome = data.get("nome")
    telefone = data.get("telefone")
    cidade = data.get("cidade")

    if not nome or not telefone or not cidade:
        return jsonify({"status": "erro", "mensagem": "Faltam dados"}), 400

    sheet.append_row([nome, telefone, cidade])
    return jsonify({"status": "sucesso", "mensagem": "Dados salvos com sucesso"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)