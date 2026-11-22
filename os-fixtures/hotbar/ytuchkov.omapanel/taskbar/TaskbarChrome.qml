import QtQuick
import qs.Commons
import qs.Ui

Item {
    id: chrome

    required property var taskbar

    anchors.centerIn: parent
    implicitWidth: content.implicitWidth + (taskbar ? taskbar.barPadHorizontal : 0) * 2
    implicitHeight: taskbar ? taskbar.panelHeight : content.implicitHeight
    width: implicitWidth
    height: implicitHeight
    readonly property bool trimEdges: !!(taskbar && taskbar.trimEdgeItemGaps)
    readonly property int pinnedCount: taskbar && taskbar.pinnedItems ? taskbar.pinnedItems.length : 0
    readonly property int runningCount: taskbar && taskbar.runningWindows ? taskbar.runningWindows.length : 0

    function updateDrop(x, y) {
        taskbar.dropAddress = "";
        for (var i = 0; i < windowRepeater.count; i++) {
            var item = windowRepeater.itemAt(i);
            if (!item || !item.entry || !item.entry.window) continue;
            var point = item.mapFromItem(taskbar, x, y);
            if (point.x >= 0 && point.x < item.width && point.y >= 0 && point.y < item.height) {
                taskbar.dropAddress = taskbar.normalizedAddress(item.entry.window);
                taskbar.dropAfter = point.x > item.width / 2;
                return;
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        radius: taskbar ? taskbar.barCornerRadius : 0
        color: taskbar ? taskbar.barBackgroundColor : "transparent"
        visible: taskbar && taskbar.barBackgroundEnabled
    }

    Row {
        id: content

        x: taskbar ? taskbar.barPadHorizontal : 0
        y: taskbar ? taskbar.barPadTop : 0
        spacing: 0

        TaskbarSeparator {
            taskbar: taskbar
            visible: !!(taskbar && taskbar.leadingSeparator && taskbar.pinnedApps && taskbar.pinnedApps.length > 0)
        }

        Repeater {
            id: windowRepeater
            model: taskbar ? (taskbar.scrollingMode ? taskbar.scrollingItems : taskbar.pinnedItems) : []

            Item {
                required property int index
                readonly property var entry: taskbar.scrollingMode
                    ? taskbar.scrollingItems[index]
                    : taskbar.pinnedItems[index]
                width: pinnedChip.width
                height: pinnedChip.height
                AppChip {
                    id: pinnedChip
                    taskbar: taskbar
                    app: parent.entry ? parent.entry.app : null
                    appWindow: parent.entry ? parent.entry.window : null
                    pinned: !!app
                    includeLeadingHitPadding: !chrome.trimEdges || parent.index > 0
                    includeTrailingHitPadding: true
                }
            }

        }

        TaskbarSeparator {
            taskbar: taskbar
            visible: !!(taskbar && !taskbar.scrollingMode && taskbar.sectionSeparator && taskbar.pinnedApps && taskbar.pinnedApps.length > 0 && taskbar.runningWindows && taskbar.runningWindows.length > 0)
        }

        Repeater {
            model: taskbar && !taskbar.scrollingMode ? taskbar.runningWindows : []

            Row {
                required property int index
                readonly property var modelData: taskbar.runningWindows[index]

                spacing: 0

                TaskbarSeparator {
                    taskbar: taskbar
                    visible: !!(taskbar && taskbar.startsWorkspaceGroup(parent.index, parent.modelData))
                }

                AppChip {
                    taskbar: taskbar
                    app: null
                    appWindow: parent.modelData
                    pinned: false
                    includeLeadingHitPadding: !chrome.trimEdges || parent.index > 0 || chrome.pinnedCount > 0
                    includeTrailingHitPadding: !chrome.trimEdges || parent.index < chrome.runningCount - 1
                }

            }

        }

    }

}
