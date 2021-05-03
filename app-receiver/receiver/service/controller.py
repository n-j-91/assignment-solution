from flask import Flask, request, jsonify
from .decrypter import Decrypter
from . import settings

app = Flask("receiver")
dec = Decrypter(settings.DECRYPTION_KEY)


@app.route("/", methods=["GET"])
def health_check():
    data = {"msg": "Server is healthy", "status_code": 200}
    return jsonify(data), 200


@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    save_location = "{0}/{1}.xml".format(settings.OUTPUT_DIR, filename)
    uploaded_file = request.files['file']
    dec.decrypt(uploaded_file.read(), save_location)
    data = {"msg": "File is decrypted and saved to {0}".format(save_location), "status_code": 201}
    return jsonify(data), 201
