import meilisearch
import subprocess

from modules.config import Config
from modules.helper import wait_till_address_responds
from modules.print.utils import get_rich_console

console = get_rich_console()


class MeiliSearchHelper:
    def __init__(self, config: Config) -> None:
        self.config = config.database.meilisearch
        self.http_addr = f"{self.config.host}:{self.config.port}"
        self.server_url = f"{'https'if not self.config.port or self.config.port==443 else 'http'}://{self.http_addr}"
        self.meilisearch_process = self._start_meilisearch()  # TODO: make sure this is closed when the program exits (app.py)

        self.client = meilisearch.Client(self.server_url)
        self.client.create_index(self.config.index_name, {"primaryKey": self.config.index_primary_key})

    def upsert_documents(self, documents: list[dict], primary_key: str | None = None) -> None:
        if primary_key:
            self.client.index(self.config.index_name).add_documents(documents, primary_key=primary_key)
        else:
            self.client.index(self.config.index_name).add_documents(documents)

    def search(self, key: str):
        return self.client.index(self.config.index_name).search(key)

    def get_primary_key_name(self) -> str:
        return self.config.index_primary_key

    def close(self):
        """close all held up connections to free up resources"""
        self.meilisearch_process.terminate()
        console.log(f"[blue]waiting for meilisearch to close gracefully")
        self.meilisearch_process.wait()
        console.log(f"[green]meilisearch was successfully closed")

    def _start_meilisearch(self):
        args = self._build_startup_args()
        process = subprocess.Popen(["meilisearch", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        server_started_successfully = wait_till_address_responds(self.server_url)
        if not server_started_successfully:
            _, stderr = process.communicate()
            raise Exception(f"could not start meilisearch at {self.server_url}. error: [{stderr}]")
        return process

    def _build_startup_args(self) -> list[str]:
        args = ["--http-addr", self.http_addr, "--db-path", self.config.db_path]
        for extra_arg in self.config.startup_args:
            args.append(extra_arg)

        return args


if __name__ == "__main__":
    search = MeiliSearchHelper(Config.get_base_configuration())
    search.close()
