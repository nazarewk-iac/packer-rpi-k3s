#!/usr/bin/env bash
set -xeEuo pipefail

ARCHIVE_PATH="${1}"
MOUNTPOINT="${2}"
pwd
cd packer_cache
unzip -n "${ARCHIVE_PATH}"
lo_device="$(losetup -f)"
img_path="${PWD}/$(echo -n *raspbian-*-lite.img)"

cd "${MOUNTPOINT}"

setup () {
  mkdir -p ./mnt
  mount "${lo_device}p2" ./mnt
  mount "${lo_device}p1" ./mnt/boot
}

teardown () {
  umount -R ./mnt
  losetup -d "${lo_device}"
  rm "${img_path}"
}

losetup -P "${lo_device}" "${img_path}"
trap teardown EXIT
setup
cp -ra ./mnt/* .
