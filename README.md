# Introductory Task

This is a simple server that accepts string from the user and checks if the string exists in the configuration file and returns the response accordingly.

## Table of Content
- [Setting Up the virtual Environment](#setting-up-the-virtual-environment)
- [Setting up configuration file](#setting-up-configuration-file)
- [Runing as daemon](#running-as-daemon)
- [Running Normally](#running-normally)
- [Using the client script](#using-the-client-script)

---

## Setting Up the virtual Environment

### Step 1: Create a Virtual Environment

Navigate to the project directory and create a virtual environment:
```bash
python3 -m venv venv
```
Creating a virtual environment is different for different operating systems, you can follow this youtube video for instructions on any of Linux, Windows or Mac [Video](https://youtu.be/kz4gbWNO1cw)

Activate the virtual environment:
* On Linux/macOS:

```bash
source venv/bin/activate
```

* On Windows:

```bash
venv\Scripts\activate
```

### Step 2: Install Dependencies
Navigate to the project directory and run the bash command:

```bash
pip install -r requirements.txt
```

---
## Setting up configuration file
You have to create a file named .env at the root of the folder and then copy the contents of sample.env into it and then set the variables values acording to your setup for running the server.

For HOST, PORT and BUFFER_SIZE, you set the values acording to the available port and host on your system, The LOG_FILE is the path to the file you want the logs to be saved for debugging,
linuxpath is the path to the file where the server search for the existence of the string sent by the client.

REREAD_ON_QUERY DEBUG, USE_SSL=False and ENABLE_SSL can be set as true or false, but USE_SSL is only used for client script to determine ssl or not in the client server communication.

SSL_CERTIFICATE is set to the path of your generated ssl certificate incase of running in secure mode, SSL_KEY is the path to ssl key for secure mode, then also set the MAX_BUFFER_SIZE.


## Running as daemon
Navigate to the project directory and run the command

```bash
python3 py_server/server.py daemon
```

## Running Normally
Navigate to the project directory and run the command

```bash
python3 py_server/server.py
```

## Using the client script
Navigate to the project directory and run the command

```bash
python3 speed_test_client.py daemon
```
