# Appearance and window settings

## Appearance baseline

```toml
theme = Nord Wave                # +list-themes | grep -i nord for variants
font-family = MesloLGS Nerd Font Mono
font-size = 15
cursor-style = block
cursor-style-blink = false

font-thicken = true              # firms up text on retina without going bold
font-thicken-strength = 1        # 1 = lightest thickening (255 = max)
adjust-cell-height = 1           # 1px vertical breathing room

bold-is-bright = true            # bright ANSI codes render as bright (p10k, ls --color)
```

`font-thicken-strength` higher than 1 starts looking aggressive at 15pt+. Step up for smaller fonts.
Back off at 18pt+.

## Window chrome

```toml
window-padding-x = 8
window-padding-y = 6
window-padding-balance = true        # equalize when cells don't divide evenly
window-save-state = always           # restore tabs/splits on relaunch
window-inherit-working-directory = true
window-inherit-font-size = true

background-opacity = 0.96
background-blur = 20                 # macOS native vibrancy, 0-100
unfocused-split-opacity = 0.85

window-colorspace = display-p3       # Apple Silicon Retina wide-gamut
resize-overlay = after-first         # size hint only after first drag
window-step-resize = true            # cell-snap on drag-resize (macOS)
window-new-tab-position = end        # browser-convention tab placement
```

`window-colorspace = display-p3` matters for color-managed themes. Nord is defined in sRGB so colors
shift slightly under display-p3 rendering. Verify visually and switch to `srgb` if the palette looks
off.

`window-save-state = always` lets `confirm-close-surface = false` ride: kill the window, relaunch,
tabs/splits restored.

## macOS-native integration

```toml
macos-titlebar-style = transparent       # tabs break under non-native fullscreen
macos-non-native-fullscreen = padded-notch    # MBP notch-aware
macos-option-as-alt = left               # left-Option = Meta; right keeps € ç etc.
macos-window-shadow = true
```

`macos-titlebar-style = hidden` is the chromeless alternative: more screen, no tabs visible. Pick one
per the tab vs screen-real-estate trade.
