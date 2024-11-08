import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    property alias text: textEdit.text

    id: frame
    border.color: textEdit.activeFocus ? "#6f9ada": "#88A1A5A6"
    border.width: 3
    radius: 5
    clip: true
    TextEdit {
        id: textEdit
        y: -vbar.position * textEdit.height
        width: parent.width
        height: 200
        leftPadding: 20
        rightPadding: 20
        font.pixelSize: 16
        selectByMouse:true
        text: "asfas"
        wrapMode: TextEdit.WrapAnywhere
    }
    MouseArea {
        propagateComposedEvents: true
        anchors.fill: parent
        onWheel: {
            if (wheel.angleDelta.y > 0) {
                vbar.decrease();
            } else {
                vbar.increase();
            }
        }
        onPressed: {
            mouse.accepted = false
        }
        onClicked: {
            textEdit.forceActiveFocus();
        }
    }
    ScrollBar {
        id: vbar
        width: 10
        // size: frame.height / textEdit.height
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        hoverEnabled: true 
        active: hovered || pressed
        orientation: Qt.Vertical
    }

}
