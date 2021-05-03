from json2xml import json2xml
from json2xml.utils import readfromjson

import hashlib
import logging
import requests
import os


def hash_file(path_to_file):
    """
    This method can find the hash value for a given file.
    :param path_to_file: Path to file
    :return: hash value
    """
    h = hashlib.sha1()
    with open(path_to_file, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


def convert_to_xml(status, path_to_jsonfile):
    """
    This method will convert a given json file to a xml file.
    :param status: StatusHandler object
    :param path_to_jsonfile: Path to jsonfile
    :return: Path to converted xml file
    """
    data = readfromjson(path_to_jsonfile)
    path_to_xmlfile = None
    with open("{0}/{1}.xml".format(os.path.dirname(path_to_jsonfile),
                                   os.path.basename(path_to_jsonfile).split('.')[0]), "w") as xmlfile:
        xmlfile.write(json2xml.Json2xml(data).to_xml())
        status.update_status_object(os.path.basename(path_to_jsonfile), "converted", True)
        path_to_xmlfile = xmlfile.name
        logging.info("{0} is converted to {1}".format(path_to_jsonfile, xmlfile.name))
    return path_to_xmlfile


def encrypt_xml(status, enc, path_to_xmlfile, jsonfilename):
    """
    Encrypts a given file.
    :param status: StatusHandler object
    :param enc: Encrypter object
    :param path_to_xmlfile: Path to a file.
    :param jsonfilename: Json file name (equal to json object name in StatusHandler)
    :return: None
    """
    enc.encrypt_file(path_to_xmlfile, "{0}.enc".format(path_to_xmlfile))
    status.update_status_object(jsonfilename, "encrypted", True)
    logging.info("{0} is encrypted to {1}.enc".format(jsonfilename, path_to_xmlfile))


def upload_to_server(status, hostname, port, uri, path_to_file, filename, jsonfilename):
    """
    Upload a given file to a remote server.
    :param status: StatusHandler object.
    :param hostname: Remote server hostname / IP.
    :param port: Listening port of the remote server.
    :param uri: Upload URI of the remote server.
    :param path_to_file: File to upload.
    :param filename: File name for the file being uploaded.
    :param jsonfilename: Json file name (equal to json object name in StatusHandler)
    :return: None
    """
    full_uri = "http://{0}:{1}{2}/{3}".format(hostname, port, uri, filename)
    headers = {
        "Content-Type": "multipart/form-data"
    }
    response = None
    with open(path_to_file, "rb") as encryptedData:
        try:
            response = requests.post(url=full_uri, files=dict(file=encryptedData))
            if response.status_code == 201:
                logging.info("{0} is uploaded successfully. Response from server: {1}".format(filename,
                                                                                              response.json()["msg"]))
                status.update_status_object(jsonfilename, "transferred", True)
        except Exception as err:
            logging.error("Unable to upload file. msg: {}".format(err))