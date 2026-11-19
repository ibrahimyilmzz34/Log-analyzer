# Log Analyzer

A small Python command-line tool that reads SSH authentication logs and counts failed login attempts per IP address. The goal is to spot brute-force attacks.

> 🚧 Work in progress. This is a learning project. It is being built in 3 weeks, and this README will be updated as features are added.

## What it does (so far)

- Reads an SSH log file line by line
- Finds `Failed password` entries
- Pulls out the source IP address and counts the attempts from each IP
- Gets the IP right even when the attacker tries a username like `from`. It reads fields from the end of the line, so a fake username can't move the IP's position.

## Usage

Requires Python 3. No external dependencies.

```bash
python analyzer.py
```

Example output with the included sample log:

```
::1 -> 5
127.0.0.1 -> 3
```

## Sample data

`samples/kali_ssh_2026-11-18.log` was made in my own lab. I started the SSH server on a Kali Linux VM and then tried to log in to it from the same machine (`::1` / `127.0.0.1`). It contains no real third-party data.

### Scenarios in the log

| # | Scenario | Source IP | Failed attempts | Result |
|---|----------|-----------|-----------------|--------|
| 1 | Wrong password for a real user (`ibrahim`) | `::1` | 3 | Connection closed |
| 2 | Login attempt with a non-existent user (`admin`) | `::1` | 2 | Connection closed |
| 3 | Correct password for `ibrahim` | `::1` | 0 | Login accepted ✅ |
| 4 | Username chosen to break naive parsing (`from`) | `127.0.0.1` | 3 | Connection closed |

### Anatomy of a log line

The tool looks at `Failed password` lines. They come in two shapes:

```
Nov 18 20:43:27 kali sshd-session[10794]: Failed password for ibrahim from ::1 port 55320 ssh2
Nov 18 23:56:30 kali sshd-session[31918]: Failed password for invalid user admin from ::1 port 60384 ssh2
```

| Part | Example | Meaning |
|------|---------|---------|
| Timestamp | `Nov 18 20:43:27` | When the attempt happened |
| Host | `kali` | Machine that wrote the log |
| Process | `sshd-session[10794]` | SSH session process and its PID |
| Username | `ibrahim` / `invalid user admin` | Account the attacker tried. `invalid user` means the account doesn't exist |
| Source IP | `::1` | Where the attempt came from (IPv6 localhost here) |
| Port | `55320` | Attacker's source port |

### Why the IP is read from the end of the line

Because of the `invalid user` prefix, the IP is not always at the same position counted from the **start** of the line. Counting from the **end** always works, because every line ends the same way: `<IP> port <port> ssh2`.

```
... from  127.0.0.1  port  50198  ssh2
          [-4]       [-3]  [-2]   [-1]
```

Scenario 4 shows why this matters. The username itself is `from`:

```
Failed password for invalid user from from 127.0.0.1 port 50198 ssh2
```

If you search for the word `from` and take the next field, you get `from`, not the IP. An attacker can use this kind of **log injection** to hide their real address. Reading `parcalar[-4]` avoids the trap.

### Other events in the log (not analyzed yet)

- `Invalid user admin from ::1`: a login attempt for a username that doesn't exist
- `Accepted password for ibrahim`: a successful login. A success right after many failures could mean a brute-force attack worked.
- `Connection closed ... [preauth]`: the client disconnected before logging in
- `pam_unix(...): authentication failure`: the same failures as recorded by the PAM authentication layer

## Roadmap

- [x] Count failed logins per IP
- [ ] Take the log file path as a command-line argument
- [ ] Flag IPs over a configurable threshold as suspicious
- [ ] Use regex for more robust parsing
- [ ] Generate a summary report (text / JSON / CSV)
- [ ] Tests

## What I'm learning

Python file handling and dictionaries, parsing Linux auth logs, how brute-force attacks show up in logs, and Git/GitHub workflow.
