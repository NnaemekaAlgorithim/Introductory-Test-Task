# Introductory Task

This is a simple server that accepts a string from the user, checks if the string exists in the configuration file, and returns the response accordingly.

## Table of Content
- [Setting Up The virtual Environment](#setting-up-the-virtual-environment)
- [Setting Up Configuration File](#setting-up-configuration-file)
- [Running As Daemon](#running-as-daemon)
- [Running Normally](#running-normally)
- [Using The Client Script](#using-the-client-script)

---

## Setting Up The virtual Environment

### Step 1: Create A Virtual Environment

Navigate to the project directory and create a virtual environment:
```bash
python3 -m venv venv
```
Creating a virtual environment is different for different operating systems. You can follow this YouTube video for instructions on Linux, Windows, or macOS: [Video](https://youtu.be/kz4gbWNO1cw)

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
Navigate to the project directory and run the following command:

```bash
pip install -r requirements.txt
```

---
## Setting Up Configuration File
You need to create a file named .env at the root of the folder, then copy the contents of sample.env into it. After that, set the variable values according to your setup for running the server.

For HOST, PORT, and BUFFER_SIZE, set the values according to the available port and host on your system. LOG_FILE should be the path to the file where you want the logs to be saved for debugging. linuxpath is the path to the file where the server searches for the existence of the string sent by the client.

REREAD_ON_QUERY, DEBUG, USE_SSL=False, and ENABLE_SSL can be set to true or false. However, USE_SSL is only used by the client script to determine whether SSL should be used for communication between the client and the server.

SSL_CERTIFICATE should be set to the path of your generated SSL certificate if running in secure mode. SSL_KEY should be the path to the SSL key for secure mode. Lastly, set MAX_BUFFER_SIZE.


## Running As Daemon
Navigate to the project directory and run the command

```bash
python3 py_server/server.py daemon
```

Or we can set it up as a systemd service by following the steps below:

### Step 1: Locate the Path of Your Virtual Environment and Script
Activate your virtual environment and note its full path:
```bash
source /path/to/venv/bin/activate
which python
deactivate
```
Replace /path/to/venv with your virtual environment's directory.
Note the full path to your Python script.

### Step 2: Create the Service File
Open a terminal and create a new service file for your script:
```bash
sudo nano /etc/systemd/system/introductory-task-server.service
```

### Step 3: Edit the Service File
Add the following content:
```bash
[Unit]
Description= introductory task server Daemon
After=network.target

[Service]
Type=simple
User=your_user
Group=your_user_group
WorkingDirectory=/path/to/the/folder/Introductory-Test-Task
ExecStart=/path/to/venv/bin/python /path/to/folder/Introductory-Test-Task/py_server/server.py
Restart=always
Environment="PYTHONPATH=/path/to/folder/Introductory-Test-Task:$PYTHONPATH"
Environment="PATH=/path/to/venv/bin:$PATH"
[Install]
WantedBy=multi-user.target
```
Replace your_user and your_user_group with your system user and group respectively,

Replace /path/to/the/folder/Introductory-Test-Task, /path/to/venv/bin/python /path/to/folder/Introductory-Test-Task/py_server/server.py, /path/to/folder/Introductory-Test-Task and /path/to/venv/bin with the absolute paths for the respective files and folders.

### Step 4: Reload and Enable the Service

Reload the systemd manager to recognize the new service:
```bash
sudo systemctl daemon-reload
```

Enable the service to start at boot:
```bash
sudo systemctl enable introductory-task-server.service
```

Start the service:
```bash
sudo systemctl start introductory-task-server.service
```

Check the status of the service to ensure it's running:
```bash
sudo systemctl status introductory-task-server.service
```

### Step 5: Test and Debug

View the logs of your service:
```bash
journalctl -u introductory-task-server.service
```

If needed, modify the service file and reload:
```bash
sudo nano /etc/systemd/system/introductory-task-server.service
sudo systemctl daemon-reload
sudo systemctl restart introductory-task-server.service
```

### Step 6: Optional - Manage Your Service

Stop the Service:
```bash
sudo systemctl stop introductory-task-server.service
```

Disable the Service:
```bash
sudo systemctl disable introductory-task-server.service
```

## Running Normally
Navigate to the project directory and run the command

```bash
python3 py_server/server.py
```

## Using The Client Script
Navigate to the project directory and run the command

```bash
python3 speed_test_client.py daemon
```
