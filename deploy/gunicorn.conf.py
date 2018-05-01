from __future__ import unicode_literals
import multiprocessing

bind = "unix:/opt/assistant/deploy/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "/opt/assistant/deploy/error.log"
loglevel = "error"
proc_name = "assistant"

