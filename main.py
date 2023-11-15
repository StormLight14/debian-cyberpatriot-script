# Debian and Ubuntu shell script for CyberPatriot

import os

# update apt repos and install package upgrades
os.system("sudo apt update && sudo apt upgrade")

# enable auto update

# install (if it for some reason isnt) and enable ufw
os.system("sudo apt install ufw")
os.system("sudo ufw enable")

# disable root ssh login

# search for media files, prompt whether to delete or not

# disable anonymous ftp login

# enable ssl for ftp

# set mininum password age
