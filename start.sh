#!/bin/bash


apt -y install python3-pip
lxd init --auto
lxc profile create mk8s
cat microk8s.profile | lxc profile edit mk8s

cd custom && ./operatorcopy.sh
cd ../

lxdcli build k8smaster &
sleep 30 && lxdcli build k8sworker &

wait
