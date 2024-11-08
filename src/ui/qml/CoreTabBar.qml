import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15

Window {
    id: root
    width: 940
    height: 750
    visible: true
    TabBar {
        id: bar
        width: firstBtn.width
        TabButton {
            id: firstBtn
            text: qsTr("Home")
            width: root.width / 8
            height: root.height / 3
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
        }
        TabButton {
            id: secondBtn
            text: qsTr("Discover")
            width: root.width / 8
            height: root.height / 3
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: firstBtn.bottom
        }
        TabButton {
            id: thirdBtn
            text: qsTr("Activity")
            width: root.width / 8
            height: root.height / 3
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: secondBtn.bottom
        }
    }
    Rectangle {
        id: rec
        width: root.width - bar.width - root.width*0.05
//        width: 500
        height: parent.height
        anchors.left: bar.right
        anchors.leftMargin: 20
//        color: "red"
        StackLayout {
            id: stackLayout
//            anchors.fill: parent
            currentIndex: bar.currentIndex
//            currentIndex: 0
            anchors.horizontalCenter: parent.horizontalCenter
//            anchors.centerIn: parent
            Rectangle {
                width: 200
                height: 200
                color: "red"
                anchors.leftMargin: 20
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Layout.fillWidth: false
                Layout.fillHeight: false
            }
            Rectangle {
                width: 200
                height: 200
                color: "red"
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Search {
                    anchors.centerIn: parent
       //            width: parent.width * 0.95
       //            height: parent.height * 0.95
//                   Layout.topMargin: 123
//                   Layout.alignment: Qt.AlignVCenter
//                   Layout.fillHeight: false
                }
            }
            Setting {
                width: parent.width * 0.95
                height: parent.height * 0.95
            }
            Component.onCompleted: {
                console.log(stackLayout.height)
            }
        }
//        Component.onCompleted: {
//            console.log(rec.width)
//        }
    }
}
