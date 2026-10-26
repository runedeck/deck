# Desktop

Commands for the X11 desktop of a Parallels agent VM. A cua Space offers the same through its `computer_*` tools.

## Run as the agent

Run GUI commands as `agent` on display `:0`. A login shell sets the agent's home, so X finds its authority file there:

```sh
prlctl exec <vm> "runuser -l agent -c 'DISPLAY=:0 <command>'"
```

A command that starts a program in the background needs a script. Use `scripts/run-in-guest.sh` and switch user inside the script.

## Look

- Screen size: `xdotool getdisplaygeometry` (1024 768 by default).
- In-guest screenshot: `scrot -o /tmp/screen.png` (about 30 ms). From the host: `prlctl capture <vm> --file shot.png`.
- Windows: `xdotool search --onlyvisible --class <app>` or `wmctrl -l`.

## Act

- Focus: `xdotool windowactivate --sync <window-id>`.
- Click: `xdotool mousemove <x> <y> click 1`.
- Type: `xdotool type --delay 30 "<text>"`, then `xdotool key Return`.
- Clipboard: `xclip -selection clipboard`.
- Before the desktop exists (installer, login), use `prlctl send-key-event <vm> --scancode <code>`.

## Read the accessibility tree

Accessibility is on at login, so GTK, Qt and Firefox build their trees. A fresh clone showed 199 nodes for Firefox.

```python
import pyatspi

desktop = pyatspi.Registry.getDesktop(0)
for app in (desktop.getChildAtIndex(i) for i in range(desktop.childCount)):
    print(app.name, app.childCount)
```

Run it as `agent` with `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus`. Prefer named elements over pixel coordinates: a name survives a layout change.

## Browser

`firefox --new-instance <url>` opens without the terms dialog. Firefox runs on X11 here, so `xdotool` and AT-SPI both reach it.
