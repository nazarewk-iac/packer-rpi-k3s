#!/usr/bin/env python3
import difflib
import os
import re
import subprocess
import sys
from pathlib import Path


def main():
    disable_swap()
    enable_cgroups()
    set_root()


def set_root():
    print('fixing root partitions...')

    root = None
    mounts = subprocess.check_output('mount'.split(), encoding='utf8').splitlines()
    for mount in mounts:
        pieces = mount.split()
        if pieces[2] == '/':
            root = Path(pieces[0])

    if not root:
        print('root partition not found in:\n' + '\n'.join(mounts))
        sys.exit(1)

    root_partuuid_base = None
    paths = list(Path('/dev/disk/by-partuuid').iterdir())
    for path in paths:
        if path.resolve() == root:
            root_partuuid_base, _ = path.name.split('-', maxsplit=1)

    if not root_partuuid_base:
        print(f'root PARTUUID not found in:')
        for path in paths:
            print(f'{path} -> {path.resolve()}')
        sys.exit(1)

    pattern = re.compile(r'PARTUUID=[^-]{8}')
    for path in map(Path, ('/boot/cmdline.txt', '/etc/fstab')):
        old = path.read_text()
        new = pattern.sub(f'PARTUUID={root_partuuid_base}', old)
        printdiff(path, new, old)
        path.write_text(new)


def enable_cgroups():
    print('enabling cgroups...')
    cmdline = Path('/boot/cmdline.txt')
    old = cmdline.read_text()
    args = old.split()
    args.extend((
        'cgroup_enable=cpuset',
        'cgroup_memory=1',
        'cgroup_enable=memory',
    ))
    new = ' '.join(args)

    printdiff(cmdline, new, old)
    cmdline.write_text(new)


def disable_swap():
    print('disabling swap...')

    if '/sbin' not in os.environ['PATH']:
        os.environ['PATH'] += ':/sbin'

    commands = [
        "dphys-swapfile swapoff",
        "dphys-swapfile uninstall",
        "update-rc.d dphys-swapfile remove",
        "systemctl disable dphys-swapfile",
    ]

    for cmd in commands:
        subprocess.run(cmd.split())


def printdiff(path: Path, actual, expected):
    print(f'DIFF {path}:')
    print(diff(actual, expected))


def diff(actual, expected):
    expected = expected.splitlines(keepends=True)
    actual = actual.splitlines(keepends=True)
    return ''.join(difflib.unified_diff(expected, actual))


if __name__ == '__main__':
    main()
