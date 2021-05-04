from flask import Flask, request, jsonify
from .decrypter import Decrypter
from . import settings

app = Flask("receiver")
dec = Decrypter(settings.DECRYPTION_KEY)


@app.route("/", methods=["GET"])
def health_check():
    """
    Requests sent to / (root) are handled by this method.
    Considered as a health check endpoint for the application.
    :return: A tuple with json data and status_code
    """
    data = {"msg": "Server is healthy", "status_code": 200}
    return jsonify(data), 200


@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    """
    Requests sent to /upload/<filename> are handled by this method.
    Content-type handled by this rest api method is multipart/form-data.
    Request should contain file data ( data of an encrypted xml ).

    Hint: app-sender/sender/utils.upload_to_server(**args) method calls
    this method over rest api to upload the file.

    :param filename: Path parameter containing a filename
    :return: A tuple with json data and status_code
    """
    save_location = "{0}/{1}.xml".format(settings.OUTPUT_DIR, filename)
    uploaded_file = request.files['file']
    dec.decrypt(uploaded_file.read(), save_location)
    data = {"msg": "File is decrypted and saved to {0}".format(save_location), "status_code": 201}
    return jsonify(data), 201
