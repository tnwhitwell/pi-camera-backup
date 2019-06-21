from datetime import datetime

import pibackup

class BackupManagerException(Exception):
    """Base class for other BackupManager Exceptions"""
    def __init__(self, msg: str = None):
        if msg is None:
            msg = "An error occurred in BackupManager"
        super(BackupManagerException, self).__init__(msg)

class BackupAlreadyRunningError(BackupManagerException):
    """Raised when the backup is already running"""
    def __init__(self, start_time: datetime):
        now = datetime.now()
        run_time = now - start_time
        hours, remainder = divmod(run_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        super(BackupAlreadyRunningError, self).__init__(
            msg="A backup is already in progress. Current run time: {}".format(
                "{:02}:{:02}:{:02}".format(
                    hours, minutes, seconds
                )
            )
        )

class BackupChecksumFailedError(BackupManagerException):
    """Raised when the hash of source and dest differ after copying"""
    def __init__(self, source_hash: str, dest_hash: str):
        super(BackupChecksumFailedError, self).__init__(
            msg="The checksums of source and dest differ: {} != {}".format(
                source_hash, dest_hash
            )
        )
        self.source_hash = source_hash
        self.dest_hash = dest_hash
