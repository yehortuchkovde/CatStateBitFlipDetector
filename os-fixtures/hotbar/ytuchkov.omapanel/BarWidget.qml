// GENERATED FILE — DO NOT EDIT.
//
// BarWidget.qml is produced by scripts/bundle-qml.py from:
//   - src/BarWidget.qml and src/*.inc
//   - taskbar/*.qml and taskbar/*.inc
//   - settings/**/*.qml and settings/**/*.inc
//
// Any change you make here will be overwritten the next time the
// bundle script runs. Edit those sources instead, then run:
//   python3 scripts/bundle-qml.py

import QtQuick
import QtQuick.Controls as QQC
import QtQuick.Layouts
import Quickshell
import Quickshell.Hyprland
import Quickshell.Io
import Quickshell.Wayland
import qs.Commons
import qs.Ui
import "TaskHelpers.js" as Helpers
import "TaskMatch.js" as Match

BarWidget {
    id: taskbar

    readonly property color activeBackgroundColor: configuredColor(activeBackgroundValue, activeHoverBackgroundColor)
    readonly property bool activeBackgroundEnabled: activeBackgroundValue.length > 0
    readonly property string activeBackgroundValue: hexColorValue(setting("activeBackgroundColor", ""))
    readonly property int activeFontWeight: clampedInt("activeFontWeight", 600, 1, 1000)
    readonly property color activeHoverBackgroundColor: Style.hoverFillFor(activeTextColor, Color.accent)
    readonly property string activeIndicator: String(setting("activeIndicator", "Underline"))
    readonly property real activeOpacity: resolvedOpacity(setting("activeOpacity", 100))
    readonly property color activeTextColor: configuredColor(setting("activeColor", ""), bar ? bar.barForeground : Color.foreground)
    readonly property var activeWindow: Hyprland.activeToplevel
    readonly property string altClickAction: normalizedClickAction(setting("altClickAction", "Focus or Launch"), "Focus or Launch")
    readonly property int animationDuration: clampedInt("animationDuration", 180, 0, 500)
    readonly property int automaticFontSize: Math.max(1, Math.round(Style.font.body))
    readonly property color barBackgroundColor: configuredColor(barBackgroundValue, "transparent")
    readonly property bool barBackgroundEnabled: barBackgroundValue.length > 0
    readonly property string barBackgroundValue: hexColorValue(setting("barBackgroundColor", ""))
    readonly property int barBottomPadding: clampedInt("barBottomPadding", 0, 0, 16)
    readonly property real barCornerRadius: resolvedItemCornerRadius(setting("barCornerRadius", ""))
    readonly property int barHorizontalPadding: clampedInt("barHorizontalPadding", 0, 0, 24)
    readonly property real barPadBottom: Style.space(barBottomPadding)
    readonly property real barPadHorizontal: Style.space(barHorizontalPadding)
    readonly property real barPadTop: Style.space(barTopPadding)
    readonly property int barTopPadding: clampedInt("barTopPadding", 0, 0, 16)
    readonly property var contextActions: {
        var actions = contextEntry && contextEntry.actions ? contextEntry.actions : [];
        return actions.filter(function (action) {
            return action && String(action.id || "").toLowerCase() !== "new-window";
        });
    }
    property Item contextAnchor: null
    property var contextApp: null
    readonly property bool contextCanLaunch: !!(contextEntry || (contextApp && contextApp.launch))
    readonly property var contextEntry: desktopEntryFor(contextApp, contextWindow)
    readonly property bool contextIsPinned: contextPinnedIndex >= 0
    property bool contextMenuOpen: false
    readonly property int contextPinnedIndex: pinnedIndex(contextApp, contextWindow)
    property var contextWindow: null
    readonly property var contextWindows: windowsForDescriptor(contextApp, contextWindow)
    readonly property string ctrlClickAction: normalizedClickAction(setting("ctrlClickAction", "Focus or Launch"), "Focus or Launch")
    readonly property string defaultPinnedApps: '[{"label":"Zen","match":"^zen$","launch":"omarchy-launch-browser","icon":"zen-browser","desktopId":"zen"},{"label":"Cursor","match":"^cursor$","launch":"uwsm-app -- cursor","icon":"co.anysphere.cursor","desktopId":"cursor"}]'
    property string dragAddress: ""
    property string dropAddress: ""
    property bool dropAfter: false
    readonly property string excludedClasses: String(setting("excludedClasses", ""))
    readonly property string fallbackIconName: "application-x-executable"
    readonly property int fixedItemWidth: clampedInt("fixedItemWidth", 160, 24)
    readonly property int fontSize: resolvedFontSize(setting("fontSize", ""))
    readonly property bool groupRunningByWorkspace: boolSetting("groupRunningByWorkspace", true)
    property real groupWheelAccumulator: 0
    property string groupWheelCursorAddress: ""
    property double groupWheelCursorDeadline: 0
    property string groupWheelKey: ""
    readonly property color hoverBackgroundColor: configuredColor(setting("hoverBackgroundColor", ""), Style.hoverFillFor(hoverTextColor, Color.accent))
    readonly property int hoverFontWeight: clampedInt("hoverFontWeight", 500, 1, 1000)
    readonly property real hoverOpacity: resolvedOpacity(setting("hoverOpacity", 100))
    readonly property bool hoverOverridesActive: boolSetting("hoverOverridesActive", true)
    readonly property color hoverTextColor: configuredColor(setting("hoverColor", ""), normalTextColor)
    property int hyprlandRevision: 0
    readonly property int iconLabelSpacing: clampedInt("iconLabelSpacing", 8, 0)
    readonly property bool iconOnlyWhenClosed: boolSetting("iconOnlyWhenClosed", true)
    readonly property int iconSize: clampedInt("iconSize", 18, 8)
    readonly property color indicatorColor: configuredColor(setting("indicatorColor", ""), Color.accent)
    readonly property int indicatorLength: clampedInt("indicatorLength", 0, 0)
    readonly property int indicatorMargin: clampedInt("indicatorMargin", 2, 0)
    readonly property int indicatorSize: clampedInt("indicatorSize", 4, 2)
    readonly property int indicatorThickness: clampedInt("indicatorThickness", 2, 1)

    // The Omarchy ModuleSlot puts a left-button drag area above WidgetHost.
    // Raise only our holder above that sibling so app clicks and drags reach
    // AppChip. The bar itself and other widgets keep their stock gestures.
    readonly property Item inputHolder: {
        var item = parent;
        while (item) {
            if ("owner" in item && item.owner && "widgetHolder" in item.owner)
                return item.owner.widgetHolder.parent;
            item = item.parent;
        }
        return null;
    }
    readonly property bool invertIconColors: boolSetting("invertIconColors", false)
    readonly property real itemCornerRadius: resolvedItemCornerRadius(setting("itemCornerRadius", ""))
    readonly property int itemHorizontalPadding: clampedInt("itemHorizontalPadding", 8, 0)
    readonly property int itemSpacing: clampedInt("itemSpacing", 4, 0)
    readonly property int itemVerticalPadding: clampedInt("itemVerticalPadding", 12, 0)
    readonly property string labelFormat: String(setting("labelFormat", "[APP_NAME] - [WINDOW_TITLE]"))
    readonly property bool leadingSeparator: boolSetting("leadingSeparator", false)
    readonly property string leftClickAction: normalizedClickAction(setting("leftClickAction", "Focus or Launch"), "Focus or Launch")
    readonly property int maxAdaptiveWidth: clampedInt("maxAdaptiveWidth", 280, 24)
    readonly property int maxClassLength: 96
    readonly property int maxDesktopIdLength: 128
    readonly property int maxIconLength: 512
    readonly property int maxLabelLength: clampedInt("maxLabelLength", 14, 4)
    readonly property int maxLaunchLength: 4096
    readonly property int maxRegexPatternLength: 256
    readonly property int maxRunningWindows: clampedInt("maxRunningWindows", 12, 1)
    readonly property int maxUntrustedTextLength: 512
    readonly property string middleClickAction: normalizedClickAction(setting("middleClickAction", "Do Nothing"), "Do Nothing")
    readonly property color normalBackgroundColor: configuredColor(normalBackgroundValue, Style.normalFillFor(normalTextColor, Color.accent))
    readonly property bool normalBackgroundEnabled: normalBackgroundValue.length > 0
    readonly property string normalBackgroundValue: hexColorValue(setting("normalBackgroundColor", ""))
    readonly property int normalFontWeight: clampedInt("normalFontWeight", 400, 1, 1000)
    readonly property real normalOpacity: resolvedOpacity(setting("normalOpacity", 100))
    readonly property color normalTextColor: configuredColor(setting("normalColor", ""), bar ? bar.barForeground : Color.foreground)
    readonly property bool opened: contextMenuOpen || settingsPanelOpen
    readonly property int panelHeight: resolvedBarHeight(setting("barHeight", ""))
    property Item pendingPreviewAnchor: null
    property var pendingPreviewToplevel: null
    readonly property var pinnedApps: parsePinnedApps(setting("pinnedApps", defaultPinnedApps))
    readonly property var pinnedItems: {
        var revision = hyprlandRevision;
        var result = [];
        for (var i = 0; i < pinnedApps.length; i++) {
            var app = pinnedApps[i];
            var windows = windowsForDescriptor(app, null);
            if (windows.length === 0) {
                result.push({
                    "app": app,
                    "window": null
                });
                continue;
            }
            for (var j = 0; j < windows.length; j++) {
                result.push({
                    "app": app,
                    "window": windows[j]
                });
            }
        }
        return result;
    }
    property Item previewAnchor: null
    readonly property bool previewAutoHeight: boolSetting("previewAutoHeight", false)
    readonly property int previewDelay: clampedInt("previewDelay", 350, 0, 1500)
    readonly property int previewHeight: clampedInt("previewHeight", 220, 100, 480)
    property int previewHoverCount: 0
    readonly property int previewQuality: clampedInt("previewQuality", 100, 10, 100)
    property var previewToplevel: null
    readonly property int previewWidth: clampedInt("previewWidth", 320, 160, 640)
    property var resolvedIdentities: ({})
    readonly property string rightClickAction: normalizedClickAction(setting("rightClickAction", "Open Context Menu"), "Open Context Menu")
    readonly property var runningWindows: {
        var revision = hyprlandRevision;
        var values = Hyprland.toplevels && Hyprland.toplevels.values ? Hyprland.toplevels.values : [];
        var result = [];
        if (!showRunning)
            return result;

        for (var i = 0; i < values.length; i++) {
            var candidate = values[i];
            if (!candidate || !windowClass(candidate))
                continue;

            if (isPinnedWindow(candidate) || isExcludedWindow(candidate))
                continue;

            result.push(candidate);
        }
        if (groupRunningByWorkspace)
            result = result.map(function (window, index) {
                return {
                    "window": window,
                    "originalIndex": index
                };
            }).sort(function (left, right) {
                var workspaceDifference = windowWorkspaceId(left.window) - windowWorkspaceId(right.window);
                return workspaceDifference !== 0 ? workspaceDifference : left.originalIndex - right.originalIndex;
            }).map(function (entry) {
                return entry.window;
            });

        return result.slice(0, maxRunningWindows);
    }
    property var scrollState: ({
            enabled: false,
            addresses: []
        })
    property var scrollingItems: []
    readonly property bool scrollingMode: !!scrollState.enabled
    readonly property bool sectionSeparator: boolSetting("sectionSeparator", true)
    property bool settingsPanelOpen: false
    readonly property string shiftClickAction: normalizedClickAction(setting("shiftClickAction", "Focus or Launch"), "Focus or Launch")
    readonly property bool showIcons: boolSetting("showIcons", true)
    readonly property bool showLabels: boolSetting("showLabels", true)
    readonly property bool showRunning: boolSetting("showRunning", true)
    readonly property bool showWindowPreviews: boolSetting("showWindowPreviews", false)
    readonly property bool trimEdgeItemGaps: boolSetting("trimEdgeItemGaps", true)
    readonly property string widthMode: String(setting("widthMode", "Adaptive"))

    function activateOrLaunch(app, toplevel) {
        if (toplevel) {
            var address = normalizedAddress(toplevel);
            if (address) {
                Quickshell.execDetached(["hyprctl", "dispatch", "hl.dsp.focus({ window = " + JSON.stringify("address:" + address) + " })"]);
                return;
            }
        }
        if (app && app.launch)
            runLaunch(app.launch);
    }
    function appMatchesWindow(app, toplevel) {
        if (!app || !patternMatches(String(app.match || ""), windowCandidates(toplevel)))
            return false;

        // When a pin declares desktopId, refuse windows whose resolved desktop entry
        // is a different app (limits broad regex + wrong Electron/.desktop pairing).
        var expected = normalizeDesktopId(app.desktopId);
        if (!expected)
            return true;

        var entry = windowDesktopEntry(toplevel);
        if (!entry)
            return true;

        var actual = normalizeDesktopId(entry.id);
        if (!actual)
            return true;

        return actual === expected;
    }
    function asPlainUiText(value) {
        return Helpers.asPlainUiText(value);
    }
    function boolSetting(key, fallback) {
        return setting(key, fallback) === true;
    }
    function cancelPreview(toplevel) {
        previewHideTimer.stop();
        if (!toplevel || pendingPreviewToplevel === toplevel)
            clearPendingPreview();

        if (!toplevel || previewToplevel === toplevel) {
            previewToplevel = null;
            previewAnchor = null;
        }
    }
    function clampedInt(key, fallback, minValue, maxValue) {
        var parsed = Number(setting(key, fallback));
        if (isNaN(parsed))
            parsed = fallback;

        parsed = Math.round(parsed);
        if (maxValue === undefined || maxValue === null)
            return Math.max(minValue, parsed);

        return Math.max(minValue, Math.min(maxValue, parsed));
    }
    function clampedLaunch(value) {
        return Helpers.clampedLaunch(value);
    }
    function clearPendingPreview() {
        previewTimer.stop();
        pendingPreviewAnchor = null;
        pendingPreviewToplevel = null;
    }
    function clickAction(button, modifiers) {
        if (button === Qt.LeftButton) {
            if (modifiers & Qt.ControlModifier)
                return ctrlClickAction;

            if (modifiers & Qt.ShiftModifier)
                return shiftClickAction;

            if (modifiers & Qt.AltModifier)
                return altClickAction;

            return leftClickAction;
        }
        if (button === Qt.RightButton)
            return rightClickAction;

        if (button === Qt.MiddleButton)
            return middleClickAction;

        return "Do Nothing";
    }
    function close() {
        contextMenuOpen = false;
        settingsPanelOpen = false;
        cancelPreview(null);
    }
    function closeContextWindow() {
        var target = contextWindow;
        close();
        closeWindow(target);
    }
    function closeContextWindows() {
        var targets = contextWindows.slice();
        close();
        for (var i = 0; i < targets.length; i++)
            closeWindow(targets[i]);
    }
    function closeWindow(toplevel) {
        var address = normalizedAddress(toplevel);
        if (!address)
            return;

        Quickshell.execDetached(["hyprctl", "dispatch", "hl.dsp.window.close({ window = " + JSON.stringify("address:" + address) + " })"]);
    }
    function commitPreview(anchor, toplevel) {
        clearPendingPreview();
        previewHideTimer.stop();
        previewAnchor = anchor;
        previewToplevel = toplevel;
    }
    function configuredColor(value, fallback) {
        return Match.configuredColor(value, fallback);
    }
    function cycleWindowGroup(app, toplevel, pinned, delta) {
        var group = wheelGroup(app, toplevel, pinned);
        if (group.windows.length === 0) {
            resetGroupWheel();
            return false;
        }
        if (groupWheelKey !== group.key) {
            groupWheelAccumulator = 0;
            groupWheelKey = group.key;
            groupWheelCursorAddress = "";
            groupWheelCursorDeadline = 0;
        }
        var wheel = Util.wheelSteps(groupWheelAccumulator, delta);
        groupWheelAccumulator = wheel.remainder;
        if (wheel.steps === 0)
            return true;

        var now = Date.now();
        var step = wheel.steps > 0 ? -1 : 1;
        var cursorIndex = now <= groupWheelCursorDeadline ? group.windows.map(function (window) {
            return normalizedAddress(window);
        }).indexOf(groupWheelCursorAddress) : -1;
        var activeIndex = indexOfToplevel(group.windows, activeWindow);
        var hoveredIndex = indexOfToplevel(group.windows, toplevel);
        var nextIndex;
        if (cursorIndex >= 0)
            nextIndex = (cursorIndex + step + group.windows.length) % group.windows.length;
        else if (activeIndex >= 0)
            nextIndex = (activeIndex + step + group.windows.length) % group.windows.length;
        else
            // Entering an inactive group selects exactly the chip under the pointer.
            // The following wheel step advances from this remembered cursor even if
            // Hyprland has not published the focus change yet.
            nextIndex = hoveredIndex >= 0 ? hoveredIndex : 0;
        groupWheelCursorAddress = normalizedAddress(group.windows[nextIndex]);
        groupWheelCursorDeadline = now + 750;
        activateOrLaunch(app, group.windows[nextIndex]);
        return true;
    }
    function defaultSettings() {
        var registry = bar ? bar.barWidgetRegistry : null;
        var metadata = registry && typeof registry.metadataFor === "function" ? registry.metadataFor(moduleName) : null;
        var defaults = metadata && metadata.defaults ? metadata.defaults : ({});
        return Object.assign({}, defaults);
    }
    function descriptorFor(app, toplevel) {
        if (app)
            return {
                "label": asPlainUiText(String(app.label || windowLabel(toplevel) || "App")) || "App",
                "match": String(app.match || ""),
                "launch": clampedLaunch(app.launch),
                "icon": sanitizeIconName(app.icon || windowIcon(toplevel) || fallbackIconName),
                "desktopId": normalizeDesktopId(app.desktopId)
            };

        var entry = windowDesktopEntry(toplevel);
        var appClass = windowClass(toplevel);
        var desktopId = normalizeDesktopId(entry ? entry.id : "");
        return {
            "label": windowLabel(toplevel),
            "match": appClass ? "^" + regexEscape(appClass) + "$" : "",
            "launch": launchCommandForDesktopId(desktopId),
            "icon": sanitizeIconName(entry && entry.icon ? entry.icon : windowIcon(toplevel)),
            "desktopId": desktopId
        };
    }
    function desktopEntryFor(app, toplevel) {
        var desktopId = normalizeDesktopId(app && app.desktopId ? app.desktopId : "");
        if (desktopId) {
            var byId = DesktopEntries.byId(desktopId) || DesktopEntries.byId(desktopId + ".desktop");
            if (byId)
                return byId;
        }
        if (toplevel) {
            var matched = windowDesktopEntry(toplevel);
            if (matched)
                return matched;
        }
        if (!app || !app.label)
            return null;

        var label = String(app.label || "").trim();
        return isPlausibleAppId(label) ? DesktopEntries.heuristicLookup(label) : null;
    }
    function executeDesktopAction(action) {
        close();
        if (!action || typeof action.execute !== "function")
            return;

        if (!contextEntry || !contextEntry.actions)
            return;

        var allowed = false;
        for (var i = 0; i < contextEntry.actions.length; i++) {
            if (contextEntry.actions[i] === action) {
                allowed = true;
                break;
            }
        }
        if (!allowed)
            return;

        action.execute();
    }
    function fallbackIconSource() {
        return Quickshell.iconPath(fallbackIconName, true);
    }
    function formattedWindowLabel(appName, toplevel) {
        return Match.formattedWindowLabel(appName, windowTitle(toplevel), labelFormat);
    }
    function handleChipHover(chip, hovered, toplevel) {
        if (!showWindowPreviews) {
            if (chip.bar)
                hovered ? chip.bar.showTooltip(chip, chip.tooltipText) : chip.bar.hideTooltip(chip);
            return;
        }
        if (hovered) {
            previewHoverCount++;
            previewHideTimer.stop();
            if (chip.bar)
                chip.bar.hideTooltip(chip);
            if (toplevel)
                requestPreview(chip, toplevel);
            else if (!previewToplevel && !pendingPreviewToplevel && chip.bar)
                chip.bar.showTooltip(chip, chip.tooltipText);
            return;
        }
        if (chip.bar)
            chip.bar.hideTooltip(chip);
        previewHoverCount = Math.max(0, previewHoverCount - 1);
        if (previewHoverCount === 0)
            previewHideTimer.restart();
    }
    function handleConfiguredClick(app, toplevel, anchor, button, modifiers) {
        performClickAction(clickAction(button, modifiers), app, toplevel, anchor);
    }
    function hexColorValue(value) {
        var text = value === undefined || value === null ? "" : String(value).trim();
        if (/^#[0-9a-f]{6}$/i.test(text) || /^#[0-9a-f]{8}$/i.test(text))
            return text;

        return "";
    }
    function indexOfToplevel(windows, target) {
        for (var i = 0; i < windows.length; i++) {
            if (sameToplevel(windows[i], target))
                return i;
        }
        return -1;
    }
    function isExcludedWindow(toplevel) {
        if (!excludedClasses.trim())
            return false;

        var patterns = excludedClasses.split(",");
        var candidates = windowCandidates(toplevel);
        for (var i = 0; i < patterns.length; i++) {
            if (patternMatches(patterns[i].trim(), candidates))
                return true;
        }
        return false;
    }
    function isPinnedWindow(toplevel) {
        for (var i = 0; i < pinnedApps.length; i++) {
            if (appMatchesWindow(pinnedApps[i], toplevel))
                return true;
        }
        return false;
    }
    function isPlausibleAppId(value) {
        return Helpers.isPlausibleAppId(value);
    }
    function isRemoteIconSource(value) {
        return Helpers.isRemoteIconSource(value);
    }
    function isUnsafeClassPattern(pattern) {
        return Match.isUnsafeClassPattern(pattern);
    }
    function launchCommandForDesktopId(desktopId) {
        var id = normalizeDesktopId(desktopId);
        if (!id)
            return "";

        return "uwsm-app -- gtk-launch " + Util.shellQuote(id + ".desktop");
    }
    function launchContextNewWindow() {
        var app = contextApp;
        var toplevel = contextWindow;
        close();
        launchNewWindow(app, toplevel);
    }
    function launchNewWindow(app, toplevel) {
        var descriptor = descriptorFor(app, toplevel);
        var entry = desktopEntryFor(descriptor, toplevel);
        if (entry && bar && bar.shell && bar.shell.appLibrary) {
            var id = normalizeDesktopId(entry.id || descriptor.desktopId);
            if (id) {
                bar.shell.appLibrary.launch(id, asPlainUiText(String(entry.name || descriptor.label || id)));
                return;
            }
        }
        if (descriptor.launch)
            runLaunch(descriptor.launch);
    }
    function normalizeDesktopId(value) {
        return Helpers.normalizeDesktopId(value);
    }
    function normalizedAddress(toplevel) {
        return Match.normalizedAddress(toplevel);
    }
    function normalizedClickAction(value, fallback) {
        return Helpers.normalizedClickAction(value, fallback);
    }
    function openContextMenu(anchor, app, toplevel) {
        settingsPanelOpen = false;
        contextAnchor = anchor;
        contextApp = descriptorFor(app, toplevel);
        contextWindow = toplevel;
        contextMenuOpen = true;
    }
    function openSettingsPanel() {
        contextMenuOpen = false;
        Qt.callLater(function () {
            settingsPanelOpen = true;
        });
    }
    function parsePinnedApps(raw) {
        return Helpers.parsePinnedApps(raw);
    }
    function patternMatches(pattern, values) {
        return Match.patternMatches(pattern, values);
    }
    function performClickAction(action, app, toplevel, anchor) {
        if (anchor && anchor.bar)
            anchor.bar.hideTooltip(anchor);

        if (action === "Do Nothing")
            return;

        if (action === "Open Context Menu") {
            openContextMenu(anchor, app, toplevel);
            return;
        }
        if (action === "Open Settings") {
            contextAnchor = anchor;
            openSettingsPanel();
            return;
        }
        if (action === "Toggle Pin") {
            close();
            togglePinFor(app, toplevel);
            return;
        }
        close();
        if (action === "Focus or Launch") {
            activateOrLaunch(app, toplevel);
        } else if (action === "New Window") {
            launchNewWindow(app, toplevel);
        } else if (action === "Close Window") {
            closeWindow(toplevel);
        } else if (action === "Close All Windows") {
            var targets = windowsForDescriptor(app, toplevel);
            for (var i = 0; i < targets.length; i++)
                closeWindow(targets[i]);
        }
    }
    function persistPinnedApps(apps) {
        var nextSettings = Object.assign({}, settings || {});
        nextSettings.pinnedApps = JSON.stringify(apps.map(function (app) {
            return descriptorFor(app, null);
        }));
        persistSettings(nextSettings);
    }
    function persistSetting(key, value) {
        var nextSettings = Object.assign({}, settings || {});
        nextSettings[key] = value;
        persistSettings(nextSettings);
    }
    function persistSettings(nextSettings) {
        if (!bar || !bar.shell || typeof bar.shell.updateEntryInline !== "function")
            return;

        settings = nextSettings;
        bar.shell.updateEntryInline(moduleName, nextSettings);
    }
    function pinnedIndex(app, toplevel) {
        var descriptor = descriptorFor(app, toplevel);
        for (var i = 0; i < pinnedApps.length; i++) {
            if (descriptor.match === pinnedApps[i].match)
                return i;

            if (toplevel && appMatchesWindow(pinnedApps[i], toplevel))
                return i;
        }
        return -1;
    }
    function previewToplevelAlive(toplevel) {
        if (!toplevel)
            return false;

        if (runningWindows.indexOf(toplevel) >= 0)
            return true;

        for (var i = 0; i < pinnedItems.length; i++) {
            if (pinnedItems[i].window === toplevel)
                return true;
        }
        return false;
    }
    function regexEscape(value) {
        return Match.regexEscape(value);
    }
    function reorderDrop() {
        if (dragAddress && dropAddress && dragAddress !== dropAddress && !scrollMove.running) {
            scrollMove.command = ["python3", Qt.resolvedUrl("scripts/scroll-order.py").toString().replace("file://", ""), dragAddress, dropAddress, dropAfter ? "after" : "before"];
            scrollMove.running = true;
        }
        dragAddress = "";
        dropAddress = "";
    }
    function requestPreview(anchor, toplevel) {
        if (!showWindowPreviews || !toplevel) {
            cancelPreview(null);
            return;
        }
        pendingPreviewAnchor = anchor;
        pendingPreviewToplevel = toplevel;
        if (previewDelay <= 0 || previewToplevel !== null || previewHideTimer.running)
            commitPreview(anchor, toplevel);
        else
            previewTimer.restart();
    }
    function resetGroupWheel() {
        groupWheelAccumulator = 0;
        groupWheelKey = "";
        groupWheelCursorAddress = "";
        groupWheelCursorDeadline = 0;
    }
    function resetSettings() {
        persistSettings(defaultSettings());
    }
    function resolveIconSource(icon) {
        var value = sanitizeIconName(icon);
        var resolved = "";
        if (bar && bar.shell && bar.shell.appLibrary)
            resolved = String(bar.shell.appLibrary.iconSource(value) || "");
        if (!resolved) {
            if (value.indexOf("file://") === 0 || value.indexOf("image://") === 0)
                resolved = value;
            else if (value.charAt(0) === "/")
                resolved = Util.fileUrl(value);
            else
                resolved = Quickshell.iconPath(value || fallbackIconName, true);
        }
        if (!resolved || isRemoteIconSource(resolved))
            return fallbackIconSource();

        return resolved;
    }
    function resolvedBarHeight(rawValue) {
        var available = Math.max(1, Math.round(barSize));
        var text = rawValue === undefined || rawValue === null ? "" : String(rawValue).trim();
        if (text === "")
            return available;

        var parsed = Number(text);
        if (isNaN(parsed))
            return available;

        return Math.max(16, Math.min(64, Math.min(available, Math.round(parsed))));
    }
    function resolvedFontSize(rawValue) {
        return Helpers.resolvedFontSize(rawValue, automaticFontSize);
    }
    function resolvedIdentity(toplevel) {
        var ipc = toplevel ? toplevel.lastIpcObject : null;
        return ipc ? resolvedIdentities[String(ipc.address)] : null;
    }
    function resolvedItemCornerRadius(rawValue) {
        return Helpers.resolvedItemCornerRadius(rawValue, Math.max(2, Style.cornerRadius));
    }
    function resolvedOpacity(rawValue) {
        return Helpers.resolvedOpacity(rawValue);
    }
    function runLaunch(command) {
        var value = clampedLaunch(command);
        if (!value || !bar)
            return;

        bar.run(value);
    }
    function sameToplevel(left, right) {
        if (!left || !right)
            return false;

        if (left === right)
            return true;

        var leftAddress = normalizedAddress(left);
        var rightAddress = normalizedAddress(right);
        return leftAddress !== "" && leftAddress === rightAddress;
    }
    function sanitizeClassValue(value) {
        return Helpers.sanitizeClassValue(value);
    }
    function sanitizeIconName(icon) {
        return Helpers.sanitizeIconName(icon);
    }
    function setScrollState(next) {
        scrollState = next;
        var values = Hyprland.toplevels.values;
        var items = next.addresses.map(function (address) {
            for (var i = 0; i < values.length; i++) {
                if (normalizedAddress(values[i]) === address)
                    return {
                        app: null,
                        window: values[i]
                    };
            }
            return null;
        }).filter(function (item) {
            return item && !isExcludedWindow(item.window);
        });
        scrollingItems = pinnedItems.filter(function (item) {
            return !item.window;
        }).concat(items);
    }
    function shortenedLabel(label) {
        return Match.shortenedLabel(label, maxLabelLength);
    }
    function startsWorkspaceGroup(index, toplevel) {
        if (!groupRunningByWorkspace || index <= 0)
            return false;

        return windowWorkspaceId(toplevel) !== windowWorkspaceId(runningWindows[index - 1]);
    }
    function toggleContextPin() {
        var app = contextApp;
        var toplevel = contextWindow;
        close();
        togglePinFor(app, toplevel);
    }
    function togglePinFor(app, toplevel) {
        var next = pinnedApps.slice();
        var descriptor = descriptorFor(app, toplevel);
        var index = pinnedIndex(descriptor, toplevel);
        if (index >= 0)
            next.splice(index, 1);
        else if (descriptor.match)
            next.push(descriptor);
        persistPinnedApps(next);
    }
    function updateDrop(x, y) {
        chrome.updateDrop(x, y);
    }
    function wheelGroup(app, toplevel, pinned) {
        if (!toplevel)
            return {
                "key": "",
                "windows": []
            };

        if (pinned) {
            var descriptor = descriptorFor(app, toplevel);
            return {
                "key": "pinned:" + descriptor.match + ":" + descriptor.desktopId,
                "windows": windowsForDescriptor(app, toplevel)
            };
        }
        if (!groupRunningByWorkspace)
            return {
                "key": "",
                "windows": []
            };

        var workspaceId = windowWorkspaceId(toplevel);
        return {
            "key": "workspace:" + workspaceId,
            "windows": runningWindows.filter(function (candidate) {
                return windowWorkspaceId(candidate) === workspaceId;
            })
        };
    }
    function windowCandidates(toplevel) {
        return Match.windowCandidates(toplevel);
    }
    function windowClass(toplevel) {
        var candidates = windowCandidates(toplevel);
        return candidates.length > 0 ? candidates[0] : "";
    }
    function windowDesktopEntry(toplevel) {
        var candidates = windowCandidates(toplevel);
        for (var i = 0; i < candidates.length; i++) {
            if (!isPlausibleAppId(candidates[i]))
                continue;

            var entry = DesktopEntries.heuristicLookup(candidates[i]);
            if (entry)
                return entry;
        }
        var resolved = resolvedIdentity(toplevel);
        if (resolved && resolved.id) {
            var known = DesktopEntries.byId(resolved.id);
            if (known)
                return known;
        }
        return null;
    }
    function windowIcon(toplevel) {
        var entry = windowDesktopEntry(toplevel);
        var resolved = resolvedIdentity(toplevel);
        return sanitizeIconName(entry && entry.icon ? entry.icon : (resolved && resolved.icon ? resolved.icon : fallbackIconName));
    }
    function windowLabel(toplevel) {
        var entry = windowDesktopEntry(toplevel);
        if (entry && entry.name)
            return asPlainUiText(String(entry.name));

        var ipc = toplevel ? (toplevel.lastIpcObject || null) : null;
        var tags = ipc && Array.isArray(ipc.tags) ? ipc.tags : [];
        for (var i = 0; i < tags.length; i++) {
            if (String(tags[i]).indexOf("terminal") === 0)
                return "Terminal";
        }
        var appClass = windowClass(toplevel);
        if (appClass) {
            var pieces = appClass.split(".");
            var value = pieces[pieces.length - 1].replace(/[-_]+/g, " ");
            return asPlainUiText(value.charAt(0).toUpperCase() + value.slice(1));
        }
        return windowTitle(toplevel) || "Window";
    }
    function windowPixelSize(toplevel) {
        var width = 0;
        var height = 0;
        var ipc = toplevel ? (toplevel.lastIpcObject || null) : null;
        var size = ipc ? ipc.size : null;
        if (size) {
            if (size.width !== undefined) {
                width = Number(size.width);
                height = Number(size.height);
            } else if (size.length >= 2) {
                width = Number(size[0]);
                height = Number(size[1]);
            }
        }
        if (!(width > 0 && height > 0) && toplevel && toplevel.wayland) {
            width = Number(toplevel.wayland.width || 0);
            height = Number(toplevel.wayland.height || 0);
        }
        return {
            "width": isNaN(width) ? 0 : width,
            "height": isNaN(height) ? 0 : height
        };
    }
    function windowTitle(toplevel) {
        if (!toplevel)
            return "";

        var directTitle = toplevel.title ? String(toplevel.title).trim() : "";
        if (directTitle)
            return asPlainUiText(directTitle);

        var ipc = toplevel.lastIpcObject || null;
        return ipc && ipc.title ? asPlainUiText(String(ipc.title).trim()) : "";
    }
    function windowWorkspaceId(toplevel) {
        var ipc = toplevel ? (toplevel.lastIpcObject || null) : null;
        var workspace = ipc ? (ipc.workspace || null) : null;
        var id = workspace ? Number(workspace.id) : 0;
        return isNaN(id) ? 0 : id;
    }
    function windowsForDescriptor(app, toplevel) {
        var revision = hyprlandRevision;
        var descriptor = descriptorFor(app, toplevel);
        var values = Hyprland.toplevels && Hyprland.toplevels.values ? Hyprland.toplevels.values : [];
        var result = [];
        for (var i = 0; i < values.length; i++) {
            if (appMatchesWindow(descriptor, values[i]))
                result.push(values[i]);
        }
        return result;
    }

    implicitHeight: barSize
    implicitWidth: visible ? chrome.implicitWidth : 0
    moduleName: "ytuchkov.omapanel"
    visible: !vertical && (pinnedApps.length > 0 || runningWindows.length > 0)

    Behavior on implicitWidth {
        NumberAnimation {
            duration: taskbar.animationDuration
            easing.type: Easing.OutCubic
        }
    }

    Binding {
        property: "z"
        restoreMode: Binding.RestoreBindingOrValue
        target: taskbar.inputHolder
        value: 1
        when: taskbar.inputHolder !== null
    }
    Timer {
        id: scrollRefresh

        interval: 100

        onTriggered: {
            if (!scrollQuery.running && !scrollMove.running)
                scrollQuery.running = true;
        }
    }
    Timer {
        interval: 1500
        repeat: true
        running: true
        triggeredOnStart: true

        onTriggered: {
            if (!scrollQuery.running && !scrollMove.running)
                scrollQuery.running = true;
        }
    }
    Process {
        id: scrollQuery

        command: ["python3", Qt.resolvedUrl("scripts/scroll-order.py").toString().replace("file://", "")]

        stderr: StdioCollector {
            onStreamFinished: {
                if (text.trim())
                    console.warn("Hotbar query:", text);
            }
        }
        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    var next = JSON.parse(text);
                    if (!taskbar.dragAddress && JSON.stringify(next) !== JSON.stringify(taskbar.scrollState))
                        taskbar.setScrollState(next);
                } catch (error) {
                    console.warn("Hotbar order:", error);
                }
            }
        }
    }
    Process {
        id: scrollMove

        stderr: StdioCollector {
            onStreamFinished: {
                if (text.trim())
                    console.warn("Hotbar move:", text);
            }
        }

        onExited: scrollRefresh.restart()
    }
    Process {
        id: identityResolver

        command: ["python3", Qt.resolvedUrl("scripts/resolve-icons.py").toString().replace(/^file:\/\//, "")]
        running: true

        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    var updated = JSON.parse(text);
                    if (JSON.stringify(updated) !== JSON.stringify(taskbar.resolvedIdentities)) {
                        taskbar.resolvedIdentities = updated;
                        if (taskbar.bar && taskbar.bar.shell && taskbar.bar.shell.appLibrary)
                            taskbar.bar.shell.appLibrary.refreshIcons();
                    }
                } catch (error) {
                    console.warn("OmaPanel identity lookup failed");
                }
            }
        }
    }

    // Debounce compositor events; retry while open to catch new launchers/icons.
    Timer {
        id: identityRefresh

        interval: 500

        onTriggered: {
            if (!identityResolver.running)
                identityResolver.running = true;
        }
    }
    Connections {
        function onRawEvent(event) {
            identityRefresh.restart();
        }

        target: Hyprland
    }
    Timer {
        interval: 15000
        repeat: true
        running: taskbar.visible

        onTriggered: {
            if (!identityResolver.running)
                identityResolver.running = true;
        }
    }
    Connections {
        function onRawEvent(event) {
            taskbar.hyprlandRevision++;
            if (event.name !== "activewindow" && event.name !== "activewindowv2")
                if (!scrollRefresh.running)
                    scrollRefresh.start();
            if (taskbar.previewToplevel && !taskbar.previewToplevelAlive(taskbar.previewToplevel))
                taskbar.cancelPreview(taskbar.previewToplevel);
        }

        target: Hyprland
    }
    TaskbarChrome {
        id: chrome
    }
    Timer {
        id: previewTimer

        interval: taskbar.previewDelay

        onTriggered: taskbar.commitPreview(taskbar.pendingPreviewAnchor, taskbar.pendingPreviewToplevel)
    }
    Timer {
        id: previewHideTimer

        interval: 160

        onTriggered: taskbar.cancelPreview(null)
    }
    ContextMenu {
    }
    WindowPreview {
    }
    TaskbarSettings {
        id: taskbarSettings

        anchorItem: taskbar.contextAnchor || taskbar
        bar: taskbar.bar
        open: taskbar.settingsPanelOpen
        owner: taskbar
        values: taskbar.settings || ({})

        onResetRequested: taskbar.resetSettings()
        onSettingChanged: function (key, value) {
            taskbar.persistSetting(key, value);
        }
    }

    component AppChip: WidgetButton {
        id: chip

        required property var app
        required property var appWindow
        readonly property real calculatedWidth: {
            if (!ready)
                return Math.max(24, compactWidth);

            if (isClosedPinned && taskbar.iconOnlyWhenClosed)
                return compactWidth;

            if (fixedWidthMode)
                return Math.max(nonLabelExtent, Style.space(taskbar.fixedItemWidth));

            return Math.max(nonLabelExtent, Math.min(naturalWidth, Style.space(taskbar.maxAdaptiveWidth)));
        }
        readonly property real compactWidth: horizontalPaddingExtent + iconContentExtent
        readonly property real contentHeight: Math.max(effectiveShowIcons ? iconExtent : 0, labelHeight)
        readonly property real contentSpacing: effectiveShowIcons && effectiveShowLabels ? Style.space(ready ? taskbar.iconLabelSpacing : 8) : 0
        property string displayLabel: ""
        readonly property bool effectiveShowIcons: {
            if (!taskbar)
                return true;

            return taskbar.showIcons || (taskbar.iconOnlyWhenClosed && isClosedPinned);
        }
        readonly property bool effectiveShowLabels: {
            if (!taskbar)
                return true;

            if (isClosedPinned && taskbar.iconOnlyWhenClosed)
                return false;

            return taskbar.showLabels || !effectiveShowIcons;
        }
        readonly property bool fixedWidthMode: !!taskbar && String(taskbar.widthMode).toLowerCase() === "fixed"
        readonly property color foregroundColor: {
            if (!ready)
                return Color.foreground;

            if (useHoverStyle)
                return taskbar.hoverTextColor;

            return isActive ? taskbar.activeTextColor : taskbar.normalTextColor;
        }
        readonly property real foregroundOpacity: {
            if (!ready)
                return 1;

            var value = useHoverStyle ? taskbar.hoverOpacity : (isActive ? taskbar.activeOpacity : taskbar.normalOpacity);
            return isNaN(value) ? 1 : Math.max(0, Math.min(1, value));
        }
        readonly property int foregroundWeight: {
            var weight = 400;
            if (ready)
                weight = useHoverStyle ? taskbar.hoverFontWeight : (isActive ? taskbar.activeFontWeight : taskbar.normalFontWeight);

            return Math.max(1, Math.min(1000, Number(weight) || 400));
        }
        readonly property real hitHorizontalPadding: Style.space(ready ? taskbar.itemSpacing : 4) / 2
        readonly property real hitHorizontalPaddingExtent: hitPadLeft + hitPadRight
        readonly property real hitPadLeft: includeLeadingHitPadding ? hitHorizontalPadding : 0
        readonly property real hitPadRight: includeTrailingHitPadding ? hitHorizontalPadding : 0
        readonly property real horizontalPaddingExtent: Style.space((ready ? taskbar.itemHorizontalPadding : 8) * 2)
        readonly property real iconContentExtent: effectiveShowIcons ? iconExtent : 0
        readonly property int iconExtent: Style.space(taskbar ? taskbar.iconSize : 18)
        property string iconName: ""
        property bool includeLeadingHitPadding: true
        property bool includeTrailingHitPadding: true
        readonly property bool isActive: {
            if (!taskbar || !appWindow)
                return false;

            return taskbar.activeWindow === appWindow;
        }
        readonly property bool isClosedPinned: pinned && appWindow === null
        readonly property real labelExtent: effectiveShowLabels ? Math.max(0, calculatedWidth - nonLabelExtent) : 0
        readonly property real labelHeight: effectiveShowLabels ? labelMetrics.height : 0
        readonly property real naturalWidth: nonLabelExtent + (effectiveShowLabels ? labelMetrics.advanceWidth : 0)
        readonly property real nonLabelExtent: horizontalPaddingExtent + iconContentExtent + contentSpacing
        required property bool pinned
        property bool pointerHovered: false
        readonly property bool ready: !!taskbar
        readonly property string resolvedIconName: {
            if (iconName)
                return iconName;

            if (app && app.icon)
                return String(app.icon);

            if (taskbar && appWindow)
                return taskbar.windowIcon(appWindow);

            return "";
        }
        readonly property string resolvedLabel: {
            var name = displayLabel;
            if (!name && app && app.label)
                name = String(app.label);

            if (taskbar && appWindow)
                return taskbar.formattedWindowLabel(name, appWindow);

            return name || "App";
        }
        readonly property string shortLabel: taskbar ? taskbar.shortenedLabel(resolvedLabel) : resolvedLabel
        readonly property bool useHoverStyle: ready && pointerHovered && (!isActive || taskbar.hoverOverridesActive)

        function handleBarWheel(delta) {
            return ready ? taskbar.cycleWindowGroup(app, appWindow, pinned, delta) : false;
        }
        function setPointerHovered(hovered) {
            pointerHovered = hovered;
            if (ready)
                taskbar.handleChipHover(chip, hovered, appWindow);
        }

        bar: ready ? taskbar.bar : null
        dimmed: false
        fixedHeight: {
            var padTop = ready ? taskbar.barPadTop : 0;
            var padBottom = ready ? taskbar.barPadBottom : 0;
            var barHeight = ready ? taskbar.panelHeight : 24;
            var verticalPad = Style.space((ready ? taskbar.itemVerticalPadding : 12) * 2);
            return Math.min(Math.max(1, barHeight - padTop - padBottom), contentHeight + verticalPad);
        }
        fixedWidth: Math.max(1, calculatedWidth + hitHorizontalPaddingExtent)
        hasVisualContent: true
        interactive: false
        keepSpace: true
        labelVisible: false
        opacity: taskbar.dragAddress && appWindow && taskbar.dragAddress === taskbar.normalizedAddress(appWindow) ? 0.45 : 1
        text: ""
        tooltipText: (ready ? taskbar.asPlainUiText(resolvedLabel) : resolvedLabel) + (pinned && appWindow === null ? "\nClick to open" : "\nClick to focus")
        useActiveColor: false

        Component.onDestruction: {
            if (chip.pointerHovered && taskbar)
                taskbar.handleChipHover(chip, false, chip.appWindow);
        }

        TextMetrics {
            id: labelMetrics

            font.family: ready && taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
            font.pixelSize: ready ? taskbar.fontSize : Style.font.body
            font.weight: chip.foregroundWeight
            text: chip.shortLabel
        }
        Rectangle {
            readonly property bool persistentActive: chip.ready && chip.isActive && taskbar.activeBackgroundEnabled
            readonly property bool showFill: chip.ready && (chip.useHoverStyle || persistentActive || taskbar.normalBackgroundEnabled)

            anchors.bottomMargin: Style.space(1)
            anchors.fill: parent
            anchors.leftMargin: chip.hitPadLeft + Style.space(1)
            anchors.rightMargin: chip.hitPadRight + Style.space(1)
            anchors.topMargin: Style.space(1)
            color: showFill ? (chip.useHoverStyle ? taskbar.hoverBackgroundColor : (persistentActive ? taskbar.activeBackgroundColor : taskbar.normalBackgroundColor)) : "transparent"
            opacity: showFill ? 1 : 0
            radius: chip.ready ? taskbar.itemCornerRadius : 4
        }
        Row {
            anchors.centerIn: parent
            opacity: chip.foregroundOpacity
            spacing: chip.contentSpacing
            z: 1

            Behavior on opacity {
                NumberAnimation {
                    duration: chip.ready ? taskbar.animationDuration : 0
                    easing.type: Easing.OutCubic
                }
            }

            Item {
                height: chip.iconExtent
                visible: chip.effectiveShowIcons
                width: chip.iconExtent

                Image {
                    id: appIcon

                    anchors.fill: parent
                    asynchronous: true
                    fillMode: Image.PreserveAspectFit
                    layer.enabled: chip.ready && taskbar.invertIconColors
                    layer.smooth: true
                    mipmap: true
                    smooth: true
                    source: chip.ready ? taskbar.resolveIconSource(chip.resolvedIconName) : ""
                    sourceSize.height: Math.round(height * Screen.devicePixelRatio)
                    sourceSize.width: Math.round(width * Screen.devicePixelRatio)

                    layer.effect: ShaderEffect {
                        property variant source

                        fragmentShader: Qt.resolvedUrl("shaders/invert.frag.qsb")
                    }
                }
                Text {
                    anchors.centerIn: parent
                    color: chip.foregroundColor
                    font.family: chip.ready && taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                    font.pixelSize: chip.ready ? taskbar.fontSize : Style.font.body
                    font.weight: chip.foregroundWeight
                    text: chip.shortLabel.charAt(0).toUpperCase()
                    textFormat: Text.PlainText
                    visible: appIcon.status === Image.Error || appIcon.source.toString() === ""
                }
            }
            Text {
                color: chip.foregroundColor
                elide: Text.ElideRight
                font.family: chip.ready && taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                font.pixelSize: chip.ready ? taskbar.fontSize : Style.font.body
                font.weight: chip.foregroundWeight
                maximumLineCount: 1
                text: chip.shortLabel
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter
                visible: chip.effectiveShowLabels
                width: chip.labelExtent
            }
        }
        Rectangle {
            readonly property bool dotIndicator: chip.ready && taskbar.activeIndicator === "Dot"
            readonly property real edgeMargin: Style.space(chip.ready ? taskbar.indicatorMargin : 2)
            readonly property bool topIndicator: chip.ready && taskbar.activeIndicator === "Top"

            color: chip.ready ? taskbar.indicatorColor : Color.accent
            height: dotIndicator ? width : Style.space(chip.ready ? taskbar.indicatorThickness : 2)
            radius: height / 2
            visible: chip.ready && chip.isActive && taskbar.activeIndicator !== "None"
            width: {
                if (!chip.ready)
                    return 0;

                if (dotIndicator)
                    return Style.space(taskbar.indicatorSize);

                if (taskbar.indicatorLength > 0)
                    return Math.min(chip.calculatedWidth, Style.space(taskbar.indicatorLength));

                return Math.max(Style.space(12), chip.calculatedWidth - Style.space(taskbar.itemHorizontalPadding * 2));
            }
            x: Math.round((parent.width - width) / 2)
            y: topIndicator ? edgeMargin : Math.max(0, parent.height - height - edgeMargin)
            z: 2

            Behavior on width {
                NumberAnimation {
                    duration: chip.ready ? taskbar.animationDuration : 0
                    easing.type: Easing.OutCubic
                }
            }
        }
        Rectangle {
            color: Color.foreground
            height: parent.height
            visible: !!chip.appWindow && !!taskbar.dragAddress && taskbar.dropAddress === taskbar.normalizedAddress(chip.appWindow) && taskbar.dragAddress !== taskbar.dropAddress
            width: 2
            x: taskbar.dropAfter ? parent.width - width : 0
        }
        MouseArea {
            id: pointer

            property bool moved: false
            property real pressX: 0

            acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
            preventStealing: true
            z: 10

            onCanceled: {
                taskbar.dragAddress = "";
                taskbar.dropAddress = "";
            }
            onClicked: function (mouse) {
                if (moved)
                    return;
                taskbar.handleConfiguredClick(chip.app, chip.appWindow, chip, mouse.button, mouse.modifiers);
            }
            onEntered: chip.setPointerHovered(true)
            onExited: chip.setPointerHovered(false)
            onPositionChanged: function (mouse) {
                if (!(pressedButtons & Qt.LeftButton) || !taskbar.scrollingMode || !chip.appWindow)
                    return;
                if (!moved && Math.abs(mouse.x - pressX) > 8) {
                    moved = true;
                    taskbar.cancelPreview(null);
                    taskbar.dragAddress = taskbar.normalizedAddress(chip.appWindow);
                }
                if (moved) {
                    var point = mapToItem(taskbar, mouse.x, mouse.y);
                    taskbar.updateDrop(point.x, point.y);
                }
            }
            onPressed: function (mouse) {
                pressX = mouse.x;
                moved = false;
            }
            onReleased: {
                if (moved)
                    taskbar.reorderDrop();
            }
            onWheel: function (wheel) {
                var delta = wheel.angleDelta.y !== 0 ? wheel.angleDelta.y : wheel.angleDelta.x;
                wheel.accepted = chip.handleBarWheel(delta);
            }
        }
    }
    component ApplicationsPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "RUNNING WINDOWS"
            width: parent.width
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingDescription: "Append non-pinned Hyprland windows."
            settingKey: "showRunning"
            settingLabel: "Show running windows"
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingDescription: "Sort dynamic windows and separate workspace groups."
            settingKey: "groupRunningByWorkspace"
            settingLabel: "Group by workspace"
        }
        SettingNumber {
            fallbackValue: 12
            host: panel
            maximumValue: 30
            minimumValue: 1
            settingKey: "maxRunningWindows"
            settingLabel: "Max windows"
        }
        SettingText {
            host: panel
            placeholder: "Comma-separated regular expressions"
            settingKey: "excludedClasses"
            settingLabel: "Excluded classes"
        }
        Rectangle {
            color: Style.hoverFillFor(panel.contentForeground, Color.accent)
            implicitHeight: pinHint.implicitHeight + Style.space(20)
            radius: Math.max(2, Style.cornerRadius)
            width: parent.width

            Text {
                id: pinHint

                anchors.left: parent.left
                anchors.leftMargin: Style.space(10)
                anchors.right: parent.right
                anchors.rightMargin: Style.space(10)
                anchors.verticalCenter: parent.verticalCenter
                color: panel.contentForeground
                font.family: panel.contentFontFamily
                font.pixelSize: Style.font.caption
                text: "Pinned applications are managed from each app's right-click menu."
                wrapMode: Text.WordWrap
            }
        }
        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "PINNED APPS"
            width: parent.width
        }
        Text {
            color: Util.alpha(panel.contentForeground, 0.58)
            font.family: panel.contentFontFamily
            font.pixelSize: Style.font.caption
            text: "No pinned applications. Pin apps from the right-click menu."
            visible: panel.pinnedAppsModel.length === 0
            width: parent.width
            wrapMode: Text.WordWrap
        }
        Repeater {
            model: panel.pinnedAppsModel

            Row {
                id: pinnedRow

                required property int index
                required property var modelData

                spacing: Style.space(6)
                width: parent.width

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    color: panel.contentForeground
                    elide: Text.ElideRight
                    font.family: panel.contentFontFamily
                    font.pixelSize: Style.font.body
                    text: String(pinnedRow.modelData && pinnedRow.modelData.label ? pinnedRow.modelData.label : "App")
                    textFormat: Text.PlainText
                    width: parent.width - Style.space(84)
                }
                PinnedMoveButton {
                    enabled: pinnedRow.index > 0
                    host: panel
                    iconText: "\uf077"
                    tooltipText: "Move up"

                    onClicked: panel.movePinnedApp(pinnedRow.index, -1)
                }
                PinnedMoveButton {
                    enabled: pinnedRow.index < panel.pinnedAppsModel.length - 1
                    host: panel
                    iconText: "\uf078"
                    tooltipText: "Move down"

                    onClicked: panel.movePinnedApp(pinnedRow.index, 1)
                }
            }
        }
    }
    component BarPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "BAR"
            width: parent.width
        }
        SettingOptionalNumber {
            host: panel
            maximumValue: 64
            minimumValue: 16
            placeholder: "Bar"
            settingKey: "barHeight"
            settingLabel: "Height"
            width: parent.width
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 0
                host: panel
                maximumValue: 16
                minimumValue: 0
                settingKey: "barTopPadding"
                settingLabel: "Top padding"
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 0
                host: panel
                maximumValue: 16
                minimumValue: 0
                settingKey: "barBottomPadding"
                settingLabel: "Bottom padding"
                width: (parent.width - parent.spacing) / 2
            }
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 0
                host: panel
                maximumValue: 24
                minimumValue: 0
                settingKey: "barHorizontalPadding"
                settingLabel: "Edge padding"
                width: (parent.width - parent.spacing) / 2
            }
            SettingOptionalNumber {
                host: panel
                maximumValue: 32
                minimumValue: 0
                placeholder: "Theme"
                settingKey: "barCornerRadius"
                settingLabel: "Bar rounding"
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingText {
            host: panel
            placeholder: "Off or #RRGGBBAA"
            settingKey: "barBackgroundColor"
            settingLabel: "Bar background"
        }
        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "SEPARATORS"
            width: parent.width
        }
        SettingToggle {
            fallbackValue: false
            host: panel
            settingKey: "leadingSeparator"
            settingLabel: "Leading separator"
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingKey: "sectionSeparator"
            settingLabel: "Pinned / running separator"
        }
    }
    component ChipLayoutPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "WIDTH"
            width: parent.width
        }
        SettingDropdown {
            fallbackValue: "Adaptive"
            host: panel
            settingKey: "widthMode"
            settingLabel: "Item width mode"
            settingOptions: ["Adaptive", "Fixed"]
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 160
                host: panel
                maximumValue: 480
                minimumValue: 32
                settingKey: "fixedItemWidth"
                settingLabel: "Fixed width"
                stepValue: 4
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 280
                host: panel
                maximumValue: 640
                minimumValue: 32
                settingKey: "maxAdaptiveWidth"
                settingLabel: "Adaptive max"
                stepValue: 4
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingNumber {
            fallbackValue: 14
            host: panel
            maximumValue: 40
            minimumValue: 4
            settingKey: "maxLabelLength"
            settingLabel: "Max label chars"
        }
        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "PADDING & GAPS"
            width: parent.width
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 8
                host: panel
                maximumValue: 24
                minimumValue: 0
                settingKey: "itemHorizontalPadding"
                settingLabel: "Horizontal padding"
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 12
                host: panel
                maximumValue: 16
                minimumValue: 0
                settingKey: "itemVerticalPadding"
                settingLabel: "Vertical padding"
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingNumber {
            fallbackValue: 4
            host: panel
            maximumValue: 24
            minimumValue: 0
            settingKey: "itemSpacing"
            settingLabel: "Item spacing"
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingDescription: "Keep item spacing between chips only, not at the bar edges."
            settingKey: "trimEdgeItemGaps"
            settingLabel: "Trim start/end item gaps"
        }
        SettingOptionalNumber {
            host: panel
            maximumValue: 32
            minimumValue: 0
            placeholder: "Theme"
            settingKey: "itemCornerRadius"
            settingLabel: "Item rounding"
            width: parent.width
        }
    }
    component ClicksPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "CLICK ACTIONS"
            width: parent.width
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingDropdown {
                fallbackValue: "Focus or Launch"
                host: panel
                settingKey: "leftClickAction"
                settingLabel: "Left click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
            SettingDropdown {
                fallbackValue: "Open Context Menu"
                host: panel
                settingKey: "rightClickAction"
                settingLabel: "Right click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingDropdown {
                fallbackValue: "Do Nothing"
                host: panel
                settingKey: "middleClickAction"
                settingLabel: "Middle click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
            SettingDropdown {
                fallbackValue: "Focus or Launch"
                host: panel
                settingKey: "ctrlClickAction"
                settingLabel: "Ctrl + left click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingDropdown {
                fallbackValue: "Focus or Launch"
                host: panel
                settingKey: "shiftClickAction"
                settingLabel: "Shift + left click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
            SettingDropdown {
                fallbackValue: "Focus or Launch"
                host: panel
                settingKey: "altClickAction"
                settingLabel: "Alt + left click"
                settingOptions: panel.actionOptions
                width: (parent.width - parent.spacing) / 2
            }
        }
        Text {
            color: Util.alpha(panel.contentForeground, 0.58)
            font.family: panel.contentFontFamily
            font.pixelSize: Style.font.caption
            text: "For combined modifiers, Ctrl takes priority over Shift, then Alt."
            width: parent.width
            wrapMode: Text.WordWrap
        }
    }
    component ColorsPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "ACTIVE ITEM"
            width: parent.width
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingDescription: "Use hover colors when the pointer is over the focused window."
            settingKey: "hoverOverridesActive"
            settingLabel: "Hover overrides active"
        }
        Row {
            readonly property real columnWidth: (width - spacing * 2) / 3

            spacing: Style.space(10)
            width: parent.width

            Column {
                spacing: Style.space(8)
                width: parent.columnWidth

                Text {
                    color: panel.contentForeground
                    font.bold: true
                    font.family: panel.contentFontFamily
                    font.pixelSize: Style.font.caption
                    text: "NORMAL"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Theme or #RRGGBB"
                    settingKey: "normalColor"
                    settingLabel: "Foreground"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Off or #RRGGBBAA"
                    settingKey: "normalBackgroundColor"
                    settingLabel: "Background"
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 400
                    host: panel
                    maximumValue: 1000
                    minimumValue: 1
                    settingKey: "normalFontWeight"
                    settingLabel: "Weight"
                    stepValue: 50
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 100
                    host: panel
                    maximumValue: 100
                    minimumValue: 0
                    settingKey: "normalOpacity"
                    settingLabel: "Opacity (%)"
                    stepValue: 5
                    width: parent.width
                }
            }
            Column {
                spacing: Style.space(8)
                width: parent.columnWidth

                Text {
                    color: panel.contentForeground
                    font.bold: true
                    font.family: panel.contentFontFamily
                    font.pixelSize: Style.font.caption
                    text: "HOVER"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Normal or #RRGGBB"
                    settingKey: "hoverColor"
                    settingLabel: "Foreground"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Theme or #RRGGBBAA"
                    settingKey: "hoverBackgroundColor"
                    settingLabel: "Background"
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 500
                    host: panel
                    maximumValue: 1000
                    minimumValue: 1
                    settingKey: "hoverFontWeight"
                    settingLabel: "Weight"
                    stepValue: 50
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 100
                    host: panel
                    maximumValue: 100
                    minimumValue: 0
                    settingKey: "hoverOpacity"
                    settingLabel: "Opacity (%)"
                    stepValue: 5
                    width: parent.width
                }
            }
            Column {
                spacing: Style.space(8)
                width: parent.columnWidth

                Text {
                    color: panel.contentForeground
                    font.bold: true
                    font.family: panel.contentFontFamily
                    font.pixelSize: Style.font.caption
                    text: "ACTIVE"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Theme or #RRGGBB"
                    settingKey: "activeColor"
                    settingLabel: "Foreground"
                    width: parent.width
                }
                SettingText {
                    host: panel
                    placeholder: "Active or #RRGGBBAA"
                    settingKey: "activeBackgroundColor"
                    settingLabel: "Background"
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 600
                    host: panel
                    maximumValue: 1000
                    minimumValue: 1
                    settingKey: "activeFontWeight"
                    settingLabel: "Weight"
                    stepValue: 50
                    width: parent.width
                }
                SettingNumber {
                    fallbackValue: 100
                    host: panel
                    maximumValue: 100
                    minimumValue: 0
                    settingKey: "activeOpacity"
                    settingLabel: "Opacity (%)"
                    stepValue: 5
                    width: parent.width
                }
            }
        }
    }
    component ContentPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "VISIBILITY"
            width: parent.width
        }
        SettingToggle {
            fallbackValue: true
            host: panel
            settingDescription: "Expand pinned apps when a matching window opens."
            settingKey: "iconOnlyWhenClosed"
            settingLabel: "Icon only when closed"
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingToggle {
                fallbackValue: true
                host: panel
                settingKey: "showIcons"
                settingLabel: "Icons"
                width: (parent.width - parent.spacing) / 2
            }
            SettingToggle {
                fallbackValue: true
                host: panel
                settingKey: "showLabels"
                settingLabel: "Labels"
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingToggle {
            fallbackValue: false
            host: panel
            settingDescription: "Invert application icon pixels while preserving transparency."
            settingKey: "invertIconColors"
            settingLabel: "Invert icon colors"
        }
        SettingText {
            fallbackValue: "[APP_NAME] - [WINDOW_TITLE]"
            host: panel
            placeholder: "[APP_NAME] - [WINDOW_TITLE]"
            settingKey: "labelFormat"
            settingLabel: "Label format"
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 18
                host: panel
                maximumValue: 32
                minimumValue: 8
                settingKey: "iconSize"
                settingLabel: "Icon size"
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 8
                host: panel
                maximumValue: 20
                minimumValue: 0
                settingKey: "iconLabelSpacing"
                settingLabel: "Icon / label gap"
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingOptionalNumber {
            host: panel
            maximumValue: 24
            minimumValue: 8
            placeholder: "Auto"
            settingKey: "fontSize"
            settingLabel: "Font size"
        }
    }
    component ContextMenu: PopupCard {
        id: contextPopup

        anchorItem: {
            if (!taskbar)
                return null;

            return taskbar.contextAnchor || taskbar;
        }
        bar: taskbar ? taskbar.bar : null
        contentHeight: contextPopup.fittedContentHeight(contextMenuColumn.implicitHeight, Style.space(480))
        contentWidth: contextPopup.fittedContentWidth(Style.space(300))
        open: !!(taskbar && taskbar.contextMenuOpen)
        owner: taskbar
        padding: Style.space(8)

        Flickable {
            anchors.fill: parent
            boundsBehavior: Flickable.StopAtBounds
            clip: true
            contentHeight: contextMenuColumn.implicitHeight
            contentWidth: width
            flickableDirection: Flickable.VerticalFlick
            interactive: contentHeight > height

            QQC.ScrollBar.vertical: QQC.ScrollBar {
                policy: QQC.ScrollBar.AsNeeded
            }

            Column {
                id: contextMenuColumn

                spacing: 0
                width: parent.width

                Item {
                    implicitHeight: Style.space(48)
                    width: parent.width

                    Image {
                        id: contextIcon

                        anchors.left: parent.left
                        anchors.leftMargin: Style.space(8)
                        anchors.verticalCenter: parent.verticalCenter
                        fillMode: Image.PreserveAspectFit
                        height: width
                        source: taskbar.resolveIconSource(taskbar.contextApp ? taskbar.contextApp.icon : taskbar.fallbackIconName)
                        sourceSize.height: Math.round(height * Screen.devicePixelRatio)
                        sourceSize.width: Math.round(width * Screen.devicePixelRatio)
                        width: Style.space(24)
                    }
                    Button {
                        id: contextSettingsButton

                        accent: Color.accent
                        anchors.right: parent.right
                        anchors.rightMargin: Style.space(4)
                        anchors.verticalCenter: parent.verticalCenter
                        fontFamily: taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                        foreground: taskbar.bar ? taskbar.bar.barForeground : Color.foreground
                        horizontalPadding: Style.space(9)
                        iconText: "\uf013"
                        tooltipText: "OmaPanel settings"
                        verticalPadding: Style.space(6)

                        onClicked: taskbar.openSettingsPanel()
                    }
                    Column {
                        anchors.left: contextIcon.right
                        anchors.leftMargin: Style.space(10)
                        anchors.right: contextSettingsButton.left
                        anchors.rightMargin: Style.space(8)
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: Style.space(2)

                        Text {
                            color: taskbar.bar ? taskbar.bar.barForeground : Color.foreground
                            elide: Text.ElideRight
                            font.bold: true
                            font.family: taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                            font.pixelSize: Style.font.body
                            text: taskbar.contextApp ? taskbar.contextApp.label : "Application"
                            textFormat: Text.PlainText
                            width: parent.width
                        }
                        Text {
                            color: Util.alpha(taskbar.bar ? taskbar.bar.barForeground : Color.foreground, 0.55)
                            font.family: taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                            font.pixelSize: Style.font.caption
                            text: taskbar.contextWindows.length === 0 ? "Not running" : (taskbar.contextWindows.length === 1 ? "1 window" : taskbar.contextWindows.length + " windows")
                            textFormat: Text.PlainText
                            width: parent.width
                        }
                    }
                }
                MenuSeparator {
                    visible: !!(taskbar && taskbar.contextWindows && taskbar.contextWindows.length > 0)
                }
                Repeater {
                    model: taskbar && taskbar.contextWindows ? taskbar.contextWindows : []

                    MenuRow {
                        required property var modelData

                        iconText: taskbar.activeWindow === modelData ? "\uf111" : ""
                        text: taskbar.windowTitle(modelData) || taskbar.windowLabel(modelData)

                        onTriggered: {
                            taskbar.close();
                            taskbar.activateOrLaunch(null, modelData);
                        }
                    }
                }
                MenuSeparator {
                    visible: !!(taskbar && taskbar.contextWindows && taskbar.contextWindows.length > 0)
                }
                MenuRow {
                    iconText: "\uf2d2"
                    text: "New Window"
                    visible: {
                        if (!taskbar)
                            return false;

                        return !!taskbar.contextCanLaunch;
                    }

                    onTriggered: taskbar.launchContextNewWindow()
                }
                Repeater {
                    model: taskbar && taskbar.contextActions ? taskbar.contextActions : []

                    MenuRow {
                        required property var modelData

                        iconText: "\uf144"
                        text: taskbar.asPlainUiText(String(modelData.name || modelData.id || "Application Action"))

                        onTriggered: taskbar.executeDesktopAction(modelData)
                    }
                }
                MenuRow {
                    enabled: {
                        if (!taskbar)
                            return false;

                        return !!(taskbar.contextIsPinned || taskbar.contextCanLaunch);
                    }
                    iconText: {
                        if (!taskbar)
                            return "\uf08d";

                        return taskbar.contextIsPinned ? "\uf127" : "\uf08d";
                    }
                    text: {
                        if (!taskbar)
                            return "Pin to Taskbar";

                        return taskbar.contextIsPinned ? "Unpin from Taskbar" : "Pin to Taskbar";
                    }

                    onTriggered: taskbar.toggleContextPin()
                }
                MenuSeparator {
                    visible: !!(taskbar && taskbar.contextWindows && taskbar.contextWindows.length > 0)
                }
                MenuRow {
                    destructive: true
                    iconText: "\uf2d4"
                    text: {
                        var count = taskbar && taskbar.contextWindows ? taskbar.contextWindows.length : 0;
                        return "Close " + count + " Windows";
                    }
                    visible: {
                        if (!taskbar || !taskbar.contextWindows)
                            return false;

                        return taskbar.contextWindows.length > 1;
                    }

                    onTriggered: taskbar.closeContextWindows()
                }
                MenuRow {
                    destructive: true
                    iconText: "\uf00d"
                    text: "Close Window"
                    visible: {
                        if (!taskbar || !taskbar.contextWindows)
                            return false;

                        return taskbar.contextWindow !== null && taskbar.contextWindows.length > 0;
                    }

                    onTriggered: taskbar.closeContextWindow()
                }
            }
        }
    }
    component IndicatorPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "INDICATOR"
            width: parent.width
        }
        SettingDropdown {
            fallbackValue: "Underline"
            host: panel
            settingKey: "activeIndicator"
            settingLabel: "Indicator style"
            settingOptions: ["Underline", "Top", "Dot", "None"]
        }
        SettingText {
            host: panel
            placeholder: "Theme accent or #RRGGBB"
            settingKey: "indicatorColor"
            settingLabel: "Indicator color"
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 2
                host: panel
                maximumValue: 8
                minimumValue: 1
                settingKey: "indicatorThickness"
                settingLabel: "Line thickness"
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 4
                host: panel
                maximumValue: 16
                minimumValue: 2
                settingKey: "indicatorSize"
                settingLabel: "Dot size"
                width: (parent.width - parent.spacing) / 2
            }
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 0
                host: panel
                maximumValue: 80
                minimumValue: 0
                settingKey: "indicatorLength"
                settingLabel: "Line length (0 = auto)"
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 2
                host: panel
                maximumValue: 12
                minimumValue: 0
                settingKey: "indicatorMargin"
                settingLabel: "Edge margin"
                width: (parent.width - parent.spacing) / 2
            }
        }
    }
    component MenuRow: Item {
        id: menuRow

        property bool destructive: false
        property string iconText: ""
        property string text: ""

        signal triggered

        implicitHeight: Style.space(32)
        opacity: enabled ? 1 : 0.4
        width: parent ? parent.width : Style.space(280)

        Rectangle {
            anchors.fill: parent
            color: menuMouse.containsMouse && menuRow.enabled ? Style.hoverFillFor(menuRow.destructive ? Color.urgent : (taskbar && taskbar.bar ? taskbar.bar.barForeground : Color.foreground), Color.accent) : "transparent"
            radius: Math.max(2, Style.cornerRadius)
        }
        Text {
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            color: {
                if (menuRow.destructive)
                    return Color.urgent;

                if (taskbar && taskbar.bar)
                    return taskbar.bar.barForeground;

                return Color.foreground;
            }
            font.family: {
                if (taskbar && taskbar.bar)
                    return taskbar.bar.fontFamily;

                return Style.font.family;
            }
            font.pixelSize: Style.font.bodySmall
            horizontalAlignment: Text.AlignHCenter
            text: menuRow.iconText
            width: Style.space(30)
        }
        Text {
            anchors.left: parent.left
            anchors.leftMargin: Style.space(34)
            anchors.right: parent.right
            anchors.rightMargin: Style.space(10)
            anchors.verticalCenter: parent.verticalCenter
            color: {
                if (menuRow.destructive)
                    return Color.urgent;

                if (taskbar && taskbar.bar)
                    return taskbar.bar.barForeground;

                return Color.foreground;
            }
            elide: Text.ElideRight
            font.family: {
                if (taskbar && taskbar.bar)
                    return taskbar.bar.fontFamily;

                return Style.font.family;
            }
            font.pixelSize: Style.font.bodySmall
            text: menuRow.text
            textFormat: Text.PlainText
        }
        MouseArea {
            id: menuMouse

            anchors.fill: parent
            cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
            enabled: menuRow.enabled
            hoverEnabled: true

            onClicked: menuRow.triggered()
        }
    }
    component MenuSeparator: Item {
        implicitHeight: visible ? Style.space(11) : 0
        width: parent ? parent.width : Style.space(280)

        Rectangle {
            anchors.left: parent.left
            anchors.leftMargin: Style.space(8)
            anchors.right: parent.right
            anchors.rightMargin: Style.space(8)
            anchors.verticalCenter: parent.verticalCenter
            color: Color.popups.border
            height: 1
            opacity: 0.5
        }
    }
    component PinnedMoveButton: Button {
        required property var host

        accent: Color.accent
        anchors.verticalCenter: parent.verticalCenter
        fontFamily: host.contentFontFamily
        foreground: host.contentForeground
        horizontalPadding: Style.space(8)
        verticalPadding: Style.space(5)
    }
    component PreviewsPage: Column {
        required property var panel

        spacing: Style.space(12)
        width: parent.width

        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "WINDOW PREVIEWS"
            width: parent.width
        }
        SettingToggle {
            fallbackValue: false
            host: panel
            settingDescription: "Show a live thumbnail when hovering an open window."
            settingKey: "showWindowPreviews"
            settingLabel: "Show window previews"
        }
        SettingNumber {
            fallbackValue: 350
            host: panel
            maximumValue: 1500
            minimumValue: 0
            settingKey: "previewDelay"
            settingLabel: "Preview delay (ms)"
            stepValue: 50
        }
        Row {
            spacing: Style.space(10)
            width: parent.width

            SettingNumber {
                fallbackValue: 320
                host: panel
                maximumValue: 640
                minimumValue: 160
                settingKey: "previewWidth"
                settingLabel: "Preview width"
                stepValue: 10
                width: (parent.width - parent.spacing) / 2
            }
            SettingNumber {
                fallbackValue: 220
                host: panel
                maximumValue: 480
                minimumValue: 100
                settingKey: "previewHeight"
                settingLabel: "Preview height"
                stepValue: 10
                width: (parent.width - parent.spacing) / 2
            }
        }
        SettingToggle {
            fallbackValue: false
            host: panel
            settingDescription: "Match the thumbnail height to the window aspect ratio."
            settingKey: "previewAutoHeight"
            settingLabel: "Auto height"
        }
        SettingNumber {
            fallbackValue: 100
            host: panel
            maximumValue: 100
            minimumValue: 10
            settingKey: "previewQuality"
            settingLabel: "Preview quality (%)"
            stepValue: 5
        }
        PanelSeparator {
            width: parent.width
        }
        PanelSectionHeader {
            fontFamily: panel.contentFontFamily
            foreground: panel.contentForeground
            text: "ANIMATION"
            width: parent.width
        }
        SettingNumber {
            fallbackValue: 180
            host: panel
            maximumValue: 500
            minimumValue: 0
            settingKey: "animationDuration"
            settingLabel: "Animation duration (ms)"
            stepValue: 10
        }
    }
    component SettingDropdown: Dropdown {
        property string fallbackValue: ""
        required property var host
        required property string settingKey
        required property string settingLabel
        required property var settingOptions

        accent: Color.accent
        background: Color.popups.background
        fontFamily: host.contentFontFamily
        foreground: host.contentForeground
        label: settingLabel
        options: settingOptions
        popupBorder: Color.popups.border
        value: host.stringValue(settingKey, fallbackValue)
        width: parent ? parent.width : 0

        onChanged: function (nextValue) {
            host.change(settingKey, nextValue);
        }
    }
    component SettingNumber: NumberField {
        required property int fallbackValue
        required property var host
        required property int maximumValue
        required property int minimumValue
        required property string settingKey
        required property string settingLabel
        property int stepValue: 1

        accent: Color.accent
        fieldWidth: width
        fontFamily: host.contentFontFamily
        foreground: host.contentForeground
        from: minimumValue
        label: settingLabel
        stepSize: stepValue
        to: maximumValue
        value: Math.round(host.numberValue(settingKey, fallbackValue))

        onModified: function (nextValue) {
            host.change(settingKey, nextValue);
        }
    }
    component SettingOptionalNumber: Column {
        required property var host
        required property int maximumValue
        required property int minimumValue
        property string placeholder: "Auto"
        required property string settingKey
        required property string settingLabel

        spacing: Style.spacing.md
        width: parent ? parent.width : 0

        Text {
            color: Util.alpha(host.contentForeground, 0.72)
            font.family: host.contentFontFamily
            font.pixelSize: Style.font.bodySmall
            text: parent.settingLabel
            width: parent.width
        }
        TextField {
            accent: Color.accent
            font.family: host.contentFontFamily
            foreground: host.contentForeground
            horizontalAlignment: TextInput.AlignHCenter
            inputMethodHints: Qt.ImhDigitsOnly
            maximumLength: String(parent.maximumValue).length
            placeholderText: parent.placeholder
            text: {
                var current = host.value(parent.settingKey, "");
                return current === undefined || current === null ? "" : String(current).trim();
            }
            width: parent.width

            onEditingFinished: {
                var nextValue = text.trim();
                if (nextValue === "") {
                    host.change(parent.settingKey, "");
                    return;
                }
                var parsed = Number(nextValue);
                if (isNaN(parsed)) {
                    text = "";
                    host.change(parent.settingKey, "");
                    return;
                }
                var clamped = Math.max(parent.minimumValue, Math.min(parent.maximumValue, Math.round(parsed)));
                text = String(clamped);
                host.change(parent.settingKey, String(clamped));
            }
            onTextEdited: {
                if (text.trim() === "")
                    host.change(parent.settingKey, "");
            }
        }
    }
    component SettingText: Column {
        property string fallbackValue: ""
        required property var host
        property string placeholder: ""
        required property string settingKey
        required property string settingLabel

        spacing: Style.space(5)
        width: parent ? parent.width : 0

        Text {
            color: host.contentForeground
            font.bold: true
            font.family: host.contentFontFamily
            font.pixelSize: Style.font.caption
            text: parent.settingLabel
            width: parent.width
        }
        TextField {
            accent: Color.accent
            font.family: host.contentFontFamily
            foreground: host.contentForeground
            placeholderText: parent.placeholder
            text: host.stringValue(parent.settingKey, parent.fallbackValue)
            width: parent.width

            onEditingFinished: host.change(parent.settingKey, text.trim())
        }
    }
    component SettingToggle: Toggle {
        property bool fallbackValue: false
        required property var host
        property string settingDescription: ""
        required property string settingKey
        required property string settingLabel

        accent: Color.accent
        checked: host.boolValue(settingKey, fallbackValue)
        description: settingDescription
        fontFamily: host.contentFontFamily
        foreground: host.contentForeground
        label: settingLabel
        width: parent ? parent.width : 0

        onClicked: host.change(settingKey, !checked)
    }
    component SettingsHub: Column {
        id: settingsHub

        required property var panel

        spacing: Style.space(4)
        width: parent.width

        Repeater {
            model: settingsHub.panel.pages.length

            Item {
                id: categoryRow

                required property int index
                readonly property var page: settingsHub.panel.pages[index]
                readonly property string pageDescription: page && page.description ? String(page.description) : ""
                readonly property string pageId: page && page.id ? String(page.id) : ""
                readonly property string pageLabel: page && page.label ? String(page.label) : ""

                implicitHeight: Style.space(52)
                width: parent.width

                Rectangle {
                    anchors.fill: parent
                    color: rowMouse.containsMouse ? Style.hoverFillFor(settingsHub.panel.contentForeground, Color.accent) : "transparent"
                    radius: Math.max(2, Style.cornerRadius)
                }
                Column {
                    anchors.left: parent.left
                    anchors.leftMargin: Style.space(10)
                    anchors.right: chevron.left
                    anchors.rightMargin: Style.space(8)
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: Style.space(2)

                    Text {
                        color: settingsHub.panel.contentForeground
                        elide: Text.ElideRight
                        font.family: settingsHub.panel.contentFontFamily
                        font.pixelSize: Style.font.body
                        text: categoryRow.pageLabel
                        width: parent.width
                    }
                    Text {
                        color: Util.alpha(settingsHub.panel.contentForeground, 0.58)
                        elide: Text.ElideRight
                        font.family: settingsHub.panel.contentFontFamily
                        font.pixelSize: Style.font.caption
                        text: categoryRow.pageDescription
                        width: parent.width
                    }
                }
                Text {
                    id: chevron

                    anchors.right: parent.right
                    anchors.rightMargin: Style.space(10)
                    anchors.verticalCenter: parent.verticalCenter
                    color: Util.alpha(settingsHub.panel.contentForeground, 0.45)
                    font.family: settingsHub.panel.contentFontFamily
                    font.pixelSize: Style.font.caption
                    text: "\uf054"
                }
                MouseArea {
                    id: rowMouse

                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true

                    onClicked: settingsHub.panel.openPage(categoryRow.pageId)
                }
            }
        }
    }
    component TaskbarChrome: Item {
        id: chrome

        readonly property int pinnedCount: taskbar && taskbar.pinnedItems ? taskbar.pinnedItems.length : 0
        readonly property int runningCount: taskbar && taskbar.runningWindows ? taskbar.runningWindows.length : 0
        readonly property bool trimEdges: !!(taskbar && taskbar.trimEdgeItemGaps)

        function updateDrop(x, y) {
            taskbar.dropAddress = "";
            for (var i = 0; i < windowRepeater.count; i++) {
                var item = windowRepeater.itemAt(i);
                if (!item || !item.entry || !item.entry.window)
                    continue;
                var point = item.mapFromItem(taskbar, x, y);
                if (point.x >= 0 && point.x < item.width && point.y >= 0 && point.y < item.height) {
                    taskbar.dropAddress = taskbar.normalizedAddress(item.entry.window);
                    taskbar.dropAfter = point.x > item.width / 2;
                    return;
                }
            }
        }

        anchors.centerIn: parent
        height: implicitHeight
        implicitHeight: taskbar ? taskbar.panelHeight : content.implicitHeight
        implicitWidth: content.implicitWidth + (taskbar ? taskbar.barPadHorizontal : 0) * 2
        width: implicitWidth

        Rectangle {
            anchors.fill: parent
            color: taskbar ? taskbar.barBackgroundColor : "transparent"
            radius: taskbar ? taskbar.barCornerRadius : 0
            visible: taskbar && taskbar.barBackgroundEnabled
        }
        Row {
            id: content

            spacing: 0
            x: taskbar ? taskbar.barPadHorizontal : 0
            y: taskbar ? taskbar.barPadTop : 0

            TaskbarSeparator {
                visible: !!(taskbar && taskbar.leadingSeparator && taskbar.pinnedApps && taskbar.pinnedApps.length > 0)
            }
            Repeater {
                id: windowRepeater

                model: taskbar ? (taskbar.scrollingMode ? taskbar.scrollingItems : taskbar.pinnedItems) : []

                Item {
                    readonly property var entry: taskbar.scrollingMode ? taskbar.scrollingItems[index] : taskbar.pinnedItems[index]
                    required property int index

                    height: pinnedChip.height
                    width: pinnedChip.width

                    AppChip {
                        id: pinnedChip

                        app: parent.entry ? parent.entry.app : null
                        appWindow: parent.entry ? parent.entry.window : null
                        includeLeadingHitPadding: !chrome.trimEdges || parent.index > 0
                        includeTrailingHitPadding: true
                        pinned: !!app
                    }
                }
            }
            TaskbarSeparator {
                visible: !!(taskbar && !taskbar.scrollingMode && taskbar.sectionSeparator && taskbar.pinnedApps && taskbar.pinnedApps.length > 0 && taskbar.runningWindows && taskbar.runningWindows.length > 0)
            }
            Repeater {
                model: taskbar && !taskbar.scrollingMode ? taskbar.runningWindows : []

                Row {
                    required property int index
                    readonly property var modelData: taskbar.runningWindows[index]

                    spacing: 0

                    TaskbarSeparator {
                        visible: !!(taskbar && taskbar.startsWorkspaceGroup(parent.index, parent.modelData))
                    }
                    AppChip {
                        app: null
                        appWindow: parent.modelData
                        includeLeadingHitPadding: !chrome.trimEdges || parent.index > 0 || chrome.pinnedCount > 0
                        includeTrailingHitPadding: !chrome.trimEdges || parent.index < chrome.runningCount - 1
                        pinned: false
                    }
                }
            }
        }
    }
    component TaskbarSeparator: Item {
        height: taskbar ? taskbar.panelHeight : 24
        width: Style.space(9)

        Rectangle {
            anchors.centerIn: parent
            color: taskbar && taskbar.bar ? taskbar.bar.barForeground : Color.foreground
            height: Math.min(parent.height * 0.42, Style.space(16))
            opacity: 0.3
            radius: width / 2
            width: Math.max(1, Style.spaceReal(1))
        }
    }
    component TaskbarSettings: KeyboardPanel {
        id: settingsPopup

        readonly property var actionOptions: ["Focus or Launch", "Open Context Menu", "New Window", "Close Window", "Close All Windows", "Toggle Pin", "Open Settings", "Do Nothing"]
        readonly property string contentFontFamily: bar ? bar.fontFamily : Style.font.family
        readonly property color contentForeground: Color.popups.text
        property string currentPage: ""
        readonly property string currentPageDescription: pageIndex === 0 ? "Changes are saved instantly" : pages[pageIndex - 1].description
        readonly property string currentPageLabel: pageIndex === 0 ? "OmaPanel Settings" : pages[pageIndex - 1].label
        readonly property int pageIndex: {
            if (currentPage === "")
                return 0;
            for (var i = 0; i < pages.length; i++) {
                if (pages[i].id === currentPage)
                    return i + 1;
            }
            return 0;
        }
        readonly property var pages: [
            {
                "id": "applications",
                "label": "Applications",
                "description": "Pins, running windows, and filters"
            },
            {
                "id": "clicks",
                "label": "Clicks",
                "description": "Mouse and modifier actions"
            },
            {
                "id": "content",
                "label": "Icons & labels",
                "description": "Visibility, format, and type size"
            },
            {
                "id": "layout",
                "label": "Chip layout",
                "description": "Width, padding, gaps, and rounding"
            },
            {
                "id": "bar",
                "label": "Bar",
                "description": "Height, padding, fill, and separators"
            },
            {
                "id": "colors",
                "label": "Colors",
                "description": "Normal, hover, and active styles"
            },
            {
                "id": "indicator",
                "label": "Indicator",
                "description": "Active-window mark"
            },
            {
                "id": "previews",
                "label": "Previews",
                "description": "Hover thumbnails and motion"
            }
        ]
        readonly property var pinnedAppsModel: {
            var raw = stringValue("pinnedApps", "[]");
            try {
                var parsed = JSON.parse(raw);
                return Array.isArray(parsed) ? parsed : [];
            } catch (exception) {
                return [];
            }
        }
        property var values: ({})

        signal resetRequested
        signal settingChanged(string key, var value)

        function boolValue(key, fallback) {
            return value(key, fallback) === true;
        }
        function change(key, nextValue) {
            settingChanged(key, nextValue);
        }
        function goHome() {
            currentPage = "";
            settingsFlick.contentY = 0;
        }
        function movePinnedApp(index, delta) {
            var apps = pinnedAppsModel.slice();
            var next = index + delta;
            if (next < 0 || next >= apps.length)
                return;

            var item = apps[index];
            apps[index] = apps[next];
            apps[next] = item;
            change("pinnedApps", JSON.stringify(apps));
        }
        function numberValue(key, fallback) {
            var current = Number(value(key, fallback));
            return isNaN(current) ? fallback : current;
        }
        function openPage(pageId) {
            currentPage = pageId;
            settingsFlick.contentY = 0;
        }
        function stringValue(key, fallback) {
            return String(value(key, fallback));
        }
        function value(key, fallback) {
            var current = values ? values[key] : undefined;
            return current === undefined || current === null ? fallback : current;
        }

        contentHeight: fittedContentHeight(settingsColumn.implicitHeight, Style.space(680))
        contentWidth: fittedContentWidth(Style.space(460))
        focusTarget: settingsFlick
        padding: Style.space(12)

        Flickable {
            id: settingsFlick

            activeFocusOnTab: true
            anchors.fill: parent
            boundsBehavior: Flickable.StopAtBounds
            clip: true
            contentHeight: settingsColumn.implicitHeight
            contentWidth: width
            flickableDirection: Flickable.VerticalFlick
            interactive: contentHeight > height

            QQC.ScrollBar.vertical: QQC.ScrollBar {
                id: verticalBar

                policy: QQC.ScrollBar.AsNeeded
            }

            Keys.onEscapePressed: function (event) {
                if (settingsPopup.currentPage !== "") {
                    settingsPopup.goHome();
                    event.accepted = true;
                    return;
                }
                settingsPopup.close();
                event.accepted = true;
            }

            Column {
                id: settingsColumn

                spacing: Style.space(12)
                width: Math.max(1, settingsFlick.width - (verticalBar.visible ? Style.space(10) : 0))

                Item {
                    implicitHeight: Math.max(settingsTitleColumn.implicitHeight, closeButton.implicitHeight)
                    width: parent.width

                    Button {
                        id: backButton

                        accent: Color.accent
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        fontFamily: settingsPopup.contentFontFamily
                        foreground: settingsPopup.contentForeground
                        horizontalPadding: Style.space(9)
                        iconText: "\uf053"
                        tooltipText: "Back to categories"
                        verticalPadding: Style.space(6)
                        visible: settingsPopup.currentPage !== ""
                        width: visible ? implicitWidth : 0

                        onClicked: settingsPopup.goHome()
                    }
                    Column {
                        id: settingsTitleColumn

                        anchors.left: backButton.visible ? backButton.right : parent.left
                        anchors.leftMargin: backButton.visible ? Style.space(8) : 0
                        anchors.right: resetButton.left
                        anchors.rightMargin: Style.space(12)
                        spacing: Style.space(2)

                        Text {
                            color: settingsPopup.contentForeground
                            elide: Text.ElideRight
                            font.bold: true
                            font.family: settingsPopup.contentFontFamily
                            font.pixelSize: Style.font.title
                            text: settingsPopup.currentPageLabel
                            width: parent.width
                        }
                        Text {
                            color: Util.alpha(settingsPopup.contentForeground, 0.58)
                            elide: Text.ElideRight
                            font.family: settingsPopup.contentFontFamily
                            font.pixelSize: Style.font.caption
                            text: settingsPopup.currentPageDescription
                            width: parent.width
                        }
                    }
                    Button {
                        id: resetButton

                        accent: Color.accent
                        anchors.right: closeButton.left
                        anchors.rightMargin: Style.space(6)
                        anchors.verticalCenter: parent.verticalCenter
                        fontFamily: settingsPopup.contentFontFamily
                        foreground: settingsPopup.contentForeground
                        horizontalPadding: Style.space(9)
                        iconText: "\uf0e2"
                        text: "Reset defaults"
                        tooltipText: "Restore manifest defaults"
                        verticalPadding: Style.space(6)

                        onClicked: settingsPopup.resetRequested()
                    }
                    Button {
                        id: closeButton

                        accent: Color.accent
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        fontFamily: settingsPopup.contentFontFamily
                        foreground: settingsPopup.contentForeground
                        horizontalPadding: Style.space(9)
                        iconText: "\uf00d"
                        tooltipText: "Close settings"
                        verticalPadding: Style.space(6)

                        onClicked: settingsPopup.close()
                    }
                }
                StackLayout {
                    currentIndex: settingsPopup.pageIndex
                    height: children[currentIndex] ? children[currentIndex].implicitHeight : 0
                    width: parent.width

                    SettingsHub {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    ApplicationsPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    ClicksPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    ContentPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    ChipLayoutPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    BarPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    ColorsPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    IndicatorPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                    PreviewsPage {
                        Layout.fillWidth: true
                        panel: settingsPopup
                    }
                }
                Item {
                    height: Style.space(2)
                    width: 1
                }
            }
        }
    }
    component WindowPreview: PopupCard {
        id: previewCard

        readonly property real qualityScale: {
            var quality = taskbar ? taskbar.previewQuality : 100;
            return Math.max(0.1, Math.min(1, quality / 100));
        }
        readonly property int thumbnailHeight: {
            var fallback = Style.space(taskbar ? taskbar.previewHeight : 220);
            if (!taskbar || !taskbar.previewAutoHeight)
                return fallback;

            var size = taskbar.windowPixelSize(taskbar.previewToplevel);
            if (!size || !(size.width > 0 && size.height > 0))
                return fallback;

            var scaled = Math.round(Style.space(taskbar.previewWidth) * size.height / size.width);
            return Math.max(Style.space(100), Math.min(Style.space(480), scaled));
        }

        anchorItem: {
            if (!taskbar)
                return null;

            return taskbar.previewAnchor || taskbar;
        }
        bar: taskbar ? taskbar.bar : null
        contentHeight: previewCard.fittedContentHeight(previewCard.thumbnailHeight + Style.space(28), Style.space(480))
        contentWidth: previewCard.fittedContentWidth(Style.space(taskbar ? taskbar.previewWidth : 320))
        open: !!(taskbar && taskbar.showWindowPreviews && taskbar.previewToplevel !== null && taskbar.previewAnchor !== null)
        owner: taskbar
        padding: Style.space(8)
        triggerMode: "hover"

        onAnchorItemChanged: {
            if (!previewCard.open)
                return;

            Qt.callLater(function () {
                if (previewCard.open)
                    previewCard.anchor.updateAnchor();
            });
        }

        Item {
            anchors.fill: parent

            Item {
                id: previewFrame

                anchors.bottom: previewTitle.top
                anchors.bottomMargin: Style.space(7)
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                clip: true

                Text {
                    anchors.centerIn: parent
                    color: taskbar.bar ? taskbar.bar.barForeground : Color.foreground
                    font.family: taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                    font.pixelSize: Style.font.title
                    opacity: 0.5
                    text: taskbar.previewToplevel ? String(taskbar.windowLabel(taskbar.previewToplevel) || "?").charAt(0).toUpperCase() : ""
                    textFormat: Text.PlainText
                    visible: !previewView.hasContent
                }
                ScreencopyView {
                    id: previewView

                    readonly property int captureHeight: Math.max(Math.round(sourceSize.height * fitScale), Math.round(sourceSize.height * previewCard.qualityScale))
                    readonly property int captureWidth: Math.max(Math.round(sourceSize.width * fitScale), Math.round(sourceSize.width * previewCard.qualityScale))
                    readonly property real drawScale: captureWidth > 0 ? Math.min(previewFrame.width / captureWidth, previewFrame.height / captureHeight) : 1
                    readonly property real fitScale: {
                        if (sourceSize.width <= 0 || sourceSize.height <= 0)
                            return 1;

                        return Math.min(previewFrame.width / sourceSize.width, previewFrame.height / sourceSize.height);
                    }

                    captureSource: taskbar.previewToplevel ? taskbar.previewToplevel.wayland : null
                    height: previewView.captureHeight
                    layer.enabled: visible
                    layer.mipmap: true
                    layer.smooth: true
                    live: previewCard.open
                    paintCursor: false
                    transformOrigin: Item.TopLeft
                    visible: hasContent && sourceSize.width > 0 && sourceSize.height > 0
                    width: previewView.captureWidth
                    x: (previewFrame.width - captureWidth * drawScale) / 2
                    y: (previewFrame.height - captureHeight * drawScale) / 2

                    transform: Scale {
                        xScale: previewView.drawScale
                        yScale: previewView.drawScale
                    }
                }
            }
            Text {
                id: previewTitle

                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                color: taskbar.bar ? taskbar.bar.barForeground : Color.foreground
                elide: Text.ElideRight
                font.family: taskbar.bar ? taskbar.bar.fontFamily : Style.font.family
                font.pixelSize: Style.font.caption
                horizontalAlignment: Text.AlignHCenter
                text: taskbar.previewToplevel ? taskbar.asPlainUiText(taskbar.windowTitle(taskbar.previewToplevel) || taskbar.windowLabel(taskbar.previewToplevel)) : ""
                textFormat: Text.PlainText
            }
        }
    }
}
