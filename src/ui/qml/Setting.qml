import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

//Window {
//    width: 840
//    height: 600
//    visible: true
    Rectangle {
        id: settingRect
        width: parent.width * 0.95
        height: parent.height * 0.95
//        color: "black"
        color: "transparent"
//        anchors.centerIn: parent
        Text {
            id: title
            y: parent.height * 0.04
            anchors.horizontalCenter: settingRect.horizontalCenter
            font.pixelSize: 36
            font.bold: true
            font.italic: true
            text: "Pixiv-Down"
            color: "#f63375"
        }
        Row {
            id: downloadPathInputLayout
            anchors.top: title.bottom
            anchors.horizontalCenter: settingRect.horizontalCenter
            topPadding: 40
            spacing: 20
            Text {
                id: doanloadPathLabel
                text: "<b>Download Path: </b>"
                font.pixelSize: 16
            }
            TextField {
                id: downloadPathInput
                width: settingRect.width * 0.6
                background: Rectangle {
                    width: parent.width
//                    color: "#fef8f7"
                    border.color: downloadPathInput.focus? "#00cccc": "#400000cc"
                    radius: 10
               }
            }
            IconButton {
                   width: downloadPathInput.height
                   height: downloadPathInput.height
                   icon.source: "../../../resource/directory.png"
            }
            IconButton {
               width: downloadPathInput.height
               height: downloadPathInput.height
               icon.source: "../../../resource/jump.png"
               icon.width: 20
               icon.height: 20
            }
        }
        Row {
            id: proxyInputLayout
            anchors.top: downloadPathInputLayout.bottom
            anchors.left: downloadPathInputLayout.left
            topPadding: 50
            spacing: 20
            Text {
                id: proxyLabel
                text: "<b>Proxy: </b>"
                font.pixelSize: 16
                width: doanloadPathLabel.width
            }
            TextField {
                id: proxyInput
                width: settingRect.width * 0.6
                background: Rectangle {
                    width: parent.width
                    border.color: proxyInput.focus? "#00cccc": "#400000cc"
                    radius: 10
               }
            }
            Switch {
                id: proxySwitch
                checked: true
                onCheckedChanged: {
                    proxyInput.background.color = proxySwitch.checked? "white": "#11000000"
                    proxyInput.enabled = proxySwitch.checked
                }
                Component.onCompleted: {
                    proxyInput.background.color = proxySwitch.checked? "white": "#11000000"
                    proxyInput.enabled = proxySwitch.checked
                }
            }
        }
        Column {
            anchors.top: proxyInputLayout.bottom
            anchors.left: downloadPathInputLayout.left
            topPadding: 40
            spacing: 25
            Row {
                spacing: 20
                Text {
                    text: "<b>cookies: </b>"
                    font.pixelSize: 16
                    width: doanloadPathLabel.width
                }
                TextField {
                    id: cookiesInput
                    width: settingRect.width * 0.6
                    background: Rectangle {
                        width: parent.width
                        border.color: cookiesInput.focus? "#00cccc": "#400000cc"
                        radius: 10
                   }
                }
                Rectangle {
                    width: {
                        var totalWidth = 0;
                        for (var i = 0; i < downloadPathInputLayout.children.length; ++i) {
                            if (downloadPathInputLayout.children[i] instanceof IconButton) {
                                totalWidth += downloadPathInputLayout.children[i].width;
                            }
                        }
                        return totalWidth;
                    }
                    height: cookiesInput.height
                    color: "transparent"
                    IconButton {
                        anchors.centerIn: parent
                        width: cookiesInput.height
                        height: cookiesInput.height
                        icon.source: "../../../resource/directory.png"
                    }
                }
            }
            ScrollTextEdit {
                width: parent.width
                height: 200
                text: "first_visit_datetime_pc=2023-12-11%2016%3A47%3A01; p_ab_id=9; p_ab_id_2=5; p_ab_d_id=553596517; yuid_b=Y5ZmAAA; _ga=GA1.1.1425692826.1702280823; privacy_policy_notification=0; a_type=0; b_type=0; login_ever=yes; _gcl_au=1.1.1469303884.1702280921; cc1=2024-01-14%2020%3A32%3A13; cf_clearance=YzV.w8j60s_G1LZtAz_ijxuie0q6jrvjCk9wxitgEIg-1705231935-0-2-bb3d5a5e.74cac282.ec3c05be-0.2.1705231935; PHPSESSID=50341679_2pv0sBawSjRh4wmC5TwuPOBqS0uiQNa5; device_token=710c3a1769b253c7011f73423311e770; c_type=24; privacy_policy_agreement=0; _ga_MZ1NL4PHH0=GS1.1.1705231938.2.1.1705231963.0.0.0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _ga_75BBYNYN9J=GS1.1.1705244118.3.0.1705244118.0.0.0; __cf_bm=tsupefRKeK3A1MJqbV7rV01lHK_1pgRQWkZis87p_sI-1705252623-1-AabjIFGwy1Mt8J5n20VwZrPYGmk1m+LEGFwHIm04B/V4BDntSun3bJrIcUhkZuEqAQ25+FUaSYythfdcasPMlYgStQUCmFIIRS2/OLKMDbZ7"
            }
        }
    }
//}
