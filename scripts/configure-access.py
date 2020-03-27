#!/usr/bin/env python3
import difflib
import subprocess
from pathlib import Path


def main():
    setup_user(
        'nazarewk',
        'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAYEAvM4y0G5vZ2OYlSeGn2w7y/s+VZMzhGGb9rlUkDtWtwvsE2TWlApFyHggn6qObmQ5DUOu0Mhy6l/ojylyp2Q/C7FMoQWkeBorLKvxf8KFE1lJktCXCxJyptDn8kkNi6Fxszig/flrp5lSWWjDCafyVeyFhvMo22fblzjPOG//wu0+RnOLn9eiWC2CUvJjG11AH+AxWI4UMXY93gq5K1YVLd3EmhI/L1ITAoY3cXoheP0TW9epqe0Zq6lGO+gLiYeWgZJiolSqcHCkTzopbkIZ2cP+yEdeJrYp8ibdO7H0oyXOy48yPElkEobcISzQmTayXQfXyr9YzFPGdM0ZxxKPfpmMox2DTL+mpo1etLOf7ihJNBoR6aAcAWeYLdfqmIlWnVVySW1RPcq31tR4uCP6jpDsbEArXP7lttkWzb0EuBRKN94OVsl7gHuqSSdnrWJwU6jn8EAi9krRQtOKUrz62nOmAkWIe/4fM/3CVjuOgTSUkmuu15SgrbN9aLYp0ct/ nazarewk',
    )
    secure_ssh()
    subprocess.run('systemctl enable ssh.service'.split())

    delete_pi()


def setup_user(username, ssh_key):
    commands = [
        f'adduser --shell /usr/bin/zsh {username}',
        f'usermod -a -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi {username}',
    ]

    for cmd in commands:
        subprocess.run(cmd.split())

    ssh = Path(f'/home/{username}/.ssh')
    ssh.mkdir(0o700)

    authorized_keys = ssh / 'authorized_keys'
    authorized_keys.write_text(ssh_key)
    authorized_keys.chmod(0o600)

    Path(f'/etc/sudoers.d/010-{username}-nopasswd').write_text(f'{username} ALL=(ALL) NOPASSWD: ALL')


def secure_ssh():
    sshd_config = Path('/etc/ssh/sshd_config')
    old_lines = sshd_config.read_text().splitlines(keepends=False)
    rules = [
        'ChallengeResponseAuthentication no',
        'PasswordAuthentication no',
        'UsePAM no',
    ]
    new_lines = [
        line
        for line in old_lines
        if not any(r.split()[0] in line for r in rules)
    ]
    new_lines.extend(rules)

    new_text = '\n'.join(old_lines)
    printdiff(sshd_config, old_lines, new_text)
    sshd_config.write_text(new_text)


def delete_pi():
    sudoers = Path('/etc/sudoers.d/010_pi-nopasswd')
    if sudoers.exists():
        sudoers.unlink()

    subprocess.run('deluser -remove-home pi'.split())


def printdiff(path: Path, actual, expected):
    print(f'DIFF {path}:')
    print(diff(actual, expected))


def diff(actual, expected):
    if isinstance(expected, str):
        expected = expected.splitlines(keepends=True)
    if isinstance(actual, str):
        actual = actual.splitlines(keepends=True)
    return ''.join(difflib.unified_diff(expected, actual))


if __name__ == '__main__':
    main()
