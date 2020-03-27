#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

init_path = Path('/etc/init.d/generate_hostname_once')
init_content = f'''
#!/bin/sh
### BEGIN INIT INFO
# Provides:          {init_path.name}
# Required-Start:
# Required-Stop:
# Default-Start: 1 2 3
# Default-Stop:
# Short-Description: Resize the root filesystem to fill partition
# Description:
### END INIT INFO
. /lib/lsb/init-functions
case "$1" in
  start)
    log_daemon_msg "Starting {init_path.name}"
    echo -n "rpi-$(uuid)" > /etc/hostname &&
    update-rc.d {init_path.name} remove &&
    rm {init_path} &&
    log_end_msg $?
    ;;
  *)
    echo "Usage: $0 start" >&2
    exit 3
    ;;
esac
'''


def main():
    os.environ['DEBIAN_FRONTEND'] = 'noninteractive'

    commands = [
        'apt update',
        'apt upgrade -y',
        'apt install -y vim zsh uuid',
        'apt autoremove -y',
        'apt autoclean -y',
        'wget -O /etc/zsh/zshrc https://git.grml.org/f/grml-etc-core/etc/zsh/zshrc',
        'wget -O /etc/skel/.zshrc  https://git.grml.org/f/grml-etc-core/etc/skel/.zshrc',
    ]
    for cmd in commands:
        subprocess.run(cmd.split())

    init_path.write_text(init_content)
    init_path.chmod(0o755)


if __name__ == '__main__':
    main()
