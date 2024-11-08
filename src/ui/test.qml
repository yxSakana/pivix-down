import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

ApplicationWindow  {
    width: 640
    height: 480
    visible: true
    title: qsTr("qml 实现csdn的搜索框，不规则圆角实现")

    background: Rectangle {
        anchors.fill: parent
        color:"White"
    }

    Rectangle {
        id: searchBar
        anchors.centerIn: parent
        width:400
        height: 35
        border.color: "#fc5531"
        border.width: 1
        radius: searchBar.height / 2

        TextInput {
            anchors.leftMargin: 20
            anchors.right: btn.left
            anchors.left: parent.left
            font.pointSize: 12
            color: "Black"
            y:8
            maximumLength: 30
            focus: true

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    searchBar.border.color = "#fc1944"
                }

                onExited: {
                    searchBar.border.color = "#fc5531"
                }
            }
        }

        // right button #fc1944
        Rectangle {
            id:btn
            width: 80
            height: searchBar.height
            anchors.right: parent.right
            anchors.top: parent.top
            color: "#fc5531"
            layer.enabled: true
            layer.effect: OpacityMask{
                maskSource: Rectangle{
                    width: 80
                    height: btn.height
                    radius: btn.height / 2
                    //左侧
                    Rectangle{
                        width: 20
                        height: btn.height
                    }
                }
            }

            Image {
                id: image_search
                width: 20
                height:20
                x:10
                anchors.verticalCenter: parent.verticalCenter

                source: "qrc:/res/img/search.png"
            }

            Text {
                id: searchTxt
                color: "White"
                text: qsTr("搜索")
                anchors.verticalCenter: parent.verticalCenter
                anchors.left:image_search.right
                anchors.leftMargin: 1
                font.pointSize: 12
                font.bold: true
            }


            MouseArea  {
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    btn.color = "#fc1944"
                }

                onExited: {
                    btn.color = "#fc5531"
                }
            }
        }
    }
}