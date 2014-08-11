# Copyright (C) 2014 Canonical Ltd
#
# This file is part of Ubuntu Clock App
#
# Ubuntu Clock App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Ubuntu Clock App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the Clock App - Alarm"""

from __future__ import absolute_import

import datetime
import unittest

from autopilot.matchers import Eventually
from testtools.matchers import Equals
from ubuntu_clock_app.tests import ClockAppTestCase
from autopilot.platform import model


class TestAlarm(ClockAppTestCase):

    """Tests the alarm page features"""
    scenarios = [
        ('random',
            {'alarm_name': 'Random days Alarm Test',
             'days': ['Tuesday', 'Wednesday', 'Friday', 'Sunday'],
             'expected_recurrence': 'Tuesday, Wednesday, Friday, Sunday',
             'expected_time': '06:10:00',
             'enabled_value': True,
             'test_sound_name': 'Bliss'
             }),

        ('weekday',
            {'alarm_name': 'Weekday Alarm Test',
             'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
             'expected_recurrence': 'Weekdays',
             'expected_time': '06:10:00',
             'enabled_value': True,
             'test_sound_name': 'Bliss'
             }),

        ('weekend',
            {'alarm_name': 'Weekend Alarm Test',
             'days': ['Saturday', 'Sunday'],
             'expected_recurrence': 'Weekends',
             'expected_time': '06:10:00',
             'enabled_value': True,
             'test_sound_name': 'Bliss'
             })
    ]

    def setUp(self):
        """ This is needed to wait for the application to start.

        In the testfarm, the application may take some time to show up.

        """
        super(TestAlarm, self).setUp()
        self.assertThat(
            self.main_view.visible, Eventually(Equals(True)))

        self.page = self.main_view.open_alarm()

    # TODO
    # Due to bug https://bugs.launchpad.net/ubuntu-calendar-app/+bug/1328600
    # this test cannot be run on device, so until the bug is not fixed we are
    # skipping the test if model not Desktop.
    @unittest.skipIf(model() != 'Desktop',
                     "datepicker does not work correctly on device")
    def test_add_recurring_type_alarm_must_add_to_alarm_list(self):
        """Test to check if alarms are saved properly

        This test saves some random days, weekends and weekdays types of alarm
        and verifies if they are added to the alarm list in the alarm page.

        """
        time_to_set = datetime.time(6, 10, 0)
        expected_alarm_info = (
            self.alarm_name, self.expected_recurrence, self.enabled_value,
            self.expected_time)

        self.page.add_single_alarm(
            self.alarm_name, self.days, time_to_set, self.test_sound_name)

        alarmlistPage = self.main_view.get_AlarmList()
        saved_alarms = alarmlistPage.get_saved_alarms()
        self.assertIn(expected_alarm_info, saved_alarms)

        # TODO: Remove this statement once proper support for cleaning the
        # test alarm environment is added. Until then remove the alarm
        # created during the test at the end of the test.
        # -- nik90 - 2014-03-03
        alarmlistPage.delete_alarm(index=0)