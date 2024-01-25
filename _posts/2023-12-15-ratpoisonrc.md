---
categories:
  - Dotfiles
tags:
  - linux
comment: 
info: aberto.
date: '2023-12-15'
type: post
layout: post
published: true
sha: 
slug: ratpoisonrc
title: .ratpoisonrc

---

```
set fgcolor black
set bgcolor silver
set framesels 123456789
set font -xos4-terminus-medium-r-normal-*-*-140-*-*-c-*-iso8859-1
set border 0
set barborder 0
set barpadding 0 0
set winname class
set winfmt %n %s %c
set winliststyle column
set wingravity n 
set gravity center 
set transgravity center
set bargravity ne
set waitcursor 1
set padding 0 0 0 0

startup_message off
escape Super_L
banish

unmanage rpbar

exec brightnessctl s 7
exec unclutter
exec rpws init 9 -k
exec pcmanfm-qt --desktop
exec systemctl start performance_governors.service

definekey top M-Tab next
definekey top M-ISO_Left_Tab prev

bind F1 only
bind F2 hsplit
bind F3 vsplit
bind F4 resize
bind y exec freetube --no-sandbox 
bind apostrophe exec zutty -saveLines 50000 -border 0 -font 10x20
bind s-apostrophe exec zutty -saveLines 50000 -border 0 -font 12x24
bind e exec xnc
bind f exec thorium-browser --no-sandbox --flag-switches-begin --enable-features=ChromeRefresh2023,ScrollableTabStrip --flag-switches-end --disable-nacl --use-gl=angle --use-angle=gl-egl --enable-unsafe-webgpu
bind s-f exec min --no-sandbox
bind c exec gsimplecal
bind s-c exec galculator
bind i exec zutty -saveLines 50000 -border 0 -font 10x20 -e wifish
bind p exec xfce4-screenshooter
bind s-p exec thermal.sh
bind r remove
bind t exec pcmanfm-qt --daemon-mode
bind v exec viewnior
bind w exec ratpoison -c "select `ratpoison -c "windows" | dmenu | awk '{print $1}'`"
bind b exec zutty -saveLines 50000 -border 0 -font 10x20 -e bpytop
bind z nextscreen
bind s-b exec vorta
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
bind KP_0 exec xdotool key apostrophe key apostrophe key apostrophe
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
