import threading
from time import sleep
import requests
from unigen import AudioFactory, AudioFileMetadata

from modules.print.utils import get_rich_console

console = get_rich_console()


def extract_audio_file_metadata(file_path: str) -> AudioFileMetadata:
    """extracts metadata from audio files
    Args:
        file_path (str): audio file path

    Returns:
        AudioFileMetadata: metadata object of the input file

    Raises: UnsupportedFileFormatError, FileNotFoundError

    """
    audio = AudioFactory.buildAudioManager(file_path)
    return audio.getMetadata()


def wait_till_address_responds(url: str) -> bool:
    console.log(f"[bold]testing {url}")
    server_ready, timed_out, stop_checking = False, False, False
    sleep_time_seconds, max_sleep_time_seconds, timeout, per_request_timeout = 1, 16, 60, 2
    default_status = "[bold]checking if server is ready to serve requests"
    with console.status(default_status) as status:

        def update_console_status_every_second():
            nonlocal server_ready
            time_left_seconds = timeout
            while not server_ready and time_left_seconds >= 0:
                status.update(f"{default_status},[bold magenta] Time left: {time_left_seconds} seconds")
                sleep(1)
                time_left_seconds -= 1
            nonlocal timed_out
            timed_out = True

        def check_if_server_ready():
            nonlocal server_ready, sleep_time_seconds, url, stop_checking
            while not server_ready and not stop_checking:
                try:
                    requests.get(url, timeout=per_request_timeout)
                    console.log(f"[green]{url} is ready to serve requests!")
                    server_ready = True
                except requests.ConnectionError as e:
                    console.log(f"[red]error[/] connecting to {url}, retrying after {sleep_time_seconds} seconds, error: {e}")
                    sleep(sleep_time_seconds)
                    sleep_time_seconds = min(sleep_time_seconds * 2, max_sleep_time_seconds)

        timeout_thread = threading.Thread(target=update_console_status_every_second)
        checker_thread = threading.Thread(target=check_if_server_ready)
        checker_thread.start()
        timeout_thread.start()
        while True:
            if not timeout_thread.is_alive() or not checker_thread.is_alive():
                stop_checking = True
                break
            sleep(1)
    if not server_ready:
        return False
    return True
