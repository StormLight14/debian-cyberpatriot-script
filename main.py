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
        elif should_delete == "stop" or should_delete == "s":
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

# remember previous passwords and extra dictionary-based strength tests added
common_password_lines = []

with open("/etc/pam.d/common-password") as common_password_file:
    for line in common_password_file.readlines():
        common_password_lines.append(line)

with open("/etc/pam.d/common-password", "a+") as common_password_file:
    change_dictionary_checks = True 
    change_password_remember = True

    for line in common_password_lines:
        if "password" in line:
            if "requisite" in line and "pam_pwquality" in line:
                change_dictionary_checks = False
            if "required" in line and "pam_unix" in line:
                change_password_remember = False
    
    if change_dictionary_checks:
        common_password_file.write("\npassword requisite pam_pwquality.so\n")
        print("Set better password strength (Extra dictionary-based checks)")
    else:
        print("Password strength already good. (Most likely; still recommend manually checking /etc/pam.d/common-password)")

    if change_password_remember:
        common_password_file.write("\npassword required pam_unix.so remember=5\n")
        print("Set remembering past passwords.")
    else:
        print("Past passwords already set to be remembered (Most likely; still recommend manually checking /etc/pam.d/common-password)")


# set good password aging policies for future users
with open('/etc/login.defs', 'r') as logindefs_file:
    lines = logindefs_file.readlines()
    
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

print("Set system password aging policies for future users.")

# get all users on system, and authorized users from authorized-users.txt.
users = []
auth_users = []


# get all users on system and append to users list
with open('/etc/passwd', 'r') as passwd_file:
    for line in passwd_file.readlines():
        if "/home/" in line: # only have actual users
            users.append(line.split(":")[0]) # only take user's name from /etc/passwd

# read authorized_users.txt and append to auth_users list
with open('authorized-users.txt', 'r') as authorized_users:
    for user in authorized_users.readlines():
        auth_users.append(user.strip())

# set good password aging policies for current users
for user in users:
    os.system(f"sudo chage --mindays 7 --maxdays 90 --warndays 5 {user}")

print("Set system password aging policies for current users.")

# check if any users are unauthorized on the system and ask whether to delete or not
for auth_user in auth_users:
    if auth_user != "DISABLED":
        if auth_user not in auth_users:
            remove_user = input(f"Remove user {auth_user}? They are not in authorized_users.txt. (WARNING: Double check before answering!) (y/n)").lower()
            if remove_user == "y" or remove_user == "yes":
                pass # remove user here
            elif remove_user == "n" or remove_user == "no":
                print("Not removing user.")
            else:
                print("Invalid input; defaulting to not removing user.")
    else:
        print("authorized-users.txt is set to DISABLED. Not checking users.")
        break
