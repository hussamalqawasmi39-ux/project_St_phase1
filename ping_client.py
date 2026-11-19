import socket

from common import make_parser, send_request


def main():
    args = make_parser("Check if the server is reachable.", "python ping_client.py 127.0.0.1 5000").parse_args()
    try:
        reply = send_request(args.host, args.port, "PING")
        print("Reachable" if reply == "PONG" else "Invalid reply")
    except socket.timeout:
        print("No response")
    except socket.gaierror:
        print("Unknown host")
    except OSError:
        print("Connection failed")


if __name__ == "__main__":
    main()
