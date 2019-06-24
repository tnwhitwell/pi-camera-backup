from pibackup import directory, configuration


class DisplayManager:
    config = None  # type: configuration.ConfigManager
    dirmanager = None  # type: directory.DirManager

    def __init__(self, config, dirmanager):
        self.config = config
        self.dirmanager = dirmanager

    def getChartData(self):
        source = directory.disk_space(self.dirmanager.source_base)[1:]
        dest = directory.disk_space(self.dirmanager.dest_base)[1:]
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

    def get_potential_disks(self, filebrowser_base_url):
        disks = self.dirmanager.get_disks()  # type: [directory.Disk]
        resp = []
        for d in disks:
            resp.append(
                {
                    "name": d.name,
                    "fb_url": "{}/files/{}".format(
                        filebrowser_base_url,
                        d.name
                    ),
                    "free": d.free,
                    "used": d.used,
                    "total": d.total,
                    "percent": round(100 * d.used / d.total, 0),
                    "is_source": d.is_source,
                    "is_dest": d.is_dest
                }
            )
        return {
            "data": resp
        }

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
