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

If you are unsure or do not know the answers to some questions, leave them and answer the remaining.

**IMPORTANT:**  
- **Please clone or fork this repository first.**  
- **Solution / answers should be provided as a single pull request to "main" branch.**

## Pre Requisites

- Workstation with bash cli, docker-ce, docker-compose, python 3.7 and git client.
- Basic programing skills with python 3 and ability to understand code written in python 3.
- Basic understanding of the client / server architecture, restful API.
- Knowledge in running linux commands, scripts with bash.
- Knowledge in testing and packaging python applications.
- Knowledge in building docker images, running docker containers with docker cli and docker-compose.
- Knowledge in docker volumes, environment variables used with docker images.
- Optionally the knowledge in docker swarm or docker secrets.

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

All configurations are parsed in the form of Environment Variables. You may override them during run time if required.

# ASSIGNMENT TASKS

There are missing pieces in this solution.
Your task is to fill each missing piece in a way that final solution is
functional as described above.

Below instructions will guide you to locate each part that requires a fix.
Try to address as many points as you can.


1. There are some simple pytests added in test_controller.py file of the app-receiver.
   They can be located in _app-receiver/receiver/tests_ directory. Change the directory
   to _app-receiver/_ and run the tests.
    ```
    cd ./app-receiver/
    pytest -v tests
    ```
    Observe the assertion failure for test_health_check method.
    ```
    =========================================================================== short test summary info ===========================================================================
    FAILED tests/test_controller.py::test_health_check - AssertionError: assert {'msg': 'Serv...us_code': 200} == {'msg': 'Serv...us_code': 200}
    
    ```
    Fix the health_check method to pass the test case.
   

2. Open _app-receiver/receiver/service/controller.py_ and locate _upload_file_ method.
   This method is incomplete. Refer to the comments provided with the method and complete 
   the implementation to achieve what is expected from it. Use the hints provided.
   
   > Hints: 
   >
   > - Locate the test_upload_file pytest method in app-receiver/tests/test_controller.py module.
   > - test_upload_file method is correct and requires no changes.
   > - Implement upload_file method in a way that pytest for test_upload_file passes.

3. There are some missing directives in _./app-receiver/Dockerfile_.
   Identify and add these missing statements to the Dockerfile so that it can be 
   successfully built and run as a container. 
   See below example of a successful execution of app-receiver container.
   ```
   docker run --rm app-receiver:latest
   [2021-05-04 22:11:29 +0000] [1] [INFO] Starting gunicorn 20.1.0
   [2021-05-04 22:11:29 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
   [2021-05-04 22:11:29 +0000] [1] [INFO] Using worker: sync
   [2021-05-04 22:11:29 +0000] [7] [INFO] Booting worker with pid: 7
   ERROR:root:Decryption key is not available in /run/secrets/decryption_key.
   ERROR:root:Autogenerated key b'KeRnEkgfBp60gEEAxQkQWbbQ0Fcg8lrXwhR0U6mjaCE=' will be used.
   ```
   Ignore the error at the bottom of the output above. 
   This is expected behaviour of the app-receiver when /run/secrets/decryption_key is not present within the container.
   
   >Hint: 
   >
   >- Create a "key" by running "prepare-env.sh" script, and mount it to /run/secrets/decryption_key path
   >of the app-receiver container to avoid above error.
   > ```
   > bash -x ./prepare-env.sh
   > 
   > +++ readlink ./prepare-env.sh
   > ++ dirname '""'
   > + BASE_PATH=.
   > + mkdir -p ./input ./output ./status-db
   > + dd if=/dev/urandom bs=32 count=1
   > + openssl base64
   > ```
   
4. Imagine that you need to run the pytests for _app-receiver_ during the _docker build_.
   Modify the Dockerfile for app-receiver to meet this requirement.
   
   > Hints:
   > 
   > - Try to use docker multi-stage builds.
   > - When you run the following command(s) pytests should be run as part of the build.
   > ```
   > docker build -t app-receiver:latest app-receiver/
   > --or--
   > docker build -t app-receiver:latest --target development_image app-receiver/
   > ```
   
5. _run_scan()_ method of _app-sender/sender/\_\_main\_\_.py_ has slight logical problem in its design.
   In terms of converting, encrypting and transferring the file to the remote server, 
   there is **an added delay between each step, for the same .json file.**
   Can you identify this and fix?
   
   > e.g.:
   > 
   > Notice the delay of 10 seconds between each action output below, for the same .json file.
   > ```
   > app-sender_1    | [2021-05-04 22:59:00,192] - [INFO] - [utils.py] - /usr/src/app-sender/input/books.json is converted to /usr/src/app-sender/input/books.xml
   > app-sender_1    | [2021-05-04 22:59:10,230] - [INFO] - [utils.py] - books.json is encrypted to /usr/src/app-sender/input/books.xml.enc
   > app-sender_1    | [2021-05-04 22:59:20,269] - [INFO] - [utils.py] - books is uploaded successfully. Response from server: File is decrypted and saved to /usr/src/app-receiver/output/books.xml
   > ```
   
6. An important directive is missing from _app-sender/Dockerfile_. 
   When it is built and run, no output is visible. See below example.
   ```
   docker run -v ${PWD}/input:/usr/src/app-sender/input sender:test
   <NO OUTPUT>
   
   docker ps -a                                                    
   CONTAINER ID   IMAGE         COMMAND     CREATED          STATUS                     PORTS     NAMES
   aa9f86df4596   sender:test   "python3"   3 seconds ago    Exited (0) 2 seconds ago             thirsty_benz
   ```
   How can this be fixed? 
   
7. Complete _docker-compose-v1.yml_ file to build and run app-sender and app-receiver applications
   via docker-compose.
   
   > Hints:
   > 
   > - When following command is called, it should build _app-receiver:latest_ and _app-sender:latest_
   > **production docker images**.
   >  ```
   >  docker-compose -f docker-compose-v1.yml build --no-cache
   >  ``` 
   > - _app-sender_ should be able to fetch input .json files from the host machine.
   > - Files received and decrypted by _app-receiver_ should be accessible from the host machine.
   > - Use prepare-env.sh script to create symmetric encryption key that should be shared by both
   > _app-sender_ and _app-receiver_
   > - _app-sender_ should persist the state of the processed json files across restarts. In other words,
   > if _app-sender_ is restarted unexpectedly, the .json file that were already processed by it should not be re-processed.
   >

8. **[Optional task]** prepare-env.sh script will create a "key" file that can be mounted to 
_app-sender_ and _app-receiver_.However this is not a secure way of sharing the symmetric
   encryption key between two containers.
   As a solution to this problem, "create-docker-secret.sh" script is provided.
   This script will create the symmetric encryption key in the form of a docker secret.
   Next populate the missing parameters in "docker-compose-v2.yml" file so that
   it can run the _app-sender_ and _app-receiver_ containers as a **service** in a single node
   docker swarm cluster.
   
   > Hints:
   > 
   > - Refer the comments available with _create-docker-secret.sh_ and _docker-compose-v2.yml_
   > files.
   > - Services in a docker swarm can mount docker secrets to /var/run/\<secret name\> path
   > of the respective container.
   
   