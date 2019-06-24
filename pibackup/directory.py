import pathlib
import re
import shutil
import os
import json

from collections.abc import Mapping
from checksumdir import dirhash

from pibackup import backup, configuration


class Disk:
    name = None  # type: str
    path = None  # type: pathlib.Path
    free = None  # type: int
    used = None  # type: int
    total = None  # type: int
    is_source = False
    is_dest = False
    config = None  # type: configuration.ConfigManager

    def __init__(self, config: configuration.ConfigManager, path: pathlib.Path):
        self.path = path
        self.name = path.name
        self.total, self.used, self.free = disk_space(path)
        self.is_source = (path / config.source_identifier).is_file()
        self.is_dest = (path / config.dest_identifier).is_file()
        self.config = config

    def set_destination(self, state):
        self.is_dest = state
        if state:
            (self.path / self.config.dest_identifier).touch(exist_ok=True)
            self.set_source(False)
        else:
            try:
                (self.path / self.config.dest_identifier).unlink()
            except FileNotFoundError:
                pass

    def set_source(self, state):
        self.is_source = state
        if state:
            (self.path / self.config.source_identifier).touch(exist_ok=True)
            self.set_destination(False)
        else:
            try:
                (self.path / self.config.source_identifier).unlink()
            except FileNotFoundError:
                pass


class DirManager(Mapping):
    source_base = None
    dest_base = None
    dest_dir = None
    config = None

    def __init__(self, cfg):
        self.config = cfg
        self.source_base = self.identify_mounts(self.config.source_identifier)
        self.dest_base = self.identify_mounts(self.config.dest_identifier)
        self._storage = {
            "source_base": str(self.source_base),
            "dest_base": str(self.dest_base)
        }

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def identify_mounts(self, identifier: str):
        base_dir = pathlib.Path(self.config.mount_basedir)
        dir_list = [d for d in base_dir.rglob(identifier) if not pathlib.PurePath(
            str(d)).match("*/{}*/*".format(self.config.backup_dir_name_prefix))]
        if len(dir_list) != 1:
            return None
        else:
            return pathlib.Path(dir_list[0]).parent

    def set_disks(self, raw_input):
        input = dict(raw_input)

        destinations = []
        for d_input in input.pop("is_dest", []):
            d_name = re.match('^(.+)-is_dest$', d_input).groups(0)[0]
            destinations.append(Disk(self.config, pathlib.Path(self.config.mount_basedir) / d_name))

        sources = []
        for d_input in input.pop("is_source", []):
            d_name = re.match('^(.+)-is_source$', d_input).groups(0)[0]
            sources.append(Disk(self.config, pathlib.Path(self.config.mount_basedir) / d_name))

        unuseds = [Disk(self.config, pathlib.Path(self.config.mount_basedir) / d_name) for d_name in input]

        for disk in destinations:
            disk.set_destination(True)
        for disk in sources:
            disk.set_source(True)
        for disk in unuseds:
            disk.set_destination(False)
            disk.set_source(False)

    def get_disks(self):
        base_dir = pathlib.Path(self.config.mount_basedir)
        disks = []
        for d in base_dir.glob("*"):
            disks.append(Disk(self.config, d))
        return disks

    def next_backup_dir(self):
        existing_dirs = sorted([
            int(re.match('{}([0-9]+)$'.format(self.config.backup_dir_name_prefix), p.name).groups(0)[0])
            for p in self.dest_base.iterdir() if p.match("{}*".format(self.config.backup_dir_name_prefix))
        ])
        try:
            last = existing_dirs[-1]
            new_suffix = int(last) + 1
        except IndexError:
            new_suffix = 1
        nd = self.dest_base / "{}{}".format(self.config.backup_dir_name_prefix, new_suffix)

        return nd

    def dirhash(self, path: pathlib.Path):
        return dirhash(
            str(path), 'sha1',
            excluded_files=[self.config.source_identifier, self.config.dest_identifier]
        )

    def get_backups(self):
        backup_dirs = sorted(
            [p for p in self.dest_base.iterdir() if p.match("{}*".format(self.config.backup_dir_name_prefix))],
            key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', str(s))])
        data = []
        for dir in backup_dirs:  # type: pathlib.Path
            meta_file = list(dir.glob(".meta_*"))[0]
            metadata = json.loads(meta_file.read_text())
            metadata["name"] = dir.name
            metadata["filebrowser_uri"] = "/files/{}".format(str(dir).replace(str(self.config.mount_basedir), ""))
            data.append(metadata)
        return data

    def copy_files(self, source: pathlib.Path, job: backup.Job):
        job.source_hash = self.dirhash(str(source))
        copied = shutil.copytree(
            str(source), str(job.destination),
            ignore=shutil.ignore_patterns())
        job.destination_hash = self.dirhash(str(job.destination))
        return copied


def disk_space(path: pathlib.Path):
    statvfs = os.statvfs(str(path))
    total = statvfs.f_frsize * statvfs.f_blocks
    free = statvfs.f_frsize * statvfs.f_bavail
    used = total - free
    return total, used, free
