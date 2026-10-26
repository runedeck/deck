# Appearance and window settings

## Appearance baseline

```toml
# +list-themes | grep -i nord for variants
theme = Nord Wave
font-family = MesloLGS Nerd Font Mono
font-size = 15
cursor-style = block
cursor-style-blink = false

# firms up text on retina without going bold
font-thicken = true
# 1 = lightest thickening (255 = max)
font-thicken-strength = 1
# 1px vertical breathing room
adjust-cell-height = 1

# bright ANSI codes render as bright (p10k, ls --color)
bold-is-bright = true
```

`font-thicken-strength` higher than 1 starts looking aggressive at 15pt+. Step up for smaller fonts.
Back off at 18pt+.

## Window chrome

```toml
window-padding-x = 8
window-padding-y = 6
# equalize when cells don't divide evenly
window-padding-balance = true
# restore tabs/splits on relaunch
window-save-state = always
window-inherit-working-directory = true
window-inherit-font-size = true

background-opacity = 0.96
# macOS native vibrancy, 0-100
background-blur = 20
unfocused-split-opacity = 0.85

# Apple Silicon Retina wide-gamut
window-colorspace = display-p3
# size hint only after first drag
resize-overlay = after-first
# cell-snap on drag-resize (macOS)
window-step-resize = true
# browser-convention tab placement
window-new-tab-position = end
```

`window-colorspace = display-p3` matters for color-managed themes. Nord is defined in sRGB so colors
shift slightly under display-p3 rendering. Verify visually and switch to `srgb` if the palette looks
off.

`window-save-state = always` lets `confirm-close-surface = false` ride: kill the window, relaunch,
tabs/splits restored.

## macOS-native integration

```toml
# tabs break under non-native fullscreen
macos-titlebar-style = transparent
# MBP notch-aware
macos-non-native-fullscreen = padded-notch
# left-Option = Meta; right keeps € ç etc.
macos-option-as-alt = left
macos-window-shadow = true
```

`macos-titlebar-style = hidden` is the chromeless alternative: more screen, no tabs visible. Pick one
per the tab vs screen-real-estate trade.
