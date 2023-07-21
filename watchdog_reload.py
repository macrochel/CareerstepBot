import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def reload_app():
    try:
        # Import your main application here
        import app
        print("Reloading the application...")
        # Add any additional reload logic specific to your application
    except Exception as e:
        print(f"Error reloading the application: {e}")

if __name__ == "__main__":
    event_handler = FileSystemEventHandler()

    def on_modified(event):
        if event.src_path.endswith(".py"):
            reload_app()

    event_handler.on_modified = on_modified
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        print("Application started. Watching for changes...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
