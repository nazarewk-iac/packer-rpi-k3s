PACKER_VERSION ?= 1.4.5
PACKER_CONFIG ?= raspbian.json

.ONESHELL:

.PHONY: build
build: validate
	sudo PACKER_LOG=1 bin/packer build "${PACKER_CONFIG}"
	sudo chown "$(id -u):$(id -g)" raspberry-pi.img

.PHONY: validate
validate: bin/packer bin/packer-builder-arm raspbian.json
	bin/packer validate "${PACKER_CONFIG}"

raspberry-pi.img:
	$(MAKE) build

.PHONY: bake
bake: raspberry-pi.img
	[[ -b /dev/mmcblk0 ]] || exit 1
	sudo dd if=raspberry-pi.img of=/dev/mmcblk0 bs=4M status=progress

.PHONY: mount
mount: raspberry-pi.img
	bin/img mount raspberry-pi.img ./mnt-new

.PHONY: umount
umount:
	bin/img umount raspberry-pi.img


bin/packer:
	mkdir -p bin
	wget https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip
	unzip packer_${PACKER_VERSION}_linux_amd64.zip
	rm packer_${PACKER_VERSION}_linux_amd64.zip
	mv packer bin/

bin/packer-builder-arm:
	set -x
	mkdir -p bin
	git clone https://github.com/mkaczanowski/packer-builder-arm
	pushd packer-builder-arm
		go mod download
		go build
	popd
	mv packer-builder-arm/packer-builder-arm bin/
	rm -rf packer-builder-arm
