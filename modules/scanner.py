"""
This module is responsible for:
* Scanning every directory defined in audio.scan_directories for audio files
* extracting the metadata from every file and intelligently inserting to the database
* it should support re-scanning very quickly (think about how to do this, using directory hash or something)
* While scanning, it should also upsert the data to the provided database to parallelize the task
"""

import os
from modules.config import Config
from modules.database import Database
from modules.print.utils import get_rich_console
from modules.upsert_merger import UpsertMerger


class Scanner:
    def __init__(self, config: Config, database: Database):
        self.directories_to_scan = config.audio.scan_directories
        self.database = database
        self.config = config
        self.upsert_merger = UpsertMerger(database)
        self.console = get_rich_console()

    def is_audio_file(self, filename: str) -> bool:
        """Check if a file is an audio file based on its extension."""
        _, ext = os.path.splitext(filename)
        return ext.lower().strip() in self.config.audio.scan_formats

    def scan_and_upsert_all_configured_directories(self) -> None:
        """
        Scan all configured directories for audio files.
        TODO: make it multithreaded such that it scans files on different physical devices in separate threads to significantly speed up processing
        TODO: don't read the directories having the same recursive hash (because the bottleneck is the upsert part, not the scanning part)
        """
        all_audio_files = []
        for directory in self.directories_to_scan:
            self.console.log(f"scanning: {directory}")
            all_audio_files.extend(self._scan_directory(directory))
        self.console.log(f"finished scanning all directories")
        self.console.log(f"upserting audio metadata of {len(all_audio_files)} audio files to database")
        self.upsert_merger.upsert_audio_file_metadata(*all_audio_files)

    def _scan_directory(self, directory: str) -> list[str]:
        """Scan a single directory for audio files."""
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if self.is_audio_file(file):
                    audio_files.append(os.path.join(root, file))
        return audio_files


if __name__ == "__main__":
    config = Config.get_base_configuration()
    scanner = Scanner(config, Database(config))
    scanner.scan_and_upsert_all_configured_directories()
