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
    Binding {
        target: taskbar.inputHolder
        property: "z"
        value: 1
        when: taskbar.inputHolder !== null
        restoreMode: Binding.RestoreBindingOrValue
    }
