#!/bin/sh

# Compositor
picom &

# Theming
image=$(ls ~/.wallpapers | grep -E '(jpg|png)$' | sort -R | tail -1)
# wpg -s ~/.wallpapers/$image &
wal -i ~/.wallpapers/$image -q &

# Autostart programs
flameshot &
