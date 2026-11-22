# Hotbar ordering and mouse dragging

Working snapshot saved on 2026-11-22, tested with Hyprland 0.56.2 and the installed Omarchy Quickshell bar. The live plugin is `~/.config/omarchy/plugins/ytuchkov.omapanel/`; the bar selects it with `id: "ytuchkov.omapanel"` in `~/.config/omarchy/shell.json`.

The sibling [ytuchkov.omapanel/](ytuchkov.omapanel/) directory contains the runtime files, editable sources, and bundler needed to restore this version. `SHA256SUMS` records the snapshot contents. The machine's shell settings and pinned-app preferences are not included.

## Expected behavior

- In a scrolling workspace, inactive pinned launchers stay on the left. Running window icons follow the tape's actual left-to-right order.
- Drag a running icon horizontally past the small threshold, then release at the insertion marker beside another running icon. This inserts the real scrolling column at that position and restores the previously focused window.
- Floating and dwindle workspaces use the regular pinned/running display and show running apps. Icon dragging only reorders windows in scrolling mode.
- Reordering currently requires one window per scrolling column. The helper refuses stacked columns rather than moving extra windows unexpectedly. Floating windows are excluded from the scrolling tape.

## Code to consult first

| File in the plugin | Responsibility |
| --- | --- |
| [src/input-host.inc](ytuchkov.omapanel/src/input-host.inc) | Lets app mouse gestures reach this widget instead of Omarchy's overlaid whole-widget drag handler. Most sensitive to future shell changes. |
| [taskbar/AppChip.qml](ytuchkov.omapanel/taskbar/AppChip.qml) | Mouse press, horizontal drag threshold, target updates, release, click suppression, and `preventStealing`. |
| [taskbar/AppChipDrag.inc](ytuchkov.omapanel/taskbar/AppChipDrag.inc) | Dragged-icon opacity and insertion marker. |
| [taskbar/TaskbarChrome.qml](ytuchkov.omapanel/taskbar/TaskbarChrome.qml) | Chooses the scrolling or regular rows; hit-tests the drop target. |
| [src/scrolling.inc](ytuchkov.omapanel/src/scrolling.inc) | Stable scrolling row, inactive pins on the left, helper processes, refresh timers, and reorder requests. |
| [scripts/scroll-order.py](ytuchkov.omapanel/scripts/scroll-order.py) | Reads real window positions; detects floating mode; focuses and swaps real scrolling columns; restores focus. |
| [src/shell.inc](ytuchkov.omapanel/src/shell.inc) | Hyprland event refresh scheduling. |
| [src/state.inc](ytuchkov.omapanel/src/state.inc) | Original pinned and running window lists for regular mode. |
| [src/BarWidget.qml](ytuchkov.omapanel/src/BarWidget.qml) | Entry-point source and include list. |
| [scripts/bundle-qml.py](ytuchkov.omapanel/scripts/bundle-qml.py) | Generates the installed root `BarWidget.qml`. |

**Do not edit root `BarWidget.qml` directly.** Edit the split sources and regenerate it. Read the plugin's [AGENTS.md](ytuchkov.omapanel/AGENTS.md), including the 150-line source-file limit and Repeater delegate guidance.

## Failures found and fixed

### Dragging does nothing or moves the whole hotbar widget

Omarchy's installed `/usr/share/omarchy/shell/plugins/bar/Bar.qml` has a `ModuleSlot` with a `modulePointer` MouseArea above its widget. It captures left presses to rearrange whole bar widgets. An icon MouseArea nested below it never gets that press; increasing the icon's own `z` does not bypass an ancestor's sibling.

`src/input-host.inc` finds the enclosing `WidgetHost.owner.widgetHolder.parent` and raises that widget area above the overlay using a reversible `Binding` on `z`. This affects only the personal hotbar. Other bar widgets keep their stock gestures. The hotbar itself no longer uses the stock whole-widget left-drag gesture.

If an Omarchy update changes that hierarchy, inspect `WidgetHost`, `ModuleSlot`, `widgetHolder`, and `modulePointer` in the installed bar source and adapt this plugin-local integration. **Do not modify the packaged `/usr/share/omarchy/` files.**

### Icons disappear in floating mode

Omarchy implements floating mode by floating the windows while preserving the workspace's tiled layout name. Thus `activeworkspace.tiledLayout == "scrolling"` alone does not establish that the workspace is in scrolling mode.

The helper also checks the `omarchy-floating-workspace` window tag (including tags ending in `*`) and treats an all-floating nonempty workspace as non-scrolling. The regular running-row delegate reads `taskbar.runningWindows[index]` explicitly.

### Icons stop following real window order

The query helper sorts the current workspace's mapped, nonhidden tiled clients by their `at` coordinates. Its JSON must reach `setScrollState()` in `src/scrolling.inc`.

- In the **generated root** QML, the helper URL must resolve to `scripts/scroll-order.py`, not `../scripts/scroll-order.py`. Includes in the entry source retain their literal URLs when bundled. A successful direct Python invocation does not verify the QML integration.
- Frequent title updates can starve a debounce timer that is restarted on every raw event. `src/shell.inc` starts the timer only when it is not already running; the independent periodic query also runs directly.
- Keep the scrolling row stable between actual order changes. Rebuilding its Repeater model on every `hyprlandRevision` destroys the pressed icon mid-gesture. Query results only replace the row when the order/mode changes, and are deferred while dragging.

### Files changed, but the old behavior remains

In this session the shell logged “Local plugin changed, reloading” while retaining old QML behavior. `omarchy restart shell` loaded the new code. A reload log alone is not proof that the visible widget is using the new version.

## Diagnose and rebuild

```bash
cd ~/.config/omarchy/plugins/ytuchkov.omapanel

# Read-only: check helper output and the compositor's state.
python3 scripts/scroll-order.py
hyprctl -j activeworkspace
hyprctl -j clients

# Rebuild after editing split sources, then confirm the generated file matches.
PATH=/usr/lib/qt6/bin:$PATH python3 scripts/bundle-qml.py
PATH=/usr/lib/qt6/bin:$PATH python3 scripts/bundle-qml.py --check

# Load the new QML reliably.
omarchy restart shell

# Inspect helper errors and QML errors.
journalctl --user --since '5 minutes ago' -o cat --no-pager \
  | rg 'Hotbar|omapanel|ReferenceError|TypeError|Required property'
```

Quickshell also writes instance logs under `/run/user/$UID/quickshell/by-id/<instance>/log.log`. Read the active instance if the journal lacks detail. Helper stderr is logged with `Hotbar query:` or `Hotbar move:`.

The helper's mutation interface is `python3 scripts/scroll-order.py SOURCE_ADDRESS TARGET_ADDRESS before|after`. It really rearranges desktop windows; use the no-argument form for read-only diagnosis.

## Restore this snapshot

Review the snapshot against the installed plugin first, especially after an Omarchy upgrade. This restores the personal plugin code, not shell settings or the compositor configuration. Run from this directory:

```bash
live="$HOME/.config/omarchy/plugins/ytuchkov.omapanel"
backup="$HOME/.config/omarchy/plugins/ytuchkov.omapanel.backup.$(date +%Y%m%d-%H%M%S)"

sha256sum -c SHA256SUMS
cp -a "$live" "$backup"
cp -a ytuchkov.omapanel/. "$live/"
cd "$live"
PATH=/usr/lib/qt6/bin:$PATH python3 scripts/bundle-qml.py --check
omarchy restart shell
```

This copies the snapshot over the existing clone without deleting unrelated files. If reinstalling on a fresh machine, create the plugin directory and select `ytuchkov.omapanel` in the shell bar layout; the backup command above assumes an existing installation.

## Validation performed

- Dragged Chrome's visible icon past SourceGit with a virtual mouse; confirmed the actual compositor address order changed to match, then restored the original order.
- Swapped real scrolling columns and visually confirmed that the hotbar followed them.
- Temporarily floated the workspace windows; confirmed scrolling mode disabled and running icons remained visible, then restored tiled state, focus, and original order.
- Visually confirmed inactive pinned launchers stay left of running windows.
