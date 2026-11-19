import argparse
import socket


def port_number(text):
    """Check the port is a number from 1 to 65535."""
    if not text.isdigit() or not 1 <= int(text) <= 65535:
        raise argparse.ArgumentTypeError(f"invalid port '{text}'")
    return int(text)


def make_parser(description, example):
    """Read host and port from the command line."""
    parser = argparse.ArgumentParser(description=description, epilog=f"example: {example}")
    parser.add_argument("host", help="server host name or IP address")
    parser.add_argument("port", type=port_number, help="server port (1-65535)")
    return parser


def send_request(host, port, message, timeout=3):
    """Send one request and return the reply."""
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall((message + "\n").encode())
        return sock.makefile().readline().strip()
