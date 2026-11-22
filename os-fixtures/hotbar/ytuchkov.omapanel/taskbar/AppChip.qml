import QtQuick
import qs.Commons
import qs.Ui

WidgetButton {
    id: chip

    required property var taskbar
    required property var app
    required property var appWindow
    required property bool pinned

    // @include AppChipProperties.inc

    // @include AppChipVisuals.inc

    Component.onDestruction: {
        if (chip.pointerHovered && taskbar)
            taskbar.handleChipHover(chip, false, chip.appWindow);
    }

    // @include AppChipDrag.inc

    MouseArea {
        id: pointer
        property real pressX: 0
        property bool moved: false
        onPressed: function(mouse) {
            pressX = mouse.x;
            moved = false;
        }
        onPositionChanged: function(mouse) {
            if (!(pressedButtons & Qt.LeftButton) || !taskbar.scrollingMode || !chip.appWindow) return;
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
        onReleased: { if (moved) taskbar.reorderDrop(); }
        onCanceled: { taskbar.dragAddress = ""; taskbar.dropAddress = ""; }
        anchors.fill: parent
        z: 10
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
        hoverEnabled: true
        preventStealing: true
        cursorShape: Qt.PointingHandCursor
        onEntered: chip.setPointerHovered(true)
        onExited: chip.setPointerHovered(false)
        onClicked: function(mouse) {
            if (moved) return;
            taskbar.handleConfiguredClick(chip.app, chip.appWindow, chip, mouse.button, mouse.modifiers);
        }
        onWheel: function(wheel) {
            var delta = wheel.angleDelta.y !== 0 ? wheel.angleDelta.y : wheel.angleDelta.x;
            wheel.accepted = chip.handleBarWheel(delta);
        }
    }

}
