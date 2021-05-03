from encrypter import Encrypter
from statusHandler import StatusHandler
import os
import settings
import time
import utils

status = StatusHandler(settings.STATUS_DB_PATH)
enc = Encrypter(settings.ENCRYPTION_KEY)


def run_scan():
    """
    This method is called in a loop to scan the input directory for .json files.
    When a .json file is found, it will check if it has been converted to xml, encrypted and transferred to
    remote server already.
    State of each processed file is recorded and managed by the StatusHandler object.
    It will not process an already processed file.
    If a file is modified, StatusHandler will recognize the updated file based on a file hash, then convert to xml,
    encrypt and re-transmit.
    Logic is built into the StatusHandler to identify when conversion, encryption and transfer process is interrupted.
    This method can resume the flow from the interrupted point in the next cycle for a given json file.
    :return: None
    """
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
    """
    __main__ method for sender.
    """
    while True:
        run_scan()
        time.sleep(int(settings.SCAN_INTERVAL))
