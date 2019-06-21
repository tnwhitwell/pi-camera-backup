import pathlib
import re
import shutil

from pibackup import configuration


# class Directory():
#     path = None
#     dir_hash = None

#     def __repr__(self):
#         return str(self.path)

class DirManager():
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

    def __repr__(self):
        return str({
            "source_drive": str(self.source_base),
            "destination_drive": str(self.dest_base)
        })

def copy_files(source: pathlib.Path, dest: pathlib.Path):
    shutil.copytree(
        str(source), str(dest),
        ignore=shutil.ignore_patterns())


def get_hash_of_dirs(directory: pathlib.Path, ignore: str = None):
    import os
    import hashlib
    SHAhash = hashlib.sha1()
    if not directory.exists():
        return None

    try:
        for root, dirs, files in os.walk(str(directory)):
            for names in files:
                if ignore is not None:
                    if names == ignore:
                        continue
                    else:
                        print(names)
                filepath = os.path.join(root, names)
                try:
                    f1 = open(filepath, 'rb')
                except:
                    # You can't open the file for some reason
                    f1.close()
                    continue

                while True:
                    # Read file in as little chunks
                    buf = f1.read(4096)
                    if not buf:
                        break
                    SHAhash.update(hashlib.sha1(buf).hexdigest())
                    f1.close()

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return None

    return SHAhash.hexdigest()
