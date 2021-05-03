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
- Pipfile (3rd party libraries are packages with pipenv)
- Pipfile.lock
- setup.py

app-receiver is a simple restful application written in Flask framework. It is hosted with gunicorn.
- _app-receiver/receiver/gunicorn.conf.py_ file contains web server configurations.
- _app-receiver/receiver/service/settings.py_ file contains application configurations.
- All configurations are parsed in the form of Environment Variables. You may override them during run time if required.
- _app-receiver/receiver/service/controller.py_ has an incomplete method that you need to complete as part of the solution.