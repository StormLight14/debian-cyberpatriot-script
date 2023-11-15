# Debian and Ubuntu script for CyberPatriot

import os

# update apt repos and install package upgrades
os.system("sudo apt update && sudo apt upgrade")

# enable auto update
print("todo")

# install (if it for some reason isnt) and enable ufw
os.system("sudo apt install ufw")
os.system("sudo ufw enable")

# disable root ssh login by replacing text in config
os.system("sudo sed -i \"s/PermitRootLogin yes/PermitRootLogin no/g\" /etc/ssh/sshd_config")

# search for media files, prompt whether to delete or not
print("todo")

# disable anonymous ftp login
print("todo")

# enable ssl for ftp
print("todo")

# set mininum password age
print("todo")
