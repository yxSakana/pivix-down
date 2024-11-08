import QtQuick 2.15
import QtQuick.Controls 2.15

ScrollView {
    id: root
    property int rootWidth: 840
    property int rootHeight: 600
    width: rootWidth
    height: rootHeight
//    boundsBehavior: false
    contentHeight: {
        var totalHeight = 0;
        for (var i = 0; i < root.children.length; ++i) {
            totalHeight += root.children[i].height
        }
        return totalHeight;
    }
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn
//    visible: true
    Component.onCompleted: {
        console.log(root.height)
    }
    Rectangle {
        id: userFace
        property int r: 260

        x: rootWidth * 0.1
        y: rootHeight * 0.07
        width: r
        height: r
        radius: r / 2
        color: "black"
            Component.onCompleted: {
                console.log(parent.height)
            }
    }
    Rectangle {
        id: userBaseInfo
        y: rootHeight * 0.16
        anchors.left: userFace.right
        anchors.leftMargin: rootWidth * 0.12
        Column {
            spacing: 10
            Repeater {
                model: ["Name: himitsu", "uid: 657984112", "Fans: 2485", "Image: 132", "Novel: 0", "Manga: 3"]
                Text {
                    text: modelData
                    font.pixelSize: 16
                }
            }
        }
    }
    Rectangle {
        id: userFaceDivisionLine
        width: rootWidth * 0.9
        height: 3
        color: "#33000000"
        anchors.topMargin: rootHeight * 0.02
        anchors.top: userFace.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
    Rectangle {
        id: imageRect
        width: rootWidth * 0.85
        height: rootHeight * 0.4
        anchors.top: userFaceDivisionLine.bottom
        anchors.topMargin: rootHeight * 0.02
        anchors.horizontalCenter: parent.horizontalCenter
        color: "transparent"
    //        color: "black"
        Text {
            id: imageTitle
            text: "Image"
            font.bold: true
            font.italic: true
            font.underline: true
            font.pixelSize: rootWidth * 0.05
        }
        Row {
            width: rootWidth
            height: rootHeight * 0.8
            anchors.top: imageTitle.bottom
            anchors.topMargin: rootHeight * 0.02
            spacing: 4
            Repeater {
                model: 4
                Rectangle {
                    width: imageRect.width / 4
                    height: imageRect.width / 4
                    color: "black"
                }
            }
        }
    }
    Rectangle {
        id: imageDivisionLine
        width: rootWidth * 0.9
        height: 3
        color: "#33000000"
        anchors.topMargin: rootHeight * 0.08
        anchors.top: imageRect.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
    Rectangle {
        id: novelRect
        width: rootWidth * 0.85
        height: rootHeight * 0.3
        anchors.top: imageDivisionLine.bottom
        anchors.topMargin: rootHeight * 0.03
        anchors.horizontalCenter: parent.horizontalCenter
        color: "transparent"
//        color: "black"
        Text {
            id: novelTitle
            text: "Novel"
            font.bold: true
            font.italic: true
            font.underline: true
            font.pixelSize: rootWidth * 0.05
        }
        Row {
            width: rootWidth
            height: rootHeight * 0.8
            anchors.top: novelTitle.bottom
            anchors.topMargin: rootHeight * 0.02
            spacing: 4
            Repeater {
                model: 4
                Rectangle {
                    width: imageRect.width / 4
                    height: imageRect.width / 4
                    color: "black"
                }
            }
        }
    }
    Rectangle {
        id: novelDivisionLine
        width: rootWidth * 0.9
        height: 3
        color: "#33000000"
        anchors.topMargin: rootHeight * 0.17
        anchors.top: novelRect.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
    Rectangle {
        id: mangaRect
        width: rootWidth * 0.85
        height: rootHeight * 0.3
        anchors.top: novelDivisionLine.bottom
        anchors.topMargin: rootHeight * 0.03
        anchors.horizontalCenter: parent.horizontalCenter
//        color: "black"
        color: "transparent"
        Text {
            id: mangaTitle
            text: "Manga"
            font.bold: true
            font.italic: true
            font.underline: true
            font.pixelSize: rootWidth * 0.05
        }
        Row {
            width: rootWidth
            height: rootHeight * 0.8
            anchors.top: mangaTitle.bottom
            anchors.topMargin: rootHeight * 0.02
            spacing: 4
            Repeater {
                model: 4
                Rectangle {
                    width: imageRect.width / 4
                    height: imageRect.width / 4
                    color: "black"
                }
            }
        }
    }
}
