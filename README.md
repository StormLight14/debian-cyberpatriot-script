# debian-cyberpatriot-script
Basic script to get some points right off the bat for Debian/Ubuntu images.

**Unfinished and not fully tested**

## Using
If the README file on the image has a list of authorized users, fill out the `authorized-users.txt` file and make sure it isn't set to `DISABLED`.

If the script asks for a "main user", that just is whatever one the image has you logged in as.

## Todo
- [x] Colored Text (Errors, Warnings)
- [x] Update repos and packages with `apt`
- [x] Enable Auto Updates
- [x] Install/Enable UFW
- [x] Install/Enable SSH (if required)
- [x] Disable root SSH login
- [x] Update file names database
- [x] Delete unwanted media files
- [x] Disable anonymous FTP login
- [x] Enable SSL for FTP
- [x] Make `sudo` require authentication
- [x] Set good password policies (only applies to users created in the future)
- [x] Remove unauthorized users
- [x] Remove non-admins from `sudo` group
- [x] Ensure `/etc/shadow` has secure permissions on it
- [x] Disable IPv4 forwarding, if required.
- [ ] Some other things probably
