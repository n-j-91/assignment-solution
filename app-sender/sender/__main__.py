from encrypter import Encrypter
from statusHandler import StatusHandler
import os
import settings
import time
import utils

status = StatusHandler(settings.STATUS_DB_PATH)
enc = Encrypter(settings.ENCRYPTION_KEY)


def run_scan():
    for file in os.listdir(settings.INPUT_DIR):
        if file.endswith(".json"):
            file_prefix = file.split(".")[0]
            if status.is_new(file):
                status.add_status_object(file, utils.hash_file("{0}/{1}".format(settings.INPUT_DIR, file)))
                utils.convert_to_xml(status, "{0}/{1}".format(settings.INPUT_DIR, file))
            if status.is_converted(file) and not status.is_encrypted(file):
                utils.encrypt_xml(status,
                                  enc,
                                  "{0}/{1}.xml".format(settings.INPUT_DIR, file_prefix),
                                  file)
            if status.is_encrypted(file) and not status.is_transferred(file):
                utils.upload_to_server(status,
                                       settings.RECEIVER_ADDRESS,
                                       settings.RECEIVER_PORT,
                                       settings.RECEIVER_URI,
                                       "{0}/{1}.xml.enc".format(settings.INPUT_DIR, file_prefix),
                                       file_prefix,
                                       file)


if __name__ == "__main__":
    while True:
        run_scan()
        time.sleep(int(settings.SCAN_INTERVAL))
