import logging
import os
"""
This file maintains configurations for app-sender.
"""

logging.basicConfig(format='[%(asctime)s] - [%(levelname)s] - [%(filename)s] - %(message)s',
                    level=os.getenv("LOG_LEVEL", logging.INFO))

INPUT_DIR = os.getenv("INPUT_DIR", "/usr/src/app-sender/input")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "/tmp/encryption_key")
SCAN_INTERVAL = os.getenv("SCAN_INTERVAL", "5")
STATUS_DB_PATH = os.getenv("STATUS_DB_PATH", "/usr/src/app-sender/status-db")
RECEIVER_ADDRESS = os.getenv("RECEIVER_ADDRESS", "127.0.0.1")
RECEIVER_PORT = os.getenv("RECEIVER_PORT", "8080")
RECEIVER_URI = os.getenv("RECEIVER_URI", "/upload")