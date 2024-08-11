"""
This module extracts information from scanned audio files and upserts them to the database
Ideally, it should provide an upsert function which should collect data and upsert at regular intervals (or batch size)
"""

from dataclasses import asdict
from modules.database import Database
from modules.helper import calculate_md5, extract_audio_file_metadata
from modules.print.utils import get_rich_console

console = get_rich_console()


class UpsertMerger:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.console = get_rich_console()

    def upsert_audio_file_metadata(self, *file_paths: str) -> bool:
        """
        upserts the provided audio file's metadata to database after extracting it
        Args:
            file_path (str): path of audio file whose metadata to upsert

        Returns:
            bool: whether the upsert was successful or not
        """
        upsertable_metadata_list = [result for file_path in file_paths if (result := self._extract_upsertable_information(file_path)) is not None]
        self.database.upsert_documents(upsertable_metadata_list)

        return True  # TODO: return proper result of upsert, think over if it is better to stop upsert if even one of the individual upserts failed

    def _extract_upsertable_information(self, file_path: str) -> dict[str, str] | None:
        try:
            metadata = extract_audio_file_metadata(file_path)
        except Exception as e:
            self.console.log(f"could not extract metadata of {file_path}. [red]error: [{e}][/red]")
            return None
        document = asdict(metadata)
        document.pop("tags")
        document.update(**asdict(metadata.tags))
        document.pop("pictures")
        document[self.database.get_primary_key_name()] = calculate_md5(metadata.file_path)
        return document
