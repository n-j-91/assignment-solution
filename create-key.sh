#!/usr/bin/env bash

# This script will create a URL-safe base64-encoded 32-byte key.
# Run ./create-key.sh to create the key.
# Generated key can be mounted to app-sender and app-receiver containers to allow symmetric encryption and decryption.

dd if=/dev/urandom bs=32 count=1 2>/dev/null | openssl base64 > key