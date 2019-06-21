import datetime
from checksumdir import dirhash

from pibackup import configuration, directory, exceptions

class BackupManager():
    start_time = None
    config = None
    dirmanager = None

    def __init__(self, conf: configuration.ConfigManager, dmgr: directory.DirManager):
        self.config = conf
        self.dirmanager = dmgr

    def do_backup(self):
        if self.start_time is not None:
            raise exceptions.BackupAlreadyRunningError(self.start_time)
        self.start_time = datetime.datetime.now()

        destination = self.dirmanager.next_backup_dir()
        print("{} => {}".format(self.dirmanager.source_base, destination))
        source_hash = dirhash(str(self.dirmanager.source_base), 'sha1', excluded_files=self.config.source_identifier)
        # source_hash = directory.get_hash_of_dirs(self.dirmanager.source_base, ignore=self.config.source_identifier)
        directory.copy_files(self.dirmanager.source_base, destination)
        destination_hash = directory.get_hash_of_dirs(destination, ignore=self.config.source_identifier)
        if source_hash == destination_hash:
            return True
        else:
            raise exceptions.BackupChecksumFailedError(source_hash, destination_hash)
