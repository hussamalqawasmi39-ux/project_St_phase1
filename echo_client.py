import socket
import time

from common import make_parser, send_request


def main():
    parser = make_parser("Measure the server response time.", "python echo_client.py 127.0.0.1 5000 --count 5")
    parser.add_argument("--count", type=int, default=5, help="number of ECHO requests (default 5)")
    args = parser.parse_args()

    times = []
    timeouts = 0
    for request_id in range(1, args.count + 1):
        message = f"ECHO {request_id} hello"
        start = time.perf_counter()
        try:
            reply = send_request(args.host, args.port, message)
        except socket.timeout:
            timeouts += 1
            print(f"Request {request_id}: timeout")
            continue
        except socket.gaierror:
            print("Unknown host")
            return
        except OSError:
            print("Connection failed")
            return

        rtt = (time.perf_counter() - start) * 1000
        if reply == message:
            times.append(rtt)
            print(f"Request {request_id}: {rtt:.2f} ms")
        else:
            print(f"Request {request_id}: wrong reply")

    print(f"\nSuccessful: {len(times)}, Timeouts: {timeouts}")
    if times:
        print(f"Min: {min(times):.2f} ms, Avg: {sum(times) / len(times):.2f} ms, Max: {max(times):.2f} ms")


if __name__ == "__main__":
    main()
