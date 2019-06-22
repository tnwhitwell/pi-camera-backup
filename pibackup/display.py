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
