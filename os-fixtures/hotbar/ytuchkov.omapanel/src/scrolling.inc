    property var scrollState: ({ enabled: false, addresses: [] })
    property string dragAddress: ""
    property string dropAddress: ""
    property bool dropAfter: false
    readonly property bool scrollingMode: !!scrollState.enabled
    property var scrollingItems: []
    function setScrollState(next) {
        scrollState = next;
        var values = Hyprland.toplevels.values;
        var items = next.addresses.map(function(address) {
            for (var i = 0; i < values.length; i++) {
                if (normalizedAddress(values[i]) === address)
                    return { app: null, window: values[i] };
            }
            return null;
        }).filter(function(item) { return item && !isExcludedWindow(item.window); });
        scrollingItems = pinnedItems.filter(function(item) { return !item.window; }).concat(items);
    }
    function updateDrop(x, y) { chrome.updateDrop(x, y); }
    function reorderDrop() {
        if (dragAddress && dropAddress && dragAddress !== dropAddress && !scrollMove.running) {
            scrollMove.command = ["python3", Qt.resolvedUrl("scripts/scroll-order.py").toString().replace("file://", ""),
                dragAddress, dropAddress, dropAfter ? "after" : "before"];
            scrollMove.running = true;
        }
        dragAddress = "";
        dropAddress = "";
    }
    Timer {
        id: scrollRefresh
        interval: 100
        onTriggered: { if (!scrollQuery.running && !scrollMove.running) scrollQuery.running = true; }
    }
    Timer {
        interval: 1500
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: { if (!scrollQuery.running && !scrollMove.running) scrollQuery.running = true; }
    }
    Process {
        id: scrollQuery
        command: ["python3", Qt.resolvedUrl("scripts/scroll-order.py").toString().replace("file://", "")]
        stderr: StdioCollector {
            onStreamFinished: { if (text.trim()) console.warn("Hotbar query:", text); }
        }
        stdout: StdioCollector {
            onStreamFinished: {
                try {
                    var next = JSON.parse(text);
                    if (!taskbar.dragAddress && JSON.stringify(next) !== JSON.stringify(taskbar.scrollState)) taskbar.setScrollState(next);
                } catch (error) { console.warn("Hotbar order:", error); }
            }
        }
    }
    Process {
        id: scrollMove
        stderr: StdioCollector {
            onStreamFinished: { if (text.trim()) console.warn("Hotbar move:", text); }
        }
        onExited: scrollRefresh.restart()
    }
