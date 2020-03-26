PACKER_VERSION ?= 1.4.5
PACKER_CONFIG ?= raspbian.json

.ONESHELL:

build: validate
	sudo PACKER_LOG=1 bin/packer build "${PACKER_CONFIG}"

validate: bin/packer bin/packer-builder-arm raspbian.json
	bin/packer validate "${PACKER_CONFIG}"

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
