#!/usr/bin/env python3
"""Safe synthetic log/event generator for SOC demos.

Writes newline-delimited JSON events to a file or stdout. Events are synthetic and non-malicious.
Use Filebeat or other forwarders to ship these logs to Elasticsearch for demo/visualization.

Example:
  python3 tools/log_generator.py --out ./demo/logs/syslog_demo.log --rate 5 --pattern suspicious_login
"""
import argparse
import time
import json
import random
import sys
from datetime import datetime

USERS = ['alice','bob','charlie','david','eve','mallory','oscar']
IP_POOL = ['10.0.0.%d' % i for i in range(2,60)] + ['192.168.1.%d' % i for i in range(2,60)]
HOSTS = ['host-1','host-2','host-3','admin-workstation','web-server']

SUSPICIOUS_USERNAMES = ['admin','root','svc_backup','svc_sync']

def gen_base_event():
    return {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'host': random.choice(HOSTS),
        'process': random.choice(['sshd','nginx','powershell','curl','python','systemd']),
        'message': '',
        'event': {
            'action': 'info'
        }
    }

def normal_event():
    e = gen_base_event()
    e.update({
        'user': random.choice(USERS),
        'src_ip': random.choice(IP_POOL),
        'message': 'User login successful',
        'event': {'action': 'auth_success'}
    })
    return e

def suspicious_login():
    e = gen_base_event()
    # simulate repeated failed logins followed by success, or login from odd user
    if random.random() < 0.7:
        e.update({
            'user': random.choice(USERS),
            'src_ip': random.choice(IP_POOL),
            'message': 'Failed password for user',
            'event': {'action': 'auth_failed'}
        })
    else:
        e.update({
            'user': random.choice(SUSPICIOUS_USERNAMES),
            'src_ip': random.choice(IP_POOL),
            'message': 'Login successful for privileged account',
            'event': {'action': 'auth_success', 'risk': 'high'}
        })
    return e

def file_access_event():
    e = gen_base_event()
    e.update({
        'user': random.choice(USERS),
        'src_ip': random.choice(IP_POOL),
        'file': random.choice(['/etc/passwd','/var/www/html/index.php','/home/alice/secrets.txt']),
        'message': 'File read',
        'event': {'action': 'file_read'}
    })
    return e

PATTERNS = {
    'normal': normal_event,
    'suspicious_login': suspicious_login,
    'file_access': file_access_event
}

def main():
    parser = argparse.ArgumentParser(description='Synthetic log/event generator (safe)')
    parser.add_argument('--out', '-o', default=None, help='Output file (default stdout)')
    parser.add_argument('--rate', type=float, default=1.0, help='Events per second (float allowed)')
    parser.add_argument('--pattern', choices=PATTERNS.keys(), default='normal', help='Event pattern to generate')
    parser.add_argument('--duration', type=float, default=0, help='Duration in seconds (0 = infinite)')
    args = parser.parse_args()

    writer = sys.stdout
    if args.out:
        # ensure directory exists
        import os
        os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
        writer = open(args.out, 'a', buffering=1)

    interval = 1.0 / max(args.rate, 0.001)
    pattern_fn = PATTERNS[args.pattern]

    start = time.time()
    count = 0
    try:
        while True:
            ev = pattern_fn()
            writer.write(json.dumps(ev) + '\n')
            count += 1
            if args.duration and (time.time() - start) >= args.duration:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        if args.out and writer is not sys.stdout:
            writer.close()
        print(f"Generated {count} events", file=sys.stderr)

if __name__ == '__main__':
    main()
