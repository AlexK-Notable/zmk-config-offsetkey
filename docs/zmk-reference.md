# ZMK Keymap Reference

Quick reference for editing your Offsetkey keymap.

---

## Basic Syntax

```
&behavior PARAM1 PARAM2
```

Examples:
- `&kp A` → press A key
- `&mt LSHIFT D` → hold=Shift, tap=D
- `&mo 1` → momentary layer 1
- `&none` → do nothing
- `&trans` → transparent (use layer below)

---

## Key Press Behaviors

| Behavior | Syntax | Description |
|----------|--------|-------------|
| `&kp` | `&kp KEYCODE` | Press a key |
| `&mt` | `&mt MOD KEY` | Mod-tap: hold=mod, tap=key |
| `&lt` | `&lt LAYER KEY` | Layer-tap: hold=layer, tap=key |
| `&kt` | `&kt KEY` | Toggle key on/off |
| `&sk` | `&sk MOD` | Sticky key (one-shot mod) |
| `&sl` | `&sl LAYER` | Sticky layer (one-shot) |
| `&caps_word` | `&caps_word` | Caps until space/non-alpha |
| `&key_repeat` | `&key_repeat` | Repeat last key |

---

## Layer Behaviors

| Behavior | Syntax | Description |
|----------|--------|-------------|
| `&mo` | `&mo LAYER` | Momentary (hold to activate) |
| `&lt` | `&lt LAYER KEY` | Hold=layer, tap=key |
| `&to` | `&to LAYER` | Switch to layer |
| `&tog` | `&tog LAYER` | Toggle layer on/off |
| `&sl` | `&sl LAYER` | One-shot layer |

---

## Modifiers

| Name | Aliases | Modifier Function |
|------|---------|-------------------|
| `LEFT_SHIFT` | `LSHFT`, `LSHIFT` | `LS(key)` |
| `RIGHT_SHIFT` | `RSHFT`, `RSHIFT` | `RS(key)` |
| `LEFT_CONTROL` | `LCTRL` | `LC(key)` |
| `RIGHT_CONTROL` | `RCTRL` | `RC(key)` |
| `LEFT_ALT` | `LALT` | `LA(key)` |
| `RIGHT_ALT` | `RALT` | `RA(key)` |
| `LEFT_GUI` | `LGUI`, `LWIN`, `LCMD` | `LG(key)` |
| `RIGHT_GUI` | `RGUI`, `RWIN`, `RCMD` | `RG(key)` |

Combine: `LC(LS(A))` = Ctrl+Shift+A

---

## Common Keycodes

### Letters & Numbers
`A`-`Z`, `N0`-`N9` (or `NUMBER_0`-`NUMBER_9`)

### Symbols
| Key | Name | Shifted |
|-----|------|---------|
| `` ` `` | `GRAVE` | `TILDE` |
| `-` | `MINUS` | `UNDER` |
| `=` | `EQUAL` | `PLUS` |
| `[` | `LBKT` | `LBRC` `{` |
| `]` | `RBKT` | `RBRC` `}` |
| `\` | `BSLH` | `PIPE` |
| `;` | `SEMI` | `COLON` |
| `'` | `SQT` | `DQT` |
| `,` | `COMMA` | `LT` `<` |
| `.` | `DOT` | `GT` `>` |
| `/` | `FSLH` | `QMARK` |

### Whitespace & Editing
| Name | Aliases |
|------|---------|
| `SPACE` | `SPC` |
| `ENTER` | `RET` |
| `TAB` | |
| `BACKSPACE` | `BSPC` |
| `DELETE` | `DEL` |
| `ESCAPE` | `ESC` |
| `INSERT` | `INS` |

### Navigation
| Name | Aliases |
|------|---------|
| `UP_ARROW` | `UP` |
| `DOWN_ARROW` | `DOWN` |
| `LEFT_ARROW` | `LEFT` |
| `RIGHT_ARROW` | `RIGHT` |
| `HOME` | |
| `END` | |
| `PAGE_UP` | `PG_UP` |
| `PAGE_DOWN` | `PG_DN` |

### Function Keys
`F1` - `F24`

### Locks
`CAPS` (Caps Lock), `SCROLLLOCK`, `NUMLOCK`, `PSCRN` (Print Screen)

---

## Bluetooth

Include: `#include <dt-bindings/zmk/bt.h>`

| Command | Description |
|---------|-------------|
| `&bt BT_CLR` | Clear current profile bond |
| `&bt BT_CLR_ALL` | Clear all profile bonds |
| `&bt BT_NXT` | Next profile |
| `&bt BT_PRV` | Previous profile |
| `&bt BT_SEL 0` | Select profile 0-4 |
| `&bt BT_DISC 0` | Disconnect profile 0-4 |

---

## RGB Underglow

Include: `#include <dt-bindings/zmk/rgb.h>`

| Command | Description |
|---------|-------------|
| `&rgb_ug RGB_ON` | Turn on |
| `&rgb_ug RGB_OFF` | Turn off |
| `&rgb_ug RGB_TOG` | Toggle on/off |
| `&rgb_ug RGB_EFF` | Next effect |
| `&rgb_ug RGB_EFR` | Previous effect |
| `&rgb_ug RGB_HUI` | Increase hue |
| `&rgb_ug RGB_HUD` | Decrease hue |
| `&rgb_ug RGB_SAI` | Increase saturation |
| `&rgb_ug RGB_SAD` | Decrease saturation |
| `&rgb_ug RGB_BRI` | Increase brightness |
| `&rgb_ug RGB_BRD` | Decrease brightness |
| `&rgb_ug RGB_SPI` | Increase speed |
| `&rgb_ug RGB_SPD` | Decrease speed |

---

## Mouse (Pointing)

Include: `#include <dt-bindings/zmk/pointing.h>`

Enable in .conf: `CONFIG_ZMK_POINTING=y`

| Command | Description |
|---------|-------------|
| `&mkp LCLK` | Left click |
| `&mkp RCLK` | Right click |
| `&mkp MCLK` | Middle click |
| `&mkp MB4` | Back button |
| `&mkp MB5` | Forward button |
| `&mmv MOVE_UP` | Move cursor up |
| `&mmv MOVE_DOWN` | Move cursor down |
| `&mmv MOVE_LEFT` | Move cursor left |
| `&mmv MOVE_RIGHT` | Move cursor right |
| `&msc SCRL_UP` | Scroll up |
| `&msc SCRL_DOWN` | Scroll down |
| `&msc SCRL_LEFT` | Scroll left |
| `&msc SCRL_RIGHT` | Scroll right |

---

## Media & Consumer

| Name | Description |
|------|-------------|
| `C_MUTE` | Mute |
| `C_VOL_UP` / `C_VOLUME_UP` | Volume up |
| `C_VOL_DN` / `C_VOLUME_DOWN` | Volume down |
| `C_PP` / `C_PLAY_PAUSE` | Play/Pause |
| `C_NEXT` | Next track |
| `C_PREV` | Previous track |
| `C_STOP` | Stop |
| `C_BRI_UP` | Brightness up |
| `C_BRI_DN` | Brightness down |

---

## System

| Command | Description |
|---------|-------------|
| `&sys_reset` | Reset keyboard |
| `&bootloader` | Enter bootloader (for flashing) |
| `&soft_off` | Soft power off |

---

## Custom Hold-Tap (like in your keymap)

```c
behaviors {
    ltq: ltq {
        compatible = "zmk,behavior-hold-tap";
        label = "LTQ";
        bindings = <&mo>, <&kp>;  // hold=layer, tap=keypress
        #binding-cells = <2>;
        tapping-term-ms = <200>;  // hold threshold
        quick-tap-ms = <180>;     // quick tap window
    };
};
```

Usage: `&ltq 1 BACKSPACE` → hold=layer 1, tap=backspace

---

## Combos

```c
combos {
    compatible = "zmk,combos";

    my_combo {
        bindings = <&kp ESC>;
        key-positions = <0 1>;  // which keys trigger
        timeout-ms = <50>;      // optional
        layers = <0>;           // optional: limit to layers
    };
};
```

---

## Your Offsetkey Layout

```
╭────┬────┬────┬────┬────┬────╮              ╭────┬────┬────┬────┬────┬────┬────┬────╮
│ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │              │ 6  │ 7  │ 8  │ 9  │10  │11  │12  │13  │ 14
├────┼────┼────┼────┼────┼────┤              ├────┼────┼────┼────┼────┼────┼────┼────┤
│15  │16  │17  │18  │19  │20  │              │21  │22  │23  │24  │25  │26  │27  │28  │ 29  30
├────┼────┼────┼────┼────┼────┤              ├────┼────┼────┼────┼────┼────┼────┼────┤
│31  │32  │33  │34  │35  │36  │              │37  │38  │39  │40  │41  │42  │43  │    │ 44
├────┼────┼────┼────┼────┼────┤              ├────┼────┼────┼────┼────┼────┼────┼────┤
│45  │46  │47  │48  │49  │50  │              │51  │52  │53  │54  │55  │56  │57  │58  │ 59
├────┼────┼────┼────┼────┼────┤              ├────┼────┼────┼────┼────┼────┼────┼────┤
│60  │61  │62  │63  │    │64  │              │    │65  │66  │67  │68  │69  │70  │71  │ 72
├────┼────┼────┼────┼────┼────┤  ENCODER     ├────┼────┼────┼────┼────┼────┼────┼────┤
│73  │74  │75  │76  │77  │78  │              │79  │80  │81  │82  │    │    │    │    │ TRACKPOINT
╰────┴────┴────┴────┴────┴────╯              ╰────┴────┴────┴────┴────┴────┴────┴────╯

Bootloader combo: keys 0 + 11 (ESC + BSPC)
```

---

## Docs

- Full docs: https://zmk.dev/docs
- Keycodes: https://zmk.dev/docs/keymaps/list-of-keycodes
- Behaviors: https://zmk.dev/docs/keymaps/behaviors
