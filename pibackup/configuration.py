import json
class ConfigManager:
    mount_basedir = "/mnt/"
    source_identifier = "ABEDF0E7-ECDC-4858-B86E-F4D0E43DED21"
    dest_identifier = "70212024-D341-4D10-A258-1B8C1A73EC26"
    backup_dir_name_prefix = "backup_"
    filebrowser_port = None  # type: int

    def __init__(self):
        with open("filebrowser.json", 'r') as f:
            filebrowser_config = json.load(f)
            self.filebrowser_port = filebrowser_config["port"]

        with open("pibackup.json", 'r') as f:
            file_cfg = json.load(f)
            self.mount_basedir = file_cfg["mount_basedir"]
            self.source_identifier = file_cfg["source_identifier"]
            self.dest_identifier = file_cfg["destination_identifier"]
            self.backup_dir_name_prefix = file_cfg["backup_directory_name_prefix"]


    def __repr__(self):
        return str({
            "mount_basedir": self.mount_basedir,
            "source_identifier": self.source_identifier,
            "dest_identifier": self.dest_identifier
        })
