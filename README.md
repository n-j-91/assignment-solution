# devops-assignment-python-and-docker

This repo contains following folder structure.
- app-sender
- app-receiver
- docker-compose-v1.yml
- docker-compose-v2.yml
- prepare-env.sh
- create-docker-secret.sh
- LICENSE
- README.md

app-sender and app-receiver are two independent directories containing two partially complete python applications. 
Instructions below elaborate further about the missing pieces of each application.
Read them carefully and try to complete what is asked in each step to build and deliver a complete solution.

If you are unsure or do not know the answers some questions, leave them blank and answer the remaining.

**IMPORTANT:**  
- **Please clone or fork this repository before attempting.**  
- **Solution / answers should be provided as a single pull request.**

## Pre Requisites

- Workstation with bash cli, docker-ce, docker-compose, python 3.7 and git client.
- Basic programing skills with python 3 and ability to understand code written in python 3.
- Basic understanding of the client / server architecture, restful API.
- Knowledge in running linux commands, scripts with bash.
- Knowledge in testing and packaging python applications.
- Knowledge in building docker images, running docker containers with docker cli and docker-compose.
- Knowledge in docker volumes, environment variables used with docker images.
- Knowledge in simple CI flows, Jenkinsfile.
- Knowledge in docker swarm or secrets is optional.

## Solution Overview

### app-receiver
Directory structure:
- receiver (source files for receiver application)
- tests (unit tests)
- Dockerfile
- Pipfile (3rd party libraries are packaged with pipenv)
- Pipfile.lock
- setup.py

app-receiver is a simple restful application written in python Flask framework. It is hosted with gunicorn.
- _app-receiver/receiver/gunicorn.conf.py_ file contains web server configurations.
- _app-receiver/receiver/service/settings.py_ file contains application configurations.
- All configurations are parsed in the form of Environment Variables. You may override them during run time if required.
- _app-receiver/receiver/service/controller.py_ has an incomplete method that you need to complete as part of the solution.

app-receiver provides two rest interfaces.
- GET /  
  Checks the health of the service. Returns 200 with json response when successful.
  
- POST /upload/\<filename>  
  Accepts a file in the form of multipart/form-data. Upon successful receipt of the
  file, it will be decrypted and stored to a location specified with OUTPUT_DIR environment variable.


### app-sender
Directory structure:
- sender (source files for sender application)
- tests (unit tests)
- Dockerfile
- Pipfile (3rd party libraries are packaged with pipenv)
- Pipfile.lock
- setup.py

app-sender acts as a client to app-receiver. It is capable of following tasks.
- Scans directory specified in INPUT_DIR environment variable for json files.
- If a json file is found, it will verify if it has been processed before.
- If the particular file is processed already, it will skip processing it and move to the next file.
- If it is not processed already, it will convert it to xml, encrypt with the given key and transfer it
  to a remote server specified by RECEIVER_ADDRESS, RECEIVER_PORT environment variables.
  
- When successfully processed the file, it will add a record in the state handler.
- Above tasks will be repeated in an infinite loop, with a delay between each cycle, specified with SCAN_INTERVAL environment variable.

# ASSIGNMENT TASKS

There are missing pieces in this solution.
Your task is to fill each missing piece in a way that final solution is
functional as described above.

Below instructions will guide you to locate each part that requires a fix.
Try to address as many points as you can.