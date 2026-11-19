import socket
import threading
import time
from datetime import datetime

from common import make_parser

start_time = time.time()
completed = 0
count_lock = threading.Lock()
log_lock = threading.Lock()
log_file = datetime.now().strftime("server_log_%Y%m%d_%H%M%S.txt")


def write_log(addr, request, outcome):
    """Write one log line, one thread at a time."""
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {addr[0]}:{addr[1]} | {request} | {outcome}"
    with log_lock:
        print(line)
        try:
            with open(log_file, "a") as f:
                f.write(line + "\n")
        except OSError:
            print("Could not write to log file")


def process(request):
    """Return the reply and outcome for a request."""
    global completed
    parts = request.split(" ", 2)
    command = parts[0].upper()

    if command == "PING":
        reply = "PONG"
    elif command == "ECHO" and len(parts) == 3:
        reply = f"ECHO {parts[1]} {parts[2]}"
    elif command == "STATS":
        with count_lock:
            reply = f"STATS {time.time() - start_time:.1f} {completed}"
    else:
        return "ERROR invalid request", "ERROR"

    with count_lock:
        completed += 1
    return reply, "OK"


def handle_client(conn, addr):
    """Handle one client in its own thread."""
    request = ""
    with conn:
        try:
            conn.settimeout(5)
            request = conn.makefile().readline().strip()
            reply, outcome = process(request)
            conn.sendall((reply + "\n").encode())
        except OSError:
            outcome = "FAILED"
    write_log(addr, request, outcome)


def main():
    args = make_parser("Network diagnostics server.", "python server.py 127.0.0.1 5000").parse_args()
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((args.host, args.port))
        server.listen()
    except OSError:
        print("Could not start server")
        return

    print(f"Server listening on {args.host}:{args.port}")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server.close()


if __name__ == "__main__":
    main()
