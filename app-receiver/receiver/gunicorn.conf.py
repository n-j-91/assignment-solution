import os

bind = "{0}:{1}".format(os.getenv("SERVER_IP", "127.0.0.1"), os.getenv("SERVER_PORT", "8080"))
loglevel = os.getenv("LOG_LEVEL", "info")
