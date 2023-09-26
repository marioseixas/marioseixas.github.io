---
categories:
  - Tutorial
tags:
  - linux
comment: 
info: fechado.
date: '2023-09-25'
type: post
layout: post
published: true
sha: 
slug: ratpoison
title: 'Installation of ratpoison in debian/ubuntu'

---

How to make Ratpoison your only window manager:

1. Go through the Ubuntu installation process as you typically would. Once you reach the desktop, open up a Terminal.

2. Update your system:

```bash
sudo apt-get update && sudo apt-get upgrade
```

3. Install Ratpoison window manager:

```bash
sudo apt-get install ratpoison
```

4. Now, you want Ratpoison to be your default session. You can configure this in the `.xinitrc` file in your home directory:

```bash
nano ~/.xinitrc
```

5. If there is no `.xinitrc` file, creating one with the following command:

```bash
touch ~/.xinitrc
```

6. Insert the following line and save the file:

```bash
exec ratpoison
```

7. Give the `.xinitrc` file the necessary permissions:

```bash
chmod +x ~/.xinitrc
```

8. To ensure Ratpoison starts on boot, you need to install `xinit`, which is a handy and lightweight display manager:

```bash
sudo apt-get install xinit
```

9. If you want to get rid of the existing window managers or desktop environments, starting with GNOME, execute:

```bash
sudo apt-get purge ubuntu-desktop gnome-shell
```

10. Following that, to remove all the related packages and dependencies, use:

```bash
sudo apt-get autoremove
```

11. To check if other desktop environments or window manager are installed, make sure Aptitude is installed:

```bash
sudo apt install aptitude
```

12. Then run a command like this for each potential desktop package:

```bash
aptitude search '?installed(?name(gnome-shell))'
```

Change "gnome-shell" to the package name of the desktop you are searching for. If it returns nothing, the package isn't installed.

13. If you find another installed desktop environment or window manager, substitute "gnome-shell" in the purge command above with the corresponding packages.

14. Once you're certain all other desktop environments are purged, reboot your machine:

```bash
sudo reboot
```

***

# Create ratpoison.desktop file in /usr/share/xsessions/
[Desktop Entry]

Version=1.0

Encoding=UTF-8

Name=ratpoison

Name[en_US]=ratpoison

Comment=Simple and fast window manger

Exec=ratpoison

TryExec=ratpoison

Type=Xsession


[Window Manager]

SessionManaged=true

# Make a symbolic link of /usr/bin/ratpoison file in /etc/alternatives/
`sudo ln -s /usr/bin/ratpoison /etc/alternatives/x-window-manager`

`sudo ln -s /usr/bin/ratpoison /etc/alternatives/x-session-manager`
