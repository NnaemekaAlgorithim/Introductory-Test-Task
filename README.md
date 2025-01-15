to run as a deamon:
Create a file called my_python_server.service
sudo nano /etc/systemd/system/my_python_server.service

Add the following content to the service file:
[Unit]
Description=My Python Server Daemon
After=network.target

[Service]
ExecStart=/path/to/Introductory-Test-Task/env/bin/python /path/to/Introductory-Test-Task/py_server/server.py
WorkingDirectory=/path/to/Introductory-Test-Task
StandardOutput=journal
StandardError=journal
User=your-user-name
Group=your-user-group
Environment="PATH=/path/to/Introductory-Test-Task/test_env/bin:$PATH"
Environment="VIRTUAL_ENV=/path/to/Introductory-Test-Task/test_env"
Restart=always

[Install]
WantedBy=multi-user.target

Make sure to replace /path/to/your/script.py with the actual path to your Python script, and set the User and Group to the appropriate Linux user/group that will run the service.

Reload the systemd manager to recognize the new service:
sudo systemctl daemon-reload

Start the service:
sudo systemctl start my_python_server

Enable the service to start on boot:
sudo systemctl enable my_python_server

To check the status of your service:
sudo systemctl status my_python_server

If you need to stop the service:
sudo systemctl stop my_python_server

Systemd will log the output of your Python script to the journal, which you can view with:
sudo journalctl -u my_python_server.service
