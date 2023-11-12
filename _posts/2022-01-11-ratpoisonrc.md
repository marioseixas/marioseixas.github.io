---
categories:
  - Dotfiles
tags:
  - linux
comment: 
info: aberto.
date: '2023-11-12'
type: post
layout: post
published: true
sha: 
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
set bargravity ne
set waitcursor 1

startup_message off
escape Super_L
banish

unmanage rpbar
set padding 0 0 0 21
exec rpbar
addhook switchwin exec rpbarsend
addhook switchframe exec rpbarsend
addhook switchgroup exec rpbarsend
addhook deletewindow exec rpbarsend
addhook titlechanged exec rpbarsend
addhook newwindow exec rpbarsend

exec sudo /sbin/quectel-CM
exec sudo brightnessctl s 7
exec unclutter
exec rpws init 9 -k

definekey top M-Tab next
definekey top M-ISO_Left_Tab prev
definekey top M-i exec sudo urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e wpa_supplicant -B -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0

bind F1 only
bind F2 hsplit
bind F3 vsplit
bind F4 resize
bind b exec urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e neofetch
bind apostrophe exec urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls
bind s-apostrophe exec sudo urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls
bind e exec mousepad
bind f exec thorium-browser
bind c exec gsimplecal
bind i exec sudo urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e wifish
bind p exec xfce4-screenshooter
bind r remove
bind t exec pcmanfm-qt
bind s-t exec sudo pcmanfm-qt
bind v exec viewnior
bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"
bind s-b exec urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e htop
bind s-e exec sudo mousepad
bind s-i exec urxvt -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls -hold -e nmtui
bind s-k kill
bind s-x fselect
bind BackSpace undo
bind s-BackSpace redo
bind s-Down exchangedown
bind s-Up exchangeup
bind s-Left exchangeleft
bind s-Right exchangeright
bind s-Return prev
bind s-Tab focuslast
bind Tab focus
bind Escape abort
bind space exec dmenu_run
bind F9 exec amixer set Master 0
bind F10 exec amixer set Master 25%-
bind F11 exec amixer set Master 25%+
bind KP_0 exec sh /userdata/Documents/SCRIPTS/backticks.sh
bind KP_1 exec rpws 1
bind KP_2 exec rpws 2
bind KP_3 exec rpws 3
bind KP_4 exec rpws 4
bind KP_5 exec rpws 5
bind KP_6 exec rpws 6
bind KP_7 exec rpws 7
bind KP_8 exec rpws 8
bind KP_9 exec rpws 9

```

backticks.sh:

```

#!/bin/bash

# Copy backticks to clipboard
echo -n '```' | xclip -selection clipboard

# Small delay to make sure copying is done before pasting
sleep 0.1

# Simulate a paste command
xdotool key --clearmodifiers ctrl+v

```
