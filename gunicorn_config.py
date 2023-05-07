import multiprocessing

# Gunicorn configuration
workers = multiprocessing.cpu_count() * 2 + 1
bind = "127.0.0.1:8000"
loglevel = "debug"
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
