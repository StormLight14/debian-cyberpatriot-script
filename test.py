import subprocess

sudo_users = subprocess.getoutput("awk -F\':\' \'/sudo/{print $4}\' /etc/group")
print(sudo_users)
