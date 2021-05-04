import os
"""
This file contains configurations for gunicorn.
The configurations can be over-ridden with Environment Variables during run time.
"""
bind = "{0}:{1}".format(os.getenv("SERVER_IP", "127.0.0.1"), os.getenv("SERVER_PORT", "8080"))
loglevel = os.getenv("LOG_LEVEL", "info")
