import json
import logging
import settings
import utils

class StatusHandler:
    """
    StatusHandler acts as a simple json objects store for state handling of processed json files.
    """
    def __init__(self, status_db_path):
        """
        Constructor for StatusHandler object.
        When declaring, provide a path to store json objects.
        :param status_db_path: Path to json objects.
        """
        self.__status_db_location = status_db_path
        logging.info("Status DB initialized to {}".format(status_db_path))

    def add_status_object(self, object_name, file_hash):
        """
        Create a new json object for a given json file.
        :param object_name: Json file name(equal to json object name).
        :param file_hash: Json file hash
        :return: True if creationg of json object is successful.
        """
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
        """
        Retrieve the json object for a json file.
        :param object_name: Name of the json file (equal to json object name).
        :return: Dictionary type object containing the state of a json file.
        """
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
        """
        Update status of a json object.
        :param object_name: Json file name (equal to json object name).
        :param field: Field to update.
        :param value: Value for the field being updated.
        :return: True if update is successful.
        """
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
        """
        Check if a given json file is new.
        :param file: Json file name (equal to json object name)
        :return: True if file is new.
        """
        if (self.__get_status_object(file) is None
                or (not self.__get_status_object(file)["converted"]
                    and not self.__get_status_object(file)["encrypted"]
                    and not self.__get_status_object(file)["transferred"])):
            return True
        else:
            return False

    def is_converted(self, file):
        """
        Check if given json file is converted to xml already.
        :param file: Json file name (equal to json object name)
        :return: True if file is converted already.
        """
        if self.__get_status_object(file) is not None and self.__get_status_object(file)["converted"]:
            return True
        else:
            return False

    def is_encrypted(self, file):
        """
        Check if given json file is encrypted to xml already.
        :param file: Json file name (equal to json object name)
        :return: True if file is encrypted already.
        """
        if self.__get_status_object(file) is not None \
                and self.__get_status_object(file)["converted"] \
                and self.__get_status_object(file)["encrypted"]:
            return True
        else:
            return False

    def is_transferred(self, file):
        """
        Check if given json file is transferred to remote server already.
        :param file: Json file name (equal to json object name)
        :return: True if file is encrypted already.
        """
        if self.__get_status_object(file) is not None \
                and self.__get_status_object(file)["converted"] \
                and self.__get_status_object(file)["encrypted"] \
                and self.__get_status_object(file)["transferred"]:
            return True
        else:
            return False

