from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET",])
def hello():
    return jsonify({"message" : "Hello"})

@app.route("/upload", methods=["POST"])
def upload():
    token = request.headers.get('token')
    
    email = request.form.get("email")
    file = request.files.get("arquivo")
    if file is None:
        return "Nenhum arquivo enviado", 400

    
    file.save("./static/" + file.filename)

    mutation(token, email, file.filename)

    os.remove("./static/" + file.filename)
    return "Success", 500

def mutation(token, email, file):
    url = "https://api.autentique.com.br/v2/graphql"
    payload = {
        'operations': '{"query":"mutation CreateDocumentMutation($document: DocumentInput!, $signers: [SignerInput!]!, $file: Upload!) {createDocument(document: $document, signers: $signers, file: $file) {id name refusable sortable created_at signatures { public_id name email created_at action { name } link { short_link } user { id name email }}}}", "variables":{"document": {"name": "Contrato Mentor"},"signers": [{"email": "' + email + '","action": "SIGN"}],"file":null}}',
        'map': '{"file": ["variables.file"]}'
    }
    files = [
        ('file',open('/static/' + file, 'rb'))
    ]
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text


if __name__ == "__main__":
    app.run()