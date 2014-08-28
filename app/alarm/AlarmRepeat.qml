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
import Ubuntu.Components.ListItems 1.0 as ListItem

Page {
    id: _alarmRepeatPage
    objectName: "alarmRepeatPage"

    // Property to set the alarm days of the week in the edit alarm page
    property var alarm

    visible: false
    title: i18n.tr("Repeat")

    /*
     By Default, the alarm is set to Today. However if it is a one-time alarm,
     this should be set to none, since this page shows the days the alarm
     repeats on and a one-time alarm doesn't repeat on any day. While exiting
     the page, if the alarm is still a one-time alarm, then the alarm is set
     back to its original value (Today).
    */
    Component.onCompleted: {
        if (alarm.type === Alarm.OneTime)
            alarm.daysOfWeek = 0
    }

    Component.onDestruction: {
        if (alarm.type === Alarm.OneTime)
            alarm.daysOfWeek = Alarm.AutoDetect
    }

    ListModel {
        id: daysModel

        ListElement {
            day: "1"
            flag: Alarm.Monday
        }

        ListElement {
            day: "2"
            flag: Alarm.Tuesday
        }

        ListElement {
            day: "3"
            flag: Alarm.Wednesday
        }

        ListElement {
            day: "4"
            flag: Alarm.Thursday
        }

        ListElement {
            day: "5"
            flag: Alarm.Friday
        }

        ListElement {
            day: "6"
            flag: Alarm.Saturday
        }

        ListElement {
            day: "0"
            flag: Alarm.Sunday
        }
    }

    Column {
        id: _alarmDayColumn

        anchors.fill: parent

        Repeater {
            id: _alarmDays
            objectName: 'alarmDays'

            model: daysModel

            ListItem.Standard {
                id: _alarmDayHolder
                objectName: "alarmDayHolder" + index

                Label {
                    id: _alarmDay
                    objectName: 'alarmDay' + index

                    anchors {
                        left: parent.left
                        leftMargin: units.gu(2)
                        verticalCenter: parent.verticalCenter
                    }

                    color: UbuntuColors.midAubergine
                    text: Qt.locale().standaloneDayName(day, Locale.LongFormat)
                }

                control: Switch {
                    objectName: 'daySwitch' + index
                    checked: (alarm.daysOfWeek & flag) == flag && alarm.type === Alarm.Repeating
                    onCheckedChanged: {
                        if (checked) {
                            alarm.daysOfWeek |= flag
                        } else {
                            alarm.daysOfWeek &= ~flag
                        }

                        if (alarm.daysOfWeek > 0) {
                            alarm.type = Alarm.Repeating
                        } else {
                            alarm.type = Alarm.OneTime
                        }
                    }
                }
            }
        }
    }
}
