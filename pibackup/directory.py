import pathlib
import re
import shutil
import os

from checksumdir import dirhash

from pibackup import backup


class DirManager:
    source_base = None
    dest_base = None
    dest_dir = None
    config = None

    def __init__(self, cfg):
        self.config = cfg
        self.source_base = self.identify_mounts(self.config.source_identifier)
        self.dest_base = self.identify_mounts(self.config.dest_identifier)

    def identify_mounts(self, identifier: str):
        base_dir = pathlib.Path(self.config.mount_basedir)
        dir_list = [d for d in base_dir.rglob(identifier) if not pathlib.PurePath(
            str(d)).match("*/{}*/*".format(self.config.backup_dir_name_prefix))]
        if len(dir_list) != 1:
            return None
        else:
            return pathlib.Path(dir_list[0]).parent

    def next_backup_dir(self):
        existing_dirs = sorted([p.name for p in self.dest_base.iterdir() if p.match("{}*".format(self.config.backup_dir_name_prefix))])
        try:
            last = existing_dirs[-1]
            ln = re.match('{}([0-9]+)$'.format(self.config.backup_dir_name_prefix), last)
            new_suffix = int(ln.groups(0)[0]) + 1
        except IndexError:
            new_suffix = 1
        nd = self.dest_base / "{}{}".format(self.config.backup_dir_name_prefix, new_suffix)

        return nd

    def compare(self, job: backup.Job):

        destination_hash = dirhash(str(job.destination), 'sha1', excluded_files=self.config.source_identifier)
        if job.source_hash == destination_hash:
            return True
        else:
            return False

    def __repr__(self):
        return str({
            "source_drive": str(self.source_base),
            "destination_drive": str(self.dest_base)
        })


def copy_files(source: pathlib.Path, job: backup.Job):
    copied = shutil.copytree(
        str(source), str(job.destination),
        ignore=shutil.ignore_patterns())
    return copied

def disk_space(path: pathlib.Path):
    statvfs = os.statvfs(str(path))
    total = statvfs.f_frsize * statvfs.f_blocks
    free = statvfs.f_frsize * statvfs.f_bavail
    return [total - free, free]
