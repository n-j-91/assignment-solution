#!/usr/bin/env bash
#
# This script will create a docker secret called app-sender-receiver-key.
# Content of the secret is a URL-safe base64-encoded 32-byte key that can be used as a symmetric encryption/decryption
# key between app-sender and app-receiver.
# Before using this script, ensure that docker swarm is enabled by running "docker swarm init".
# Run ./create-docker-secret.sh to create the secret.
#

dd if=/dev/urandom bs=32 count=1 2>/dev/null | openssl base64 | docker secret create app-sender-receiver-key -
