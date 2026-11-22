#!/usr/bin/env python3
"""Read scrolling tape order, or insert one column beside another."""
import json
import re
import subprocess
import sys


def query(name):
    return json.loads(subprocess.check_output(['hyprctl', '-j', name], text=True, timeout=3))


def dispatch(expression):
    result = subprocess.check_output(['hyprctl', 'dispatch', expression], text=True, timeout=3)
    if result.strip() != 'ok':
        raise RuntimeError(result)


def state():
    workspace = query('activeworkspace')
    clients = query('clients')
    windows = sorted((c for c in clients if c['workspace']['id'] == workspace['id']
                      and c['mapped'] and not c['hidden'] and not c['floating']),
                     key=lambda c: (c['at'][0], c['at'][1]))
    return workspace, windows


def main():
    workspace, windows = state()
    clients = query('clients')
    workspace_clients = [c for c in clients if c['workspace']['id'] == workspace['id'] and c['mapped']]
    floating_mode = any('omarchy-floating-workspace' in [tag.rstrip('*') for tag in c.get('tags', [])]
                        for c in workspace_clients)
    enabled = workspace.get('tiledLayout') == 'scrolling' and not floating_mode
    if workspace_clients and all(c['floating'] for c in workspace_clients):
        enabled = False
    if len(sys.argv) == 1:
        print(json.dumps(dict(enabled=enabled, addresses=[w['address'] for w in windows] if enabled else [])))
        return
    source, target, side = sys.argv[1:]
    if not enabled or side not in ('before', 'after'):
        return
    if not all(re.fullmatch(r'0x[0-9a-fA-F]+', a) for a in (source, target)):
        return
    addresses = [w['address'] for w in windows]
    if source not in addresses or target not in addresses or source == target:
        return
    # A stacked column moves as a unit; don't misrepresent that as one window.
    if len({w['at'][0] for w in windows}) != len(windows):
        raise RuntimeError('Hotbar reordering requires one window per scrolling column')
    desired = addresses.copy()
    desired.remove(source)
    desired.insert(desired.index(target) + (side == 'after'), source)
    delta = desired.index(source) - addresses.index(source)
    if not delta:
        return
    original = query('activewindow').get('address')
    try:
        dispatch('hl.dsp.focus({ window = "address:' + source + '" })')
        for _ in range(abs(delta)):
            current, live = state()
            if current['id'] != workspace['id'] or current.get('tiledLayout') != 'scrolling':
                break
            if [w['address'] for w in live].count(source) != 1:
                break
            dispatch('hl.dsp.layout("swapcol ' + ('r' if delta > 0 else 'l') + '")')
    finally:
        if original and re.fullmatch(r'0x[0-9a-fA-F]+', original):
            dispatch('hl.dsp.focus({ window = "address:' + original + '" })')


if __name__ == '__main__':
    main()
