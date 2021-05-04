import os
"""
This file contains configurations for receiver service.
The configurations can be over-ridden with Environment Variables during run time.
"""
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/usr/src/app-receiver/output")
DECRYPTION_KEY = os.getenv("DECRYPTION_KEY", "/tmp/decryption_key")
