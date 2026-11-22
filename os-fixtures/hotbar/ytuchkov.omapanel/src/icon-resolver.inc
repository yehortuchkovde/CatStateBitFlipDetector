    property var resolvedIdentities: ({})

    function resolvedIdentity(toplevel) {
        var ipc = toplevel ? toplevel.lastIpcObject : null;
        return ipc ? resolvedIdentities[String(ipc.address)] : null;
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
                } catch (error) { console.warn("OmaPanel identity lookup failed"); }
            }
        }
    }

    // Debounce compositor events; retry while open to catch new launchers/icons.
    Timer {
        id: identityRefresh
        interval: 500
        onTriggered: { if (!identityResolver.running) identityResolver.running = true; }
    }
    Connections {
        target: Hyprland
        function onRawEvent(event) { identityRefresh.restart(); }
    }
    Timer {
        interval: 15000
        running: taskbar.visible
        repeat: true
        onTriggered: {
            if (!identityResolver.running) identityResolver.running = true;
        }
    }
