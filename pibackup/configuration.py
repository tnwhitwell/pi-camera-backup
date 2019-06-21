class ConfigManager():
    mount_basedir = "/mnt/"
    source_identifier = "ABEDF0E7-ECDC-4858-B86E-F4D0E43DED21"
    dest_identifier = "70212024-D341-4D10-A258-1B8C1A73EC26"
    backup_dir_name_prefix = "backup_"

    def __repr__(self):
        return str({
            "mount_basedir": self.mount_basedir,
            "source_identifier": self.source_identifier,
            "dest_identifier": self.dest_identifier
        })
