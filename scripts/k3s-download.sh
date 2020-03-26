#!/usr/bin/env bash
set -xeEuo pipefail

K3S_TAG="${K3S_TAG:-"v1.17.4%2Bk3s1"}"

curl -sfL "https://github.com/rancher/k3s/releases/download/${K3S_TAG}/k3s-arm64" -o /usr/local/bin/k3s
chmod +x /usr/local/bin/k3s

mkdir -p /var/lib/rancher/k3s/agent/images
cd /var/lib/rancher/k3s/agent/images
curl -sfLO "https://github.com/rancher/k3s/releases/download/${K3S_TAG}/k3s-airgap-images-arm64.tar"