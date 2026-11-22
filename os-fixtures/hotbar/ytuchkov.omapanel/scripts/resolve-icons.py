#!/usr/bin/env python3
"""Resolve window identities locally, without executing desktop entry commands."""
import configparser
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


def entries():
    roots = [Path(os.environ.get('XDG_DATA_HOME', str(Path.home()/'.local/share')))]
    roots += [Path(p) for p in os.environ.get('XDG_DATA_DIRS', '/usr/local/share:/usr/share').split(':') if p]
    seen = set()
    result = []
    for root in roots:
        directory = root/'applications'
        for path in sorted(directory.rglob('*.desktop')):
            key = str(path.relative_to(directory)).replace('/', '-')[:-8]
            if key in seen:
                continue
            seen.add(key)
            parser = configparser.ConfigParser(interpolation=None, strict=False)
            try:
                parser.read(path, encoding='utf-8')
                e = parser['Desktop Entry']
                if e.get('Hidden', '').lower() == 'true':
                    continue
                command = shlex.split(e.get('Exec', ''))
                executable = Path(command[0]).name.lower() if command else ''
                game = re.search(r'steam://rungameid/(\d+)', e.get('Exec', ''))
                result.append({'id': key, 'icon': e.get('Icon', ''),
                               'startup': e.get('StartupWMClass', '').lower(),
                               'exe': executable, 'game': game.group(1) if game else ''})
            except (OSError, ValueError, configparser.Error, KeyError):
                continue
    return result


def identity(pid):
    game = ''
    executable = ''
    for depth in range(6):
        if pid <= 1:
            break
        proc = Path('/proc')/str(pid)
        try:
            env = dict(item.split(b'=', 1) for item in (proc/'environ').read_bytes().split(b'\0') if b'=' in item)
            raw = env.get(b'SteamAppId', b'').decode('ascii', errors='ignore')
            if raw.isdecimal() and raw != '0':
                game = raw
            if depth == 0:
                executable = Path(os.readlink(proc/'exe')).name.lower()
            if game:
                break
            status = (proc/'status').read_text()
            pid = int(re.search(r'^PPid:\s+(\d+)', status, re.M).group(1))
        except (OSError, ValueError, AttributeError):
            break
    return game, executable


def resolve(clients, apps):
    result = {}
    for client in clients:
        game, executable = identity(int(client.get('pid', 0)))
        classes = {str(client.get(k, '')).lower() for k in ('class', 'initialClass')} - {''}
        # Only accept unambiguous identity matches; never guess from window titles.
        candidates = []
        if game:
            candidates = [e for e in apps if e['game'] == game]
        if not candidates:
            candidates = [e for e in apps if e['startup'] and e['startup'] in classes]
        if not candidates:
            candidates = [e for e in apps if e['exe'] and e['exe'] == executable]
        if candidates and len({e['icon'] for e in candidates}) == 1:
            result[client['address']] = candidates[0]
        elif game:
            result[client['address']] = {'id': '', 'icon': 'steam_icon_' + game}
    return result


if __name__ == '__main__':
    try:
        clients = json.loads(subprocess.check_output(['hyprctl', 'clients', '-j'], timeout=3))
        print(json.dumps(resolve(clients, entries())))
    except (OSError, ValueError, subprocess.SubprocessError):
        print('{}')
