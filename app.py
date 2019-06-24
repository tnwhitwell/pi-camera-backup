import http
import subprocess
import json

from flask import Flask, request, redirect, render_template, jsonify
from flask_socketio import SocketIO
from urllib.parse import urlparse

from concurrent.futures import ThreadPoolExecutor

from pibackup import configuration, directory, backup, display

executor = ThreadPoolExecutor(2)

app = Flask(__name__)
socketio = SocketIO(app)

config = configuration.ConfigManager(socketio)
directory_manager = directory.DirManager(config)
backup_manager = backup.BackupManager(config, directory_manager)
display_manager = display.DisplayManager(config, directory_manager)

## Helper Functions

def json_error(
        description, details="",
        code=255, meta={}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR):
    return app.make_response((
        jsonify({
            "error": {
                "description": description,
                "details": details,
                "code": code,
                "meta": meta
            }
        }), status))


def build_filebrowser_url(request):
    return (
        "{}://{}:{}".format(
            request.scheme,
            urlparse(request.base_url).hostname,
            config.filebrowser_port
        ))

## Route Definitions


@app.route('/')
def home():
    vars = {
        "filebrowser_base": "{}://{}:{}".format(
            request.scheme, urlparse(request.base_url).hostname,
            config.filebrowser_port),
    }
    return render_template('home.html', **vars)


@app.route('/backup')
def backup():
    vars = {
        "filebrowser_base": "{}://{}:{}".format(
            request.scheme, urlparse(request.base_url).hostname,
            config.filebrowser_port),
    }
    return render_template('backup.html', **vars)


@app.route('/configure')
def configure():
    vars = {
        "filebrowser_base": "{}://{}:{}".format(
            request.scheme, urlparse(request.base_url).hostname,
            config.filebrowser_port),
    }
    return render_template('config.html', **vars)


@app.route('/api/backup', methods=['GET', 'POST'])
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


@app.route('/api/power', methods=["POST"])
def power_action():
    action = request.form["action"]
    if action not in ["poweroff", "reboot"]:
        return jsonify(
            {"error": "action {} not found".format(action)}
        ), http.HTTPStatus.NOT_FOUND
    try:
        systemctl_action = subprocess.run(
            ["systemctl", action],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            check=True)

        resp = app.make_response((
            jsonify({
                "stderr": systemctl_action.stderr.decode("utf-8"),
                "stdout": systemctl_action.stdout.decode("utf-8")
            }),
            http.HTTPStatus.CREATED))
    except subprocess.SubprocessError as e:
        resp = json_error(
            description="{} failed".format(action),
            code=e.errno,
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        resp = json_error(
            description="{} failed".format(action),
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return resp


@app.route('/api/chartdata', methods=["GET"])
def chart_data():
    data = display_manager.getChartData()
    return jsonify(data), http.HTTPStatus.OK


@app.route('/api/backups', methods=["GET"])
def backup_list():
    data = display_manager.getBackupData()
    return jsonify(data), http.HTTPStatus.OK


@app.route('/api/potential_disks', methods=["GET"])
def potential_disks():
    data = display_manager.get_potential_disks(
        build_filebrowser_url(request)
    )
    return jsonify(data), http.HTTPStatus.OK

@app.route('/api/configure_disks', methods=["POST"])
def configure_disks():
    directory_manager.set_disks(request.form)
    return redirect("/configure", http.HTTPStatus.SEE_OTHER)

@app.route('/api/config/<conf_name>', methods=["GET"])
def get_config(conf_name):
    if conf_name == 'config':
        data = dict(config)
    elif conf_name == 'directories':
        data = dict(directory_manager)
    try:
        print(data)
        return jsonify(data), http.HTTPStatus.OK
    except UnboundLocalError:
        return jsonify({}), http.HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
