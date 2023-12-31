# Debian and Ubuntu script for CyberPatriot

import os
import subprocess

from user import User

def print_color(text, type):
    color = '\033[0m'

    if type.lower() == "warning":
        color = '\033[93m'
    elif type.lower() == "error":
        color = '\033[91m'

    print(f"{color} {text} \033[0m")

if subprocess.getoutput("whoami") != "root":
    print_color("WARNING: You are not running this script as root.", "warning")
    run_anyway = input("Run script anyway? (y/n) ").lower()

    if run_anyway == "y":
        print("Running script.")
    else:
        print("Exiting.")
        exit()

# main_user = input("What user are you logged in as? ")

required_services = []

if input("Is FTP required? (y/n) ").lower() == "y":
    required_services.append("ftp")
if input("Is SSH required? (y/n) ").lower() == "y":
    required_services.append("ssh")
if input("Is CUPS required (printing)? (y/n) ").lower() == "y":
    required_services.append("cups")
if input("Are media files allowed? (y/n) ").lower() == "y":
    required_services.append("media")
    
# update apt repos and install package upgrades
os.system("sudo apt update && sudo apt upgrade")

# enable auto update
os.system("sudo apt install unattended-upgrades")
os.system(
    "sudo dpkg-reconfigure -plow unattended-upgrades"
)  # open interactive CLI for enabling unattended-upgrades.
os.system(
    'sudo sed -i "s/Update-Package-Lists \\"0\\"/Update-Package-Lists \\"1\\"/g" /etc/apt/apt.conf.d/10periodic'
)  # daily updates
print_color("WARNING: May need to manually change what updates you get. (Example: Security Only to Security & Recommended)", "warning")
print("Enabled auto updates.")

# install and enable ufw
os.system("sudo apt install ufw")
os.system("sudo ufw enable")
print("UFW is installed and enabled.")

# install, start and enable ssh
if "ssh" in required_services:
    os.system("sudo apt install openssh-server")
    os.system("sudo systemctl enable sshd")
    os.system("sudo systemctl start sshd")

    # disable root ssh login by replacing text in config
    os.system(
        'sudo sed -i "s/PermitRootLogin yes/PermitRootLogin no/g" /etc/ssh/sshd_config'
    )
    print("Disabled root login through SSH.")
else:
    os.system("sudo systemctl disable openssh")

# update db for locating files
os.system("sudo updatedb")
print("Updated file name database.")

if "media" not in required_services:
    # search for media files, prompt whether to delete or not
    locate_output = (
        subprocess.getoutput("locate *.mp3")
        + "\n"
        + subprocess.getoutput("locate *.mp4")
        + "\n"
        + subprocess.getoutput("locate *.wav")
        + "\n"
        + subprocess.getoutput("locate *.flac")
    ).split("\n")
    for file in locate_output:
        if file != "":
            should_delete = input(f"Delete media file {file}? (y/n/stop) ").lower()
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

if "ftp" in required_services:
    # disable anonymous ftp login
    os.system('sudo sed -i "s/anonymous_enable=YES/anonymous_enable=NO/g" /etc/vsftpd.conf')
    print("Disabled vsftpd anonymous_enable")
    
    # enable ssl for ftp
    os.system('sudo sed -i "s/ssl_enable=NO/ssl_enable=YES/g" /etc/vsftpd.conf')
    print("Enabled vsftpd ssl_enable")
    
    # require sudo to authenticate
    os.system('sudo sed -i "s/!authenticate/authenticate/g" /etc/sudoers')
    print("Enabled sudo requiring authentication.")
    print_color("WARNING: Double check /etc/sudoers.", "warning")
else:
    os.system("sudo systemctl disable vsftpd")

if "cups" in required_services:
    pass
else:
    os.system("sudo systemctl disable cups")

common_password_str = ""

# save contents of common-password to a variable
with open("/etc/pam.d/common-password", "r") as common_password_file:
    common_password_str = common_password_file.read()

# remember previous passwords and extra dictionary-based strength tests added
# TODO: make it not duplicate the settings.. I CANT FIGURE OUT WHY IT IS DUPLICATING ANYWAY ARGHHHHHHHHHHHH
try:
    with open("/etc/pam.d/common-password", "a") as common_password_file:
        if "pam_pwquality.so" not in common_password_str:
            common_password_file.write("\npassword requisite pam_pwquality.so\n")
        if "pam_unix.so remember" not in common_password_str:
            common_password_file.write("\npassword required pam_unix.so remember=5\n")

        print("Set better password strength (Extra dictionary-based checks)")
        print("Set setting for remembering past passwords.")
        print_color("WARNING: Please check /etc/pam.d/common-password for any conflicts this may have made.", "warning")
except:
    print_color("ERROR: Failed to edit /etc/pam.d/common-password; it may not exist.", "warning")

users = []

# get all users on system and append to users list
with open("/etc/passwd", "r") as passwd_file:
    with open("authorized-users.txt", "r") as authorized_users:
        auth_user_names = []
        admin_user_names = []

        sudo_users = subprocess.getoutput(
            "getent group sudo | awk -F: '{print $1 \":\" $NF}'"
        )

        read_mode = None  # can be None, ADMINS, or NORMAL_USERS

        for line in authorized_users.readlines():
            if line.strip() != "":
                if line.strip() == "DISABLED":
                    print_color("WARNING: authorized-users.txt is set to DISABLED. Stop the script if this isn't the intended behavior.", "warning")
                    auth_user_names.append("DISABLED")
                    break
                elif "ADMINS" in line.strip():
                    read_mode = "ADMINS"
                elif "NORMAL_USERS" in line.strip():
                    read_mode = "NORMAL_USERS"

                if read_mode == "NORMAL_USERS":
                    auth_user_names.append(line.strip())
                if read_mode == "ADMINS":
                    auth_user_names.append(line.strip())
                    admin_user_names.append(line.strip())

        for line in passwd_file.readlines():
            if "/home/" in line:  # have mostly actual users
                user_name = line.split(":")[0]
                user_is_authed = False
                user_is_admin = False
                user_has_sudo = False

                if user_name in auth_user_names or auth_user_names[0] == "DISABLED":
                    user_is_authed = True
                if user_name in admin_user_names:
                    user_is_admin = True
                if user_name in sudo_users:
                    user_has_sudo = True

                users.append(
                    User(user_name, user_is_authed, user_is_admin, user_has_sudo)
                )

# set good password aging policies for future users
try:
    with open("/etc/login.defs", "r") as logindefs_file:
        lines = logindefs_file.readlines()

        # iterate through lines in login.defs and set different values.
        for i, line in enumerate(lines):
            if line.startswith("PASS_MAX_DAYS"):
                lines[i] = "PASS_MAX_DAYS 90\n"
            elif line.startswith("PASS_MIN_DAYS"):
                lines[i] = "PASS_MIN_DAYS 7\n"
            elif line.startswith("PASS_WARN_AGE"):
                lines[i] = "PASS_WARN_AGE 5\n"

        # write changes to login.defs
        with open("/etc/login.defs", "w") as file:
            file.writelines(lines)
        print("Set system password aging policies for future users.")

except:
    print_color("ERROR: Failed to read/write /etc/login.defs", "error")

# set good password aging policies for current users
""" DISABLED UNTIL FIXED, because I ended up soft locking sudo authentication after running it...
for user in users:
    if user != "root" and user != "main_user":
        os.system(f"sudo chage --mindays 7 --maxdays 90 --warndays 5 {user}")

    print("Set system password aging policies for current users.")

"""

# check if any users are unauthorized on the system and ask whether to delete or not
for user in users:
    if user.is_authorized == False:
        remove_user = input(
            f"Remove user {user.username}? They are not in authorized_users.txt. WARNING: Double check before answering! (y/n) "
        ).lower()
        if remove_user == "y":
            os.system(f"sudo userdel {user.username}")
            print(f"Removed user {user.username}")
        elif remove_user == "n":
            print("Not removing user.")
        else:
            print("Invalid input; defaulting to not removing user.")

    if user.has_sudo and user.is_admin == False:
        remove_sudo = input(
            f"Remove user {user.username} from sudo group? Check the administrator list. (y/n)"
        ).lower()
        if remove_sudo == "y":
            os.system(f"sudo deluser {user.username} sudo")
            print(f"Removed {user.username} from sudo group.")
        else:
            print(f"Did not remove {user.username} from sudo.")

# ensure /etc/shadow has correct file permissions.
# owner has rw perms, owner's group has r perms, all others have no perms.
os.system("sudo chmod 640 /etc/shadow")
os.system("sudo chmod 640 ~/.bash_history")

# ask user whether to disable ipv4 forwarding or not
disable_ip_forward = input(
    "Disable IPv4 Forwarding? You can always change this later in /etc/sysctl.conf (y/n) "
).lower()
if disable_ip_forward == "y":
    os.system(
        'sudo sed -i "s/net.ipv4.ip_forward=1/net.ipv4.ip_forward=0/g" /etc/sysctl.conf'
    )
    print("Disabled IPv4 forwarding.")
else:
    print("Leaving IPv4 forwarding settings at default.")
