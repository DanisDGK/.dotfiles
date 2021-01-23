#!/bin/sh

# Compositor
picom --experimental-backends &

# Theming
image=$(ls ~/.wallpapers | grep -E '(jpg|png)$' | sort -R | tail -1)
wpg -s ~/.wallpapers/$image &
wal -i ~/.wallpapers/$image -q -n &

# Autostart programs
flameshot &
