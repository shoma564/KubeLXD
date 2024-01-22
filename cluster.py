#!/usr/bin/env python3

#pip install paramiko
#pip install scp

import paramiko, os, sys, subprocess, glob, scp

linesplit = None
com = None


def countline():
    global count
    count = 0
    with open('lxdclusterfile') as f:
        for line in f:
            count += 1
    return count



def scpfile(desip, sendfile):
    print(">>>>> scpfile")
    print(sendfile)
    with paramiko.SSHClient() as sshc:
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname=desip, port=22, username=linesplit[2], password=linesplit[3])

        # SCPによるput処理
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put(sendfile, "/root/")



def sshmaster():
    global linesplit
    print("sshmaster")

    scpfile(linesplit[1], "lxdconfig-master")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(linesplit[1], username=linesplit[2], password=linesplit[3], timeout=5.0)
    command = "cat /root/lxdconfig-master | lxd init"
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')




def sshworkerconfiggen(token):
    global linesplit

    token = token.replace('\n', '')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(linesplit[1], username=linesplit[2], password=linesplit[3], timeout=5.0)
    command = "sed -e \"s#token_here#" + str(token) + "#g\" -i /root/lxdconfig-worker"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(linesplit[1], username=linesplit[2], password=linesplit[3], timeout=5.0)
    command = "cat /root/lxdconfig-worker | lxd init"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')




def sshmastertokengen(lxchostname):
    global linesplit, com

    scpfile(linesplit[1], "lxdconfig-master")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(linesplit[1], username=linesplit[2], password=linesplit[3], timeout=5.0)
    command = "lxc cluster add " + str(lxchostname)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')
    sshworkerconfiggen(com)





def sshworker():
    global linesplit

    scpfile(linesplit[1], "lxdconfig-worker")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(linesplit[1], username=linesplit[2], password=linesplit[3], timeout=5.0)
    command = "cat /root/lxdconfig-worker | lxd init"
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')




def splitline():
    global linesplit, com
    master = 0
    with open('lxdclusterfile') as f:
        for line in f:
            linesplit = line.split()
            print(linesplit[0])
            print(linesplit[1])
            print(linesplit[2])
            print(linesplit[3])
            print(master)

            if master > 0:
                print(">>>>>>>>>>> sshworker")
                sshworker()

            elif master == 0:
                sshmaster()
                master = master + 1
            print("\n\n\n\n")
            print(linesplit[0])
            sshmastertokengen(linesplit[0])
            print("\n\n\n\n\n\n\n")

            print("\n\n\n\n\n\n")


def main():
    countline()
    print(count)
    splitline()
    


main()
