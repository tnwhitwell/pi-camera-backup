import http
import subprocess

from flask import Flask, request, redirect, render_template, jsonify
from urllib.parse import urlparse


from concurrent.futures import ThreadPoolExecutor

from pibackup import configuration, directory, backup, display


executor = ThreadPoolExecutor(2)

app = Flask(__name__)

config = configuration.ConfigManager()
dirmanager = directory.DirManager(config)
backup_manager = backup.BackupManager(config, dirmanager)
display_manager = display.DisplayManager(config, dirmanager)



@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/backup', methods=['GET', 'POST'])
def run_backup():
    if backup_manager.current_job is not None:
        if request.method == 'POST':
            return "Backup already running. Start time: {}".format(
                backup_manager.current_job.start_time
            ), http.HTTPStatus.CONFLICT
        return backup_manager.current_job.run_time(), http.HTTPStatus.OK
    if request.method == 'GET':
        return "No backup currently running", http.HTTPStatus.NOT_FOUND
    executor.submit(backup_manager.do_backup)
    return "Backup started", http.HTTPStatus.CREATED

@app.route('/filebrowser')
def redir_to_filebrowser():
    return redirect("{}://{}:{}".format(
        request.scheme, urlparse(request.base_url).hostname,
        config.filebrowser_port
    ), http.HTTPStatus.MOVED_PERMANENTLY)

@app.route('/shutdown', methods=["POST"])
def shutdown_pi():
    shutdown = subprocess.run(
        ["systemctl", "poweroff"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resp = app.make_response(
        str({
            'stderr': shutdown.stderr,
            'stdout': shutdown.stdout,
            'return': shutdown.returncode
        })
    )
    resp.status_code = http.HTTPStatus.CREATED
    resp.mimetype = 'application/json'
    return resp

@app.route('/api/chartdata', methods=["GET"])
def chart_data():
    data = display_manager.getChartData()
    return jsonify(data), http.HTTPStatus.OK
