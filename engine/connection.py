"""Creates an SSH Connction between the Raspberrypi and serving device"""
import paramiko
import sys


def createConnection(ip='', port=22, uname='', password='', command=''):
    """
    Takes in 
    - ip address of the client.
    - port to ssh.
    - username of client
    - login passkey
    - command to execute
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=port, username=uname, password=password)
    inp, out, error = ssh.exec_command(command)
    output, error = out.readlines(), error.readlines()
    return(inp, output, error)

ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
command = "./client.py"



ins,outs,errors = createConnection(ip,22,user,password,command)
