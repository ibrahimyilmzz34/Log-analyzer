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

`samples/kali_ssh_2026-11-18.log` was made in my own lab: failed SSH logins against a Kali Linux VM from localhost. It contains no real third-party data.

## Roadmap

- [x] Count failed logins per IP
- [ ] Take the log file path as a command-line argument
- [ ] Flag IPs over a configurable threshold as suspicious
- [ ] Use regex for more robust parsing
- [ ] Generate a summary report (text / JSON / CSV)
- [ ] Tests

## What I'm learning

Python file handling and dictionaries, parsing Linux auth logs, how brute-force attacks show up in logs, and Git/GitHub workflow.
