import os
from multiprocessing import cpu_count

# current directory path
dir_path = os.path.dirname(os.path.realpath(__name__))

# Socket path
bind = 'unix:/run/upscaler/gunicorn.sock'

# Worker Options
# workers = cpu_count() + 1
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Worker timeout
timeout = 120

# Logging Options
loglevel = 'debug'
accesslog = '/var/log/upscaler/access.log'
errorlog = '/var/log/upscaler/error.log'
