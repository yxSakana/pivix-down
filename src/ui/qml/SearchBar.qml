import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12

Rectangle {
    id: searchRect
    width: 600
    height: 40
//    anchors.centerIn: parent
//    Component.onCompleted: {
//        console.log(searchRect.width)
//    }
    FocusScope {
       anchors.fill: parent
       anchors.centerIn: parent
       focus: true
       TextField {
           id: userInput
           anchors.fill: parent
           anchors.centerIn: parent
           focus: true
           background: Rectangle {
               width: parent.width
//               border.color: userInput.focus? "#00cccc": "#fef8f7"
               border.color: userInput.activeFocus? "#00cccc": "#fef8f7"
               radius: 10
           }
           leftPadding: 20
           rightPadding: 60
           font.pixelSize: 16
           placeholderText: "Input Please"
       }
        DropShadow {
            anchors.fill: userInput
            source: userInput
            color: "#80000000"
        }
        Rectangle {
            id: line
            width: 2
            height: userInput.height - 8
            anchors.rightMargin: 4
            color: "#dcdcdc"
            opacity: 0.7
            anchors.right: searchBtnRect.left
            anchors.verticalCenter: userInput.verticalCenter
        }
        Rectangle {
            id: searchBtnRect
            width: 30
            height: 30
            anchors.right: userInput.right
            anchors.verticalCenter: userInput.verticalCenter
            anchors.rightMargin: 10
            color: "transparent"
            Image {
                id: icon
                mipmap: true
//                smooth: true
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: "../../../resource/search.png"
            }
            MouseArea {
                anchors.fill: parent
                onPressed: { searchBtnRect.color = "#dcdcdc" }
                onReleased: { searchBtnRect.color = "transparent" }
            }
        }
    }
}
