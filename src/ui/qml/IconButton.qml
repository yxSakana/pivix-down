import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12

Rectangle {
    property alias icon: img
    signal clicked()

    id: rect
    Image {
        id: img
        width: parent.width
        height: parent.height
        anchors.centerIn: parent
    }
    Rectangle {
        id: maskSource
        visible: false
        color: "transparent"
        border.color: "#35000000"
        border.width: 1
        anchors.fill: parent
    }
    DropShadow {
        id: mask
        anchors.fill: rect
        source: maskSource
        visible: false
        color: "#80000000"
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
           rect.color = "#33565A66"
        }
        onPressed: {
            maskSource.visible = true
            mask.visible = true
        }
        onReleased: {
            maskSource.visible = false
            mask.visible = false
        }
        onClicked: {
            rect.clicked()
        }
        onExited: {
            maskSource.visible = false
            mask.visible = false
            mask.color = "#80000000"
            rect.color = "transparent"
        }
   }
}
