import json
import logging
import settings
import utils

class StatusHandler:
    def __init__(self, status_db_path):
        self.__status_db_location = status_db_path
        logging.info("Status DB initialized to {}".format(status_db_path))

    def add_status_object(self, object_name, file_hash):
        data = {'name': object_name,
                'fileHash': file_hash,
                'converted': False,
                'encrypted': False,
                'transferred': False
                }
        add_status = False
        with open("{0}/{1}".format(self.__status_db_location, object_name), "w") as statusObj:
            json.dump(data, statusObj)
            logging.debug("Created status object for {0}/{1}".format(self.__status_db_location, object_name))
            add_status = True
        return add_status

    def __get_status_object(self, object_name):
        status = None
        try:
            with open("{0}/{1}".format(self.__status_db_location, object_name), "r") as statusObj:
                status = json.load(statusObj)
                if status["name"] == object_name \
                   and status["fileHash"] != utils.hash_file("{0}/{1}".format(settings.INPUT_DIR, object_name)):
                    status = None
        except IOError as err:
            logging.debug("{0}/{1} does not exist. New object will be created.".format(self.__status_db_location,
                                                                                       object_name))
        return status

    def update_status_object(self, object_name, field, value):
        update_status = False
        with open("{0}/{1}".format(self.__status_db_location, object_name), "r") as statusObj:
            status = json.load(statusObj)
        status[field] = value
        with open("{0}/{1}".format(self.__status_db_location, object_name), "w") as statusObj:
            json.dump(status, statusObj)
            update_status = True
            logging.debug("{0}/{1} object is updated to {2}".format(self.__status_db_location, object_name, status))
        return update_status

    def is_new(self, file):
        if (self.__get_status_object(file) is None
                or (not self.__get_status_object(file)["converted"]
                    and not self.__get_status_object(file)["encrypted"]
                    and not self.__get_status_object(file)["transferred"])):
            return True
        else:
            return False

    def is_converted(self, file):
        if self.__get_status_object(file) is not None and self.__get_status_object(file)["converted"]:
            return True
        else:
            return False

    def is_encrypted(self, file):
        if self.__get_status_object(file) is not None \
                and self.__get_status_object(file)["converted"] \
                and self.__get_status_object(file)["encrypted"]:
            return True
        else:
            return False

    def is_transferred(self, file):
        if self.__get_status_object(file) is not None \
                and self.__get_status_object(file)["converted"] \
                and self.__get_status_object(file)["encrypted"] \
                and self.__get_status_object(file)["transferred"]:
            return True
        else:
            return False

