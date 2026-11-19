# Network Diagnostics Tool

A Python command-line network application. One server and three clients talk over TCP
The clients check if the server is reachable, measure how fast it replies, and show its activity

## Team Members

| Name | Student ID | Role |
|------|------------|------|
| Hussam Alqawasmi | 202311374 | Server (`server.py`) |
| Fawzi Abu zenah | 202310133 | Reachability client (`ping_client.py`) |
| Nour shaban | 202320193 | Latency client (`echo_client.py`) |
| لمار عماد محمود حسين | 202410020 | Server activity client (`stats_client.py`) |

## Files

- `server.py` - multithreaded server that answers PING, ECHO and STATS
- `ping_client.py` - sends PING and prints Reachable / No response / connection error
- `echo_client.py` - sends several ECHO requests and reports min, avg and max round-trip time
- `stats_client.py` - sends STATS and prints the server uptime and completed request count
- `common.py` - shared code
- `requirements.txt` - no external dependencies

## Setup

1. Install Python 
2. No packages are needed. Only the Python standard library is used
3. Open a terminal in this folder

## Example Commands

Start the server first:

```
python server.py 127.0.0.1 5000
```

run each client in a new terminal:

```
python ping_client.py 127.0.0.1 5000
python echo_client.py 127.0.0.1 5000 --count 5
python stats_client.py 127.0.0.1 5000 --repeat 3
```

## Expected Output

Server:
```
Server listening on 127.0.0.1:5000
2026-11-19 08:09:40 | 127.0.0.1:4685 | PING | OK
2026-11-19 08:09:40 | 127.0.0.1:4686 | ECHO 1 hello | OK
2026-11-19 08:09:40 | 127.0.0.1:4689 | STATS | OK
```

Reachability client:
```
Reachable
```

Latency client:
```
Request 1: 6.07 ms
Request 2: 0.58 ms
Request 3: 19.05 ms
Request 4: 15.55 ms
Request 5: 15.86 ms

Successful: 5, Timeouts: 0
Min: 0.58 ms, Avg: 11.42 ms, Max: 19.05 ms
```

Server activity client (the count goes up as the other clients send requests):
```
Uptime: 1.1 seconds, Completed requests: 3
Uptime: 3.1 seconds, Completed requests: 7
Uptime: 5.1 seconds, Completed requests: 8
```

Error examples:
```
python ping_client.py 127.0.0.1 5001
Connection failed

python ping_client.py 127.0.0.1 99999
ping_client.py: error: argument port: invalid port '99999'

python ping_client.py no.such.host.invalid 5000
Unknown host
```

## Design Decisions

- **Protocol:** TCP was chosen because it is reliable and shows connection errors clearly
- **Message format:** each request and reply is one line of text ending with a newline

| Request | Reply |
|---------|-------|
| `PING` | `PONG` |
| `ECHO <id> <message>` | `ECHO <id> <message>` |
| `STATS` | `STATS <uptime_seconds> <completed_count>` |
| anything else | `ERROR invalid request` |

- Each client opens a connection, sends one request, reads one reply and closes
- The client timeout is 3 seconds. After that the client reports No response or a timeout
- Shared code is in `common.py` so all four programs use the same port check and request function

## How the Server Handles Concurrent Requests

main thread waits for new connections with `accept()`.
every new connection it starts a new thread that runs `handle_client()`.
thread reads the request, sends the reply, and writes the log line
The main thread goes straight back to waiting, so the three clients are served at the same time

## How Results Are Logged Safely

- When the server starts, it creates a log file named with the start time, for example `server_log_20261119_075857.txt`.
- Each line has the time, client IP and port, the request, and the outcome (OK, ERROR or FAILED)
- The completed request counter is protected by `count_lock`
- Writing to the log file is protected by `log_lock`, so only one thread writes at a time and lines never mix
- If the log file cannot be written, the server prints an error and keeps running
