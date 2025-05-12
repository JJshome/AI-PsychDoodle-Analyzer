"""
Gunicorn configuration for AI-PsychDoodle-Analyzer server
"""

import os
import multiprocessing
import json

# Import server configuration
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server_config import ServerConfig

# Load configuration
config = ServerConfig()
server_config = config.get_server_config()

# Server socket
bind = f"{server_config['host']}:{server_config['port']}"
backlog = 2048

# Worker processes
workers = server_config.get('workers', (multiprocessing.cpu_count() * 2) + 1)
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = server_config.get('timeout', 60)
keepalive = 2

# Server mechanics
daemon = False
raw_env = [
    f"SERVER_HOST={server_config['host']}",
    f"SERVER_PORT={server_config['port']}",
    f"SERVER_WORKERS={workers}",
    f"SERVER_LOG_LEVEL={server_config['log_level']}",
    f"API_REQUIRE_KEY={json.dumps(config.get_api_config()['require_api_key'])}",
    f"USE_GPU={json.dumps(config.get_models_config()['use_gpu'])}"
]

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = server_config.get('log_level', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process naming
proc_name = "ai_psych_doodle_analyzer"

# Server hooks
def on_starting(server):
    """
    Log server start
    """
    print(f"Starting AI-PsychDoodle-Analyzer server on {bind}")

def on_reload(server):
    """
    Log server reload
    """
    print(f"Reloading AI-PsychDoodle-Analyzer server on {bind}")

def post_fork(server, worker):
    """
    Setup after worker fork
    """
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_fork(server, worker):
    """
    Setup before worker fork
    """
    pass

def pre_exec(server):
    """
    Setup before exec
    """
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    """
    Executed when server is ready
    """
    server.log.info(f"Server is ready. Listening on: {bind}")

def worker_int(worker):
    """
    Executed when worker gets SIGINT
    """
    worker.log.info(f"Worker received INT signal (pid: {worker.pid})")

def worker_abort(worker):
    """
    Executed when worker is aborted
    """
    worker.log.info(f"Worker aborted (pid: {worker.pid})")

def worker_exit(server, worker):
    """
    Executed when worker exits
    """
    server.log.info(f"Worker exited (pid: {worker.pid})")