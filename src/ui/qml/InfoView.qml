import QtQuick 2.15
import QtQuick.Window 2.2

Window {
    width: 840
    height: 600
    visible: true
    Row {
        width: 840
        height: 600
        anchors.centerIn: parent
        leftPadding: 50
        topPadding: 50
//        spacing: 20
        Rectangle {
            id: leftRect
            width: parent.width / 2 - 60
            height: parent.height - 100
//            color: "#33888888"
            color: "transparent"
            Column {
                y: parent.height * 0.2
                anchors.right: parent.right
                anchors.rightMargin: 20
                leftPadding: 40
                spacing: 15
                Image {
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "../../../resource/cookie.png"
                }
                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "This is a test text"
                    color: "#ff3399"
                    font.pixelSize: 16
                }
            }
        }
        Rectangle {
            width: parent.width / 2 - 60
            height: parent.height - 100
            color: "transparent"
//            color: "#33888888"
            Rectangle {
                width: parent.width * 0.9
                height: parent.height * 0.7
//                x: parent.width * 0.10
                y: parent.height * 0.15
                color: "transparent"
                Column {
                    anchors.fill: parent
                    anchors.centerIn: parent
                    leftPadding: parent.width * 0.05
                    topPadding: parent.height * 0.05
                    spacing: 20
                    Repeater {
                        width: parent.width
                        height: parent.height * 0.7
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        model: ["title: Test Title", "user: himitsu", "uid: 546546547", "pid: 12348483", "tags: aTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextTextText"]
                        Text {
                            width: parent.width
                            anchors.horizontalCenter: parent.horizontalCenter
                            horizontalAlignment: Text.AlignLeft
                            text: modelData
    //                        clip: true
                            elide: Text.ElideRight
                            wrapMode: Text.WrapAnywhere
                            font.pixelSize: 16
                        }
                    }
                }
            }
        }
    }
}
