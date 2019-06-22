import json
import os
from collections.abc import Mapping

from flask_socketio import SocketIO

class ConfigManager(Mapping):
    mount_basedir = "/media"
    source_identifier = "ABEDF0E7-ECDC-4858-B86E-F4D0E43DED21"
    dest_identifier = "70212024-D341-4D10-A258-1B8C1A73EC26"
    backup_dir_name_prefix = "backup_"
    filebrowser_port = None  # type: int
    socketio = None # type: SocketIO

    def __init__(self, socketio: SocketIO ):
        with open("filebrowser.json", 'r') as f:
            filebrowser_config = json.load(f)
            self.filebrowser_port = filebrowser_config["port"]

        self.mount_basedir = os.getenv("MOUNT_BASEDIR", self.mount_basedir)
        self.source_identifier = os.getenv("SOURCE_IDENTIFIER", self.source_identifier)
        self.dest_identifier = os.getenv("DESTINATION_IDENTIFIER", self.dest_identifier)
        self.backup_dir_name_prefix = os.getenv("BACKUP_DIR_PREFIX", self.backup_dir_name_prefix)
        self.socketio = socketio

        self._storage = {
            "mount_basedir": self.mount_basedir,
            "source_identifier": self.source_identifier,
            "dest_identifier": self.dest_identifier,
            "backup_dir_name_prefix": self.backup_dir_name_prefix
        }

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)
