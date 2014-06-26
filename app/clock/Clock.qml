/*
 * Copyright (C) 2014 Canonical Ltd
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.0
import Ubuntu.Components 1.1
import "../components"

ClockCircle {
    id: _outerCircle

    // Property to set the digital time label
    property string time: Qt.formatTime(new Date())
    
    isOuter: true

    Component.onCompleted: clockOpenAnimation.start()
    
    ParallelAnimation {
        id: clockOpenAnimation
        
        PropertyAnimation {
            target: _outerCircle
            property: "width"
            to: units.gu(32)
            duration: 900
        }
        
        ScriptAction {
            script: animationTimer.start()
        }
    }
    
    ClockCircle {
        id: _innerCircle

        anchors.centerIn: parent
        
        Timer {
            id: animationTimer
            interval: 200
            repeat: false
            onTriggered: _innerCircleAnimation.start()
        }
        
        ParallelAnimation {
            id: _innerCircleAnimation
            
            PropertyAnimation {
                target: _innerCircle
                property: "width"
                to: units.gu(23)
                duration: 900
            }
            
            PropertyAnimation {
                target: _digitalTimeRow
                property: "digitalTimeFontPixelSize"
                to: units.dp(62)
                duration: 900
            }

            PropertyAnimation {
                target: _digitalTimePeriod
                property: "font.pixelSize"
                to: units.dp(24)
                duration: 900
            }
        }

        Row {
            id: _digitalTimeRow
            property real digitalTimeFontPixelSize: units.dp(1)
            anchors {
                centerIn: parent
            }
        
            Label {
                id: _digitalTimeHours
                color: UbuntuColors.midAubergine
                font.pixelSize: _digitalTimeRow.digitalTimeFontPixelSize
                font.weight: Font.Light
                text: time.split(":")[0]
            }

            Label {
                id: _digitalTimeDivider
                color: UbuntuColors.coolGrey
                font.pixelSize: _digitalTimeRow.digitalTimeFontPixelSize
                font.weight: Font.Light
                text: ":"
            }

            Label {
                id: _digitalTimeMinutes
                color: UbuntuColors.midAubergine
                font.pixelSize: _digitalTimeRow.digitalTimeFontPixelSize
                font.weight: Font.Light
                text: time.split(":")[1].split(" ")[0]
            }
        }

        Label {
            id: _digitalTimePeriod
            property string period: time.split(":")[1].split(" ")[1] !== undefined
                                    ? time.split(":")[1].split(" ")[1] : ""
            anchors {
                top: _digitalTimeRow.bottom
                horizontalCenter: parent.horizontalCenter
            }
            color: UbuntuColors.midAubergine
            font.pixelSize: units.dp(1)
            font.weight: Font.Light
            visible: period !== ""
            text: period
        }
    }
}
