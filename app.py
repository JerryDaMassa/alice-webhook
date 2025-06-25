from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import os

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
json_creds = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
client = gspread.authorize(creds)

# Nome da planilha e aba
spreadsheet = client.open("Dados Alice")
sheet = spreadsheet.worksheet("Página1")

@app.route("/", methods=["POST"])
def receber_dados():
    data = request.json
    nome = data.get("nome", "")
    telefone = data.get("telefone", "")
    cidade = data.get("cidade", "")
    
    # Adiciona nova linha na planilha
    sheet.append_row([nome, telefone, cidade])
    return {"status": "sucesso"}

if __name__ == "__main__":
    app.run(debug=True)
