import QtQuick 2.15
import QtQuick.Controls 2.15
//import QtQuick.Layouts 1.15
//import QtQuick.Window 2.15
import QtGraphicalEffects 1.12

//ApplicationWindow {
//    width: 840
//    height: 600
//    visible: true
//    color: "#ffffcc"
//
    Rectangle {
        width: 600
        height: 200
//        anchors.centerIn: parent
        SearchBar {
            id: searchBar
            width: 600
            height: 40
        }

        ButtonGroup {
            id: modeGroup
        }
        Row {
            anchors.topMargin: 30
            anchors.top: searchBar.bottom
            leftPadding: 60
            spacing: 60
            Repeater {
                id: modeOptionRep
                model: ["Image", "Novel", "Manga", "User"]
                FocusScope {
                    id: modeOptionFocus
                    width: 70; height: 30
                    focus: true
                    Button {
                        id: modeOption
                        anchors.fill: parent
                        anchors.centerIn: parent
                        autoExclusive: true
                        checkable: true
                        ButtonGroup.group: modeGroup
                        background: Rectangle {
                            id: modeOptionBackground
                            anchors.fill: parent
                            anchors.centerIn: parent
                            border.color: "#88EAEBEE"
                            color: "white"
                            radius: 10
                        }
                        contentItem: Label {
                            text: modelData
                            font.pixelSize: 16
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                        }
                        MouseArea {
                            id: modeOptionMouse
                            hoverEnabled: true
                            anchors.fill: parent
                            propagateComposedEvents: true
                            onEntered: {
                                if (modeOption.checked) { return }
                                modeOptionBackground.color = "#E8F0FE"
                            }
                            onClicked: {
                                modeOptionRep.itemAt(index).children[0].checked = true
                                for (var i = 0; i < modeOptionRep.count; i++) {
                                    for (var j = 0; j < modeOptionRep.itemAt(0).children.length; j++) {
                                        var btn = modeOptionRep.itemAt(i).children[j]
                                        if (btn instanceof Button) {
//                                            console.log(modeOptionRep.itemAt(i).children[j].checked)
                                            btn.background.color = btn.checked? "#333399cc": "white"
                                            btn.contentItem.color = btn.checked? "#3062D8": "black"
                                        }
                                    }
                                }
                            }
                            onExited: {
                                if (modeOption.checked) { return }
                                modeOptionBackground.color = modeOption.checked? "#3399cc": "white"
                            }
                        }
                    }
                    DropShadow {
                        anchors.fill: modeOption
                        source: modeOption
                        color: "#40000000"
                        horizontalOffset: 2
                        verticalOffset: 2
                    }
                }
            }
        }

    }
//}