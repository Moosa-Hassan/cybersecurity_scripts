
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import OCR_Detection as ocr
import time
import os
from PIL import Image

class UploadFolderHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            if ocr.main(event.src_path) and self.imgcheck(event.src_path):
                os.remove(event.src_path)
                print(f"File {event.src_path} processed and removed.")   
                
    def imgcheck(self, file_path):
        try:
            img = Image.open(file_path)
            img.verify()  # Verify that it is an image
            return True
        except (IOError, SyntaxError) as e:
            return False 
            

# Path to monitor
path = r"C:\Users\Moosa\Documents\intenship\Scripts for DLP\uploads"

event_handler = UploadFolderHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
