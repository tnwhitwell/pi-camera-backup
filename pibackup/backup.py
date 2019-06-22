import datetime
import pathlib

from time import sleep

from pibackup import configuration, directory, exceptions


class Job:
    start_time = None  # type: datetime.datetime
    destination = None  # type: pathlib.Path
    source_hash = None  # type: str

    def run_time(self):
        now = datetime.datetime.now()
        run_time = now - self.start_time
        hours, remainder = divmod(run_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return("{}:{}:{}".format(
            hours, minutes, seconds
        ))


class BackupManager:
    current_job = None  # type: Job
    config = None  # type: configuration.Config
    dirmanager = None  # type: directory.DirManager

    def __init__(self, conf: configuration.ConfigManager, dmgr):
        self.config = conf
        self.dirmanager = dmgr

    def do_backup(self):
        if self.current_job is not None:
            raise exceptions.BackupAlreadyRunningError(self.current_job.start_time)
        j = Job()
        j.start_time = datetime.datetime.now()
        j.destination = self.dirmanager.next_backup_dir()
        self.current_job = j

        print("{} => {}".format(self.dirmanager.source_base, self.current_job.destination))
        directory.copy_files(self.dirmanager.source_base, j)
        sleep(10)
        print("backup done")
        self.current_job = None
