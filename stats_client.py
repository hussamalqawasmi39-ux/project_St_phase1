import socket
import time

from common import make_parser, send_request


def main():
    parser = make_parser("Show server uptime and completed requests.", "python stats_client.py 127.0.0.1 5000 --repeat 3")
    parser.add_argument("--repeat", type=int, default=1, help="how many times to ask (default 1)")
    args = parser.parse_args()

    for i in range(args.repeat):
        try:
            parts = send_request(args.host, args.port, "STATS").split()
            if len(parts) == 3 and parts[0] == "STATS":
                print(f"Uptime: {parts[1]} seconds, Completed requests: {parts[2]}")
            else:
                print("Invalid reply")
        except socket.timeout:
            print("No response")
        except socket.gaierror:
            print("Unknown host")
            return
        except OSError:
            print("Connection failed")
            return
        if i < args.repeat - 1:
            time.sleep(2)


if __name__ == "__main__":
    main()
