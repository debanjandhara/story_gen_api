import http.server
import socketserver
import os
import threading
from queue import Queue

# Number of worker threads
NUM_THREADS = 10

# Request queue for handling incoming requests
request_queue = Queue()

class SeekableFileHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add 'Accept-Ranges' header to allow seeking
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()
    
    def list_directory(self, path):
        # Override list_directory to disable directory listing
        self.send_error(403, "Forbidden")
        return None

    def handle_request(self):
        # Your custom request handling logic goes here
        pass

    def do_GET(self):
        self.handle_request()
        super().do_GET()

def worker():
    while True:
        # Get a request from the queue
        client_address, request = request_queue.get()

        try:
            # Process the request
            handler = SeekableFileHandler(None, client_address, None)
            handler.request = request
            handler.finish()
        except Exception as e:
            print(f"Error processing request: {e}")
            # Restart the worker thread upon failure
            threading.Thread(target=worker, daemon=True).start()
            break  # Exit the current thread

        finally:
            # Mark the task as done
            request_queue.task_done()

def start_server():
    # Change to the media directory
    os.chdir(media_directory)

    # Create a file server with seekable support
    handler = SeekableFileHandler

    # Create a multithreaded HTTP server
    server = socketserver.ThreadingTCPServer(("0.0.0.0", port), handler)

    # Start worker threads
    for _ in range(NUM_THREADS):
        threading.Thread(target=worker, daemon=True).start()

    print(f"Serving on port {port} for all IP addresses")
    
    try:
        # Serve requests indefinitely
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    # Specify the directory containing your unique folders
    # Each unique folder contains an "audio.mp3" file
    media_directory = '/home/azureuser/story-generation/'

    # Set the port for the server
    port = 8000

    # Start the server
    start_server()

