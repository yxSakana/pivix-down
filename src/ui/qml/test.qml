import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 400
    height: 400
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

    StackLayout {
        id: stackLayout
        anchors.centerIn: parent // 将StackLayout居中对齐
        currentIndex: bar.currentIndex

        Rectangle {
            width: 100
            height: 100
            color: "red"
            Layout.alignment: Qt.AlignHCenter // 水平居中对齐
        }

        Rectangle {
            width: 200
            height: 100
            color: "green"
            Layout.alignment: Qt.AlignHCenter // 水平居中对齐
        }

        Rectangle {
            width: 300
            height: 100
            color: "blue"
            Layout.alignment: Qt.AlignHCenter // 水平居中对齐
        }
    }
}