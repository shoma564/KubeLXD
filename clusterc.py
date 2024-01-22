#!/usr/bin/env python3
#pip install paramiko
#pip install scp

import paramiko, os, sys, subprocess, glob, scp


def workerfunc(masterip, masteruser, masterpass, workerhost, workerip, workeruser, workerpass):
    print(">>>>> workerfunc")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(masterip, username=masteruser, password=masterpass, timeout=5.0)
    command = "lxc cluster add " + str(workerhost)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')
    com = com.replace("\n", "")


    with paramiko.SSHClient() as sshc:
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname=workerip, port=22, username=workeruser, password=workerpass)
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put("lxdconfig-worker", "/root/")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(workerip, username=workeruser, password=workerpass, timeout=5.0)
    command = "sed -e \"s#token_here#" + str(com) + "#g\" -i /root/lxdconfig-worker"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')

    command = "cat /root/lxdconfig-worker | lxd init"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')


    



def masterfunc(masterip, masteruser, masterpass):
    print(">>>>> masterfunc")
    with paramiko.SSHClient() as sshc:
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname=masterip, port=22, username=masteruser, password=masterpass)

        # SCPによるput処理
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put("lxdconfig-master", "/root/")
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(masterip, username=masteruser, password=masterpass, timeout=5.0)
        command = "cat /root/lxdconfig-master | lxd init"
        stdin, stdout, stderr = client.exec_command(command, timeout=5)
        for com in stdout:
            print(com, end='')
    





def splitline():
    mastercount = 0

    with open('lxdclusterfile') as f:
        for line in f:
            linesplit = line.split()
            print(linesplit[0])
            print(linesplit[1])
            print(linesplit[2])
            print(linesplit[3])
            
            if mastercount > 0:
                workerfunc(master_ip, master_user, master_pass, linesplit[0], linesplit[1], linesplit[2], linesplit[3])

            elif mastercount == 0:
                
                master_host = linesplit[0]
                master_ip = linesplit[1]
                master_user = linesplit[2]
                master_pass = linesplit[3]

                masterfunc(master_ip, master_user, master_pass)
                mastercount = mastercount + 1





splitline()