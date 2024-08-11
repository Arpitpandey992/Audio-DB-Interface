from modules.config import Config
from modules.database import Database
from modules.scanner import Scanner


class App:
    def __init__(self) -> None:
        self.config = Config.get_base_configuration()
        self.database = Database(self.config)
        self.scanner = Scanner(self.config, self.database)

    def start_up(self):
        self.scanner.scan_and_upsert_all_configured_directories()

    def close(self):
        self.database.close()


if __name__ == "__main__":
    import time

    app = App()
    app.start_up()

    try:
        print("search for docs")
        text = ""
        while text != "exit":
            text = input()
            print(app.database.search(text))
    finally:
        app.close()
