---
categories:
  - Dotfiles
tags:
  - linux
comment: 
info: fechado.
date: '2021-05-25'
type: post
layout: post
published: true
sha: f0bb67137c01ab23f366aaec5a7ea982daa2f58f
slug: ratpoisonrc
title: /root/.ratpoisonrc

---
```
set fgcolor black

set bgcolor silver

set framesels 123456789

set font -xos4-terminus-medium-r-normal-*-*-140-*-*-c-*-iso8859-1

set border 0

set barborder 0

set padding 0 0 0 0

set barpadding 0 0

set winname class

set winfmt %n %s %c

set winliststyle column

set wingravity n 

set gravity center 

set transgravity center

set bargravity nw

startup_message off

escape Super_L

exec brightnessctl s 7

exec feh --bg-fill /home/mario/images/marriage.png

exec unclutter

exec rpws init 4 -k

bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"

bind f exec firefox

bind m exec geary

bind v exec viewnior

bind e exec mousepad

bind s-e exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls -e rnano -S -i -O -x -w -m

bind c exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls

bind t exec thunar

bind g exec gsimplecal

bind s-c exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls

bind Escape abort

bind apostrophe help

bind F2 exec pm-suspend

bind 1 only

bind 2 hsplit

bind 3 vsplit

bind 4 resize

bind r remove

bind space exec dmenu_run

bind XF86AudioLowerVolume exec amixer set Master 25%-

bind XF86AudioRaiseVolume exec amixer set Master 25%+

bind XF86AudioMute exec amixer set Master 0

bind XF86WebCam exec reboot

bind s-Return prev

bind BackSpace undo

bind s-BackSpace redo

bind s-k kill

bind Tab focus

bind s-Tab focuslast

bind s-Left exchangeleft

bind s-Right exchangeright

bind s-Up exchangeup

bind s-Down exchangedown

bind s-x fselect

bind s exec catfish

bind p exec xfce4-screenshooter

bind b exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e neofetch

bind s-b exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e htop

bind i exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e wifish
```