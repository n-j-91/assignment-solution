#!/usr/bin/env bash

#
# This script will create a URL-safe base64-encoded 32-byte key and a directory structure to input json files and
# output decrypted xml files
#
# Run ./prepare-env.sh create the key and directory structure.
#
# Generated key can be mounted to app-sender and app-receiver containers to allow symmetric encryption and decryption.
# Mount input to /usr/share/app-sender/input of app-sender.
# Mount status-db to /usr/share/app-sender/status-db of app-sender.
# Mount output to /usr/share/app-receiver/output of app-receiver.
#
BASE_PATH=$(dirname \"$(readlink "$0")\")

mkdir -p $BASE_PATH/input $BASE_PATH/output $BASE_PATH/status-db
dd if=/dev/urandom bs=32 count=1 2>/dev/null | openssl base64 > $BASE_PATH/key