from modules.config import Config
from modules.database import Database
from modules.scanner import AudioScanner


def start_up():
    config = Config.get_base_configuration()
    database = Database(config)
    scanner = AudioScanner(config, database)
