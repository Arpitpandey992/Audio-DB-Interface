"""
This module extracts information from scanned audio files and upserts them to the database
Ideally, it should provide an upsert function which should collect data and upsert at regular intervals (or batch size)
"""

from modules.database import Database
from modules.helper import extract_audio_file_metadata


class UpsertMerger:
    def __init__(self, database: Database) -> None:
        self.database = database

    def upsert_audio_file_metadata(self, file_path: str) -> bool:
        """
        upserts the provided audio file's metadata to database after extracting it
        Args:
            file_path (str): path of audio file whose metadata to upsert

        Returns:
            bool: whether the upsert was successful or not
        """
        try:
            metadata = extract_audio_file_metadata(file_path)
        except Exception as e:
            print(f"could not extract metadata of [{file_path}]. error: [{e}]")
            return False
        
