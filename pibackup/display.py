from pibackup import directory, configuration


class DisplayManager:
    config = None  # type: configuration.ConfigManager
    dirmanager = None  # type: directory.DirManager

    def __init__(self, config, dirmanager):
        self.config = config
        self.dirmanager = dirmanager

    def getChartData(self):
        source = directory.disk_space(self.dirmanager.source_base)
        dest = directory.disk_space(self.dirmanager.dest_base)
        data = [
            {
                "name": "sourceChart",
                "value": source,
                "title": "Source Disk"
            },
            {
                "name": "destChart",
                "value": dest,
                "title": "Destination Disk"
            }
        ]
        return data

    def getDisks(self):
        pass

    def getBackupData(self):
        data = {
            "meta": {
                "headers": [
                    {
                        "name": "Name",
                        "key": "name"
                    },
                    {
                        "name": "File Count",
                        "key": "file_count",
                        "numeric": True
                    },
                    {
                        "name": "Source Checksum",
                        "key": "source_hash"
                    },
                    {
                        "name": "Backup Checksum",
                        "key": "backup_hash"
                    }
                ]
            },
            "data": self.dirmanager.get_backups()
        }
        return data
