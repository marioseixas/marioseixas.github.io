---
categories:
  - Tutorial
tags:
  - linux
comment: 
info: fechado.
date: '2022-01-09'
type: post
layout: post
published: true
sha: 
slug: ratpoison
title: 'Installation of ratpoison in debian'

---

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
