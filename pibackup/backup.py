import datetime
import pathlib
import uuid
import json

from collections.abc import Mapping


from pibackup import configuration, directory, exceptions


class Job:
    start_time = None  # type: datetime.datetime
    destination = None  # type: pathlib.Path
    source_hash = None  # type: str
    destination_hash = None  # type: str
    id = None # type: uuid.uuid4

    def __init__(self):
        self.id = uuid.uuid4()

    def serialise(self) -> dict:
        return {
            "id": str(self.id),
            "start_time": self.start_time.strftime("%c"),
            "destination": str(self.destination),
            "source_hash": self.source_hash,
            "destination_hash": self.destination_hash
        }

    def run_time(self):
        now = datetime.datetime.now()
        run_time = now - self.start_time
        hours, remainder = divmod(run_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return("{}:{}:{}".format(
            hours, minutes, seconds
        ))

    def meta(self):
        print(list(self.destination.glob("**/*")))
        return {
            "source_hash": self.source_hash,
            "backup_hash": self.destination_hash,
            "file_count": len(
                list(self.destination.rglob("*"))) - 1,
            "job_id": str(self.id)
        }



class BackupManager:
    current_job = None  # type: Job
    config = None  # type: configuration.Config
    dirmanager = None  # type: directory.DirManager

    def __init__(self, conf: configuration.ConfigManager, dmgr):
        self.config = conf
        self.dirmanager = dmgr

    def do_backup(self):
        if self.current_job is not None:
            self.config.socketio.emit("backup already running", self.current_job.serialise())
            raise exceptions.BackupAlreadyRunningError(self.current_job.start_time)
        j = Job()
        j.start_time = datetime.datetime.now()
        j.destination = self.dirmanager.next_backup_dir()
        self.current_job = j
        print(j.serialise())
        self.config.socketio.emit("backup started", j.serialise())

        print("{} => {}".format(self.dirmanager.source_base, self.current_job.destination))
        self.dirmanager.copy_files(self.dirmanager.source_base, j)
        meta_file = j.destination / ".meta_{}".format(j.id)
        job_metadata = j.meta()
        meta_file.write_text(json.dumps(job_metadata))
        print("backup done")
        self.config.socketio.emit("backup complete", j.serialise())
        self.current_job = None
