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
sha: 9cf6a86094683e1c4872ee71b65755e8cb71bdc1
slug: ratpoisonrc
title: /root/.ratpoisonrc

---

```
#brightnessctl feh unclutter firefox geary viewnior rxvt-unicode rnano thunar gsimplecal catfish xfce4-screenshooter neofetch htop wifish amixer dmenu

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

exec feh --bg-center /root/Imagens/wp.png

exec unclutter

exec rpws init 4 -k

bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"

bind f exec firefox

bind F2 exec geary

bind v exec viewnior

bind e exec mousepad

bind s-e exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls -e rnano -S -i -O -x -w -m

bind c exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 10x20 -ls

bind t exec thunar

bind g exec gsimplecal

bind s-c exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls

bind Escape abort

bind apostrophe help

bind End exec pm-suspend

bind KP_Separator exec /usr/bin/chromium-browser --profile-directory=Default --app-id=khknmpnbcfnenmadanigadgaabebblip

bind KP_0 exec /usr/bin/chromium-browser --profile-directory=Default --app-id=kjnpgmkbjlilfafkkdpehnefjpocheed

bind KP_1 exec /usr/bin/chromium-browser --profile-directory=Default --app-id=glpafmialolpdohgeinpjffpbnjjfhhc

bind KP_2 exec /usr/bin/chromium-browser --profile-directory=Default --app-id=cjmkdloaeckmnapbbnofepkincodpoeh

bind KP_3 exec /usr/bin/chromium-browser --profile-directory=Default --app-id=ogjlbiopdidgogioefmnmeelgkidmfoo

bind 1 only

bind 2 hsplit

bind 3 vsplit

bind 4 resize

bind r remove

bind space exec dmenu_run

bind F10 exec amixer set Master 25%-

bind F11 exec amixer set Master 25%+

bind F9 exec amixer set Master 0

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

bind F5 exec rxvt-unicode -fg silver -sl 1000 -vb +sb -b 0 -tr -sh 25 -fade 30 -font 12x24 -ls -hold -e bash /root/Documentos/timer.sh
```