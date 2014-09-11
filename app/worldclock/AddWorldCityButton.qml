/*
 * Copyright (C) 2014 Canonical Ltd
 *
 * This file is part of Ubuntu Clock App
 *
 * Ubuntu Clock App is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * Ubuntu Clock App is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.3
import Ubuntu.Components 1.1
import "../components"

AbstractButton {
    id: addWorldCityButton

    width: childrenRect.width
    height: childrenRect.height

    Row {
        spacing: units.gu(1)

        width: childrenRect.width
        height: _addButton.height

        Label {
            text: i18n.tr("Add")
            color: UbuntuColors.midAubergine
            anchors.verticalCenter: parent.verticalCenter
        }

        ClockCircle {
            id: _addButton

            isOuter: true
            width: units.gu(5)

            ClockCircle {
                width: units.gu(3.5)
                anchors.centerIn: parent

                Icon {
                    anchors.centerIn: parent
                    color: UbuntuColors.coolGrey
                    name: "add"
                    height: units.gu(2)
                    width: height
                }
            }
        }

        Label {
            text: i18n.tr("City")
            color: UbuntuColors.midAubergine
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    onClicked: {
        pageStack.push(Qt.resolvedUrl("WorldCityList.qml"))
    }
}