    opacity: taskbar.dragAddress && appWindow && taskbar.dragAddress === taskbar.normalizedAddress(appWindow) ? 0.45 : 1
    Rectangle {
        width: 2
        height: parent.height
        x: taskbar.dropAfter ? parent.width - width : 0
        color: Color.foreground
        visible: !!chip.appWindow && !!taskbar.dragAddress && taskbar.dropAddress === taskbar.normalizedAddress(chip.appWindow) && taskbar.dragAddress !== taskbar.dropAddress
    }
