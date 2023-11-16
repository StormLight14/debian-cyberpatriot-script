# Debian and Ubuntu script for CyberPatriot

import os
import subprocess

if subprocess.getoutput("whoami") != "root":
    print("WARNING: You are not running this script as root.")
    run_anyway = input("Run script anyway? (y/n)").lower()

    if run_anyway == "y" or run_anyway == "yes":
        print("Running script.")
    else:
        print("Exiting.")
        exit()

# update apt repos and install package upgrades
os.system("sudo apt update && sudo apt upgrade")

# install unattended-upgrades and enable auto update
os.system("sudo apt install unattended-upgrades")

# install ufw (if it for some reason isnt installed already) and enable it
os.system("sudo apt install ufw")
os.system("sudo ufw enable")
print("UFW is installed and enabled.")

# disable root ssh login by replacing text in config
os.system("sudo sed -i \"s/PermitRootLogin yes/PermitRootLogin no/g\" /etc/ssh/sshd_config")
print("Disabled root login through SSH.")

# update db for locating files
os.system("sudo updatedb")
print("Updated file name database.")

# search for media files, prompt whether to delete or not
locate_output = (subprocess.getoutput("locate *.mp3") + "\n" + subprocess.getoutput("locate *.mp4") + "\n" + subprocess.getoutput("locate *.wav")).split("\n")
for file in locate_output:
    if file != '':
        should_delete = input(f"Delete media file {file}? (y/n/stop)").lower()
        if should_delete == "y":
            try:
                print("Deleted media file.")
                os.remove(file)
            except:
                print("Failed to delete media file, please try doing it manually.")
        elif should_delete == "stop":
            print("Stopped going through media files.")
            break
        elif should_delete == "n":
            print("Did not delete media file.")
        else:
            print("Invalid input; defaulted to not deleting.")

# disable anonymous ftp login
os.system("sudo sed -i \"s/anonymous_enable=YES/anonymous_enable=NO/g\" /etc/vsftpd.conf")
print("Disabled vsftpd anonymous_enable")

# enable ssl for ftp
os.system("sudo sed -i \"s/ssl_enable=NO/ssl_enable=YES/g\" /etc/vsftpd.conf")
print("Enabled vsftpd ssl_enable")

# set good password aging policies
with open('/etc/login.defs', 'r') as file:
    lines = file.readlines()
    
    # iterate through lines in login.defs
    for i, line in enumerate(lines): 
        if line.startswith("PASS_MAX_DAYS"):
            lines[i] = "PASS_MAX_DAYS 90\n"
        elif line.startswith("PASS_MIN_DAYS"):
            lines[i] = "PASS_MIN_DAYS 7\n"
        elif line.startswith("PASS_WARN_AGE"):
            lines[i] = "PASS_WARN_AGE 5\n"

    # write changes to login.defs
    with open('/etc/login.defs', 'w') as file:
        file.writelines(lines)

print("Set system password aging policies.")
