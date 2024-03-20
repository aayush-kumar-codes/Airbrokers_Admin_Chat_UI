# Define the Python path to your Django project's settings module
pythonpath = '/root/apis/django_chat_admin'

# Specify the WSGI application for Gunicorn to run
# Change 'your_project_name' to the name of your Django project
# Change 'your_project_name.wsgi' to the location of your WSGI application
# Usually, it's the 'wsgi.py' file inside your Django project folder
wsgi_app = 'admin_ui.wsgi:application'

# The address and port to bind to
bind = '127.0.0.1:8099'

# The number of worker processes for handling requests
workers = 4

# Log level
loglevel = 'info'

# Path to the error log file
errorlog = '/var/log/gunicorn_error.log'
