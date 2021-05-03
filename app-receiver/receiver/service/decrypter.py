from cryptography.fernet import Fernet
import logging
import os


class Decrypter:

    def __init__(self, path_to_key):
        self.__decryption_keypath = path_to_key
        self.__load_decryption_key()
        self.__fernet_obj = Fernet(self.__decryption_key)

    def __load_decryption_key(self):
        if os.path.isfile(self.__decryption_keypath):
            key = open(self.__decryption_keypath, "r")
            self.__decryption_key = str.encode(key.read().rstrip('\n'))
        else:
            logging.error("Decryption key is not available in {}.".format(self.__decryption_keypath))
            self.__decryption_key = Fernet.generate_key()
            logging.error("Autogenerated key {} will be used.".format(self.__decryption_key))

    def decrypt_file(self, file_to_decrypt, output_file):
        with open(file_to_decrypt, "rb") as fileobj:
            file_data = fileobj.read()
        decrypted_data = self.__fernet_obj.decrypt(file_data)
        with open(output_file, "wb") as fileobj:
            fileobj.write(decrypted_data)

    def decrypt(self, data_to_decrypt, output_file):
        decrypted_data = self.__fernet_obj.decrypt(data_to_decrypt)
        with open(output_file, "wb") as fileobj:
            fileobj.write(decrypted_data)
