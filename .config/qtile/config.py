# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# Load script to read colors from pywal
import pywal_colors
colors = pywal_colors.colors

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows in current stack pane
    #Key([mod], "k", lazy.layout.down()),
    #Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    #Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    #Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("kitty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # Qtile commands
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    ### Custom Keybinds for bsp layout ###
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "p", lazy.spawn('rofi -show power-menu -modi "power-menu:rofi-power-menu --choices=shutdown/reboot" \
                            -font "JetBrainsMono Nerd Font 80"\
                            -theme ~/.config/rofi/config.rasi\
                            -fullscreen')),

    # Custom keybinds
    Key([mod, "shift"], "r", lazy.spawn("rofi -show run -width 60 -theme ~/.cache/wal/colors-rofi-dark.rasi")),
    Key([], "Print", lazy.spawn("flameshot gui")),
]

# Default Layout Variable
def_layout = "bsp"

# Define Groups

group_names=[("  ",{'layout': def_layout, 'spawn':'kitty'}),
           ("  ",{'layout': def_layout}),
           ("  ",{'layout': def_layout, 'spawn':'firefox'}),
           ("  ",{'layout': def_layout, 'spawn':'kitty -e zsh -c ua-update-all'}), 
           ("  ",{'layout': def_layout, 'spawn':'kitty -e /home/daniel/mic_over_mumble/mic_over_mumble'}),
           (" ﭮ ",{'layout': def_layout, 'spawn':'discord'}),
           ("  ",{'layout': def_layout, 'spawn':'kitty -e /home/daniel/.local/bin/yterm'}),
           ("  ",{'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group	

# Append a Scratchpad group
groups.append(
    ScratchPad(
        "scratchpad", [
            # Define a drop down terminal
            # It is placed in the upper third of the screen by default
            DropDown(
                "kitty",
                "/usr/bin/kitty",
                opacity=0.88,
                height=0.55,
                width=0.80
            ),

            # Define another terminal exclusively for qshell at different position
            DropDown(
                "qshell",
                "/usr/bin/kitty -e qshell",
                x=0.05,
                y=0.4,
                width=0.9,
                height=0.6,
                opacity=0.9,
                on_focus_lost_hide=True
            ),
        ]
    )
)

# Define keys to toggle the dropdown terminals
keys.extend([
    Key([], "F12", lazy.group["scratchpad"].dropdown_toggle("kitty")),
    Key([], "F11", lazy.group["scratchpad"].dropdown_toggle("qshell")),
])

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 2,
                "margin": 5,
                "border_focus": "3BB2E2",
                "border_normal": colors[5],
                }

layouts = [
    layout.Bsp(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

### COLORS ###

# colors = ["003b4c",     # Background
#         "66a5ad",       # Current group 
#         "ececec",       # Highlight Text
#         "999999",       # Dark Text
#         "73b8bf",       # Widget 1 Color
#         "50a5af",       # Widget 2 Color
#         "40848c",       # Widget 3 Color
#         "306369",       # Widget 4 Color
#         "204246",       # Widget 5 Color
#         "102123",       # Widget 6 Color

#         ]

# Define the foreground (text) color
fgcolor = colors[0]

widget_defaults = dict(
    font='Fira Code Nerd Font',
    fontsize=15,
    padding=3,
    background = colors[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.Sep(
                #    linewidth = 0,
                #    padding = 9,
                #    ),
                widget.GroupBox(
                    rounded = False,
                    active = colors[7],     # Color of text of active group
                    inactive = colors[6],
                    highlight_method = 'block',
                    highlight_color = [colors[3], colors[4]],
                    # current_screen_border = colors[1],
                    this_current_screen_border = colors[1],
                    ),
                widget.Sep(
                    linewidth = 0,
                    padding = 20,
                    ),
                widget.Spacer(),
                widget.Net(
                    background = colors[4],
                    foreground = fgcolor,
                    format = '{down}  {up} ',
                    disconnected_message = 'N/A',
                    ),
#                widget.TextBox(
#                    " Layout:",
#                    background = colors[5],
#                    foreground = fgcolor,
#                    ),
#                widget.CurrentLayoutIcon(
#                    background = colors[5],
#                    foreground = fgcolor,
#                    scale = 0.7,
#                    padding = 8,
#                    ),
#                widget.CurrentLayout(
#                    background = colors[5],
#                    foreground = fgcolor,
#                    padding = 5,
#                    ),
                widget.Volume(
                    emoji = False,
                    background = colors[6],
                    foreground = fgcolor,
                    fmt = '墳 {}',
                    padding = 8,
                    update_interval = 0.05,
                    ),
                widget.Clock(
                    format=' %d/%m/%y  %H:%M',
                    background = colors[7],
                    foreground = fgcolor,
                    padding = 9,
                    ),
            ],
            24,
            margin = [4, 6, 1, 6],
            opacity = 0.85,
        ),
        bottom=bar.Bar(
                [
                widget.Spacer(
                    length = 10,
                    ),
                widget.Prompt(),
                widget.WindowName(),
                widget.KeyboardLayout(
                    configured_keyboards = ['us', 'us -variant colemak'],
                    display_map = {'us':'US ', 'us -variant colemak':'Colemak '},
                    ),
                widget.Systray(),
                #widget.Spacer(
                #    length = 10,
                #    ),
                widget.TextBox(
                    "⏻",
                    fontsize = 18,
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('rofi -show power-menu -modi "power-menu:rofi-power-menu --choices=shutdown/reboot" \
                            -font "JetBrainsMono Nerd Font 80"\
                            -theme ~/.config/rofi/config.rasi\
                            -fullscreen')
                            },
                    padding = 10,
                    ),
                ],
            26,
            margin = [1, 6, 4, 6],
            opacity = 0.85,
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
