#! /bin/sh

GETSTATE=$(bspc query --node focused.floating --nodes | wc -c)

if [[ $GETSTATE -ne 0 ]]; then
    STATE="Floating"
else
    STATE="Tiled"
fi

if [ $STATE == "Tiled" ]; then
    bspc node focused.tiled --state floating
elif [ $STATE == "Floating" ]; then
    bspc node focused.floating --state tiled
fi
