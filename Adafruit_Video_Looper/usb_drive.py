# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import glob
import os

from .usb_drive_mounter import USBDriveMounter


class USBDriveReader:

    def __init__(self, config):
        """Create an instance of a file reader that uses the USB drive mounter
        service to keep track of attached USB drives and automatically mount
        them for reading videos.
        """
        self._load_config(config)
        self._mounter = USBDriveMounter(root=self._mount_path,
                                        readonly=self._readonly)
        self._mounter.start_monitor()


    def _load_config(self, config):
        self._mount_path = config.get('usb_drive', 'mount_path')
        self._readonly = config.getboolean('usb_drive', 'readonly')

    def search_paths(self):
        """Return a list of paths to search for files. Will return a list of all
        mounted USB drives.
        """
        self._mounter.mount_all()
        return glob.glob(self._mount_path + '*')

    def search_usb_paths(self, folder_name):
        """Return a list of paths to the specified folder on mounted USB drives."""
        usb_paths = []
    
        # Get a list of all mounted USB drives
        mounted_drives = self.search_paths()
    
        # Search for the specified folder on each mounted USB drive
        for drive in mounted_drives:
            folder_path = os.path.join(drive, folder_name)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                usb_paths.append(folder_path)
    
        return usb_paths

    def is_changed(self):
        """Return true if the file search paths have changed, like when a new
        USB drive is inserted.
        """
        return self._mounter.poll_changes()

    def idle_message(self):
        """Return a message to display when idle and no files are found."""
        return 'Insert USB drive with compatible movies.'


def create_file_reader(config, screen):
    """Create new file reader based on mounting USB drives."""
    return USBDriveReader(config)
