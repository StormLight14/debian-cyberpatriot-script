# Debian and Ubuntu script for CyberPatriot

import os
import subprocess

# update apt repos and install package upgrades
os.system("sudo apt update && sudo apt upgrade")

# enable auto update
print("todo")

# install ufw (if it for some reason isnt installed already) and enable it
os.system("sudo apt install ufw")
os.system("sudo ufw enable")

# disable root ssh login by replacing text in config
os.system("sudo sed -i \"s/PermitRootLogin yes/PermitRootLogin no/g\" /etc/ssh/sshd_config")

# update db for locate command
os.system("sudo updatedb")

# search for media files, prompt whether to delete or not
locate_output = subprocess.getoutput("locate *.mp3") + subprocess.getoutput("locate *.mp4")

# disable anonymous ftp login
print("todo")

# enable ssl for ftp
print("todo")

# set mininum password age
print("todo")
