import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class HEICtoPNGHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith('.heic'):
            return
        time.sleep(1)  # Delay to ensure the file is fully written
        if not os.path.isfile(event.src_path) or os.path.getsize(event.src_path) == 0:
            print(f"File {event.src_path} is not ready or is empty.")
            return
        try:
            png_path = event.src_path.rsplit('.', 1)[0] + '.png'
            conversion_command = f"/usr/bin/sips -s format png '{event.src_path}' --out '{png_path}'"
            if os.system(conversion_command) == 0:
                print(f"Converted {event.src_path} to {png_path}")
                os.remove(event.src_path)
                print("Removed original HEIC file")
            else:
                print(f"Failed to convert {event.src_path}")
        except Exception as e:
            print(f"Error processing file {event.src_path}: {e}")


def start_monitoring(path):
    event_handler = HEICtoPNGHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print("Watchdog started. Any airdropped photos will be automatically converted to PNG.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    sys.stdout.flush()
    download_folder = os.path.expanduser('~/Downloads')
    print("AirConvert 1.0.0 by Ian Fain\n")
    print("Turning on watchdog for Downloads folder...")
    start_monitoring(download_folder)
