from flask import Flask

from pibackup import configuration, directory, backup, exceptions

app = Flask(__name__)

config = configuration.ConfigManager()
dirmanager = directory.DirManager(config)
backup_manager = backup.BackupManager(config, dirmanager)
# directories.create_new_incremental_directory(directories.dest_base)

try:
    backup_manager.do_backup()
except exceptions.BackupAlreadyRunningError as e:
    print(e)

@app.route('/')
def hello_world():
    return str(dirmanager)

# def reload_
