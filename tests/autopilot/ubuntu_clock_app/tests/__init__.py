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

"""clock-app autopilot tests."""

import os.path
import os
import shutil
import logging
import fixtures

from autopilot import logging as autopilot_logging
from ubuntuuitoolkit import (
    base,
    emulators as toolkit_emulators
)

from ubuntu_clock_app import emulators

logger = logging.getLogger(__name__)


def find_local_path(what):

    """Depending on which directory we build in, paths might be
    named differently. This way we find them and don't have to
    hook into cmake variables.

    """
    if not what:
        return None
    if what.endswith("/"):
        what = what[:-1]
    for dirpath, dirnames, filenames in os.walk("../.."):
        avail_dirs = map(lambda a: os.path.abspath(os.path.join(dirpath, a)),
                         dirnames)
        match_dirs = filter(lambda a: a.endswith(what), avail_dirs)
        if match_dirs:
            return match_dirs[0]

        avail_files = map(lambda a: os.path.abspath(os.path.join(dirpath, a)),
                          filenames)
        match_files = filter(lambda a: a.endswith(what), avail_files)
        if match_files:
            return match_files[0]
    return None


class ClockAppTestCase(base.UbuntuUIToolkitAppTestCase):

    """A common test case class that provides several useful methods for
    clock-app tests.

    """

    local_location = os.path.dirname(os.path.dirname(os.getcwd()))
    local_location_qml = find_local_path("app/ubuntu-clock-app.qml")
    local_location_backend = find_local_path("backend/")
    # FIXME: this is hard-coded ('builddir') and needs to be the actual path.
    installed_location_backend = \
        '/usr/share/ubuntu-clock-app/builddir/backend'
    installed_location_qml = \
        '/usr/share/ubuntu-clock-app/app/ubuntu-clock-app.qml'

    # note this directory could change to com.ubuntu.clock at some point
    sqlite_dir = os.path.expanduser(
        "~/.local/share/com.ubuntu.clock.devel")
    backup_dir = sqlite_dir + ".backup"

    def setUp(self):
        # backup and wipe db's before testing
        self.temp_move_sqlite_db()
        self.addCleanup(self.restore_sqlite_db)

        launch, self.test_type = self.get_launcher_method_and_type()
        self.useFixture(fixtures.EnvironmentVariable('LC_ALL', newvalue='C'))
        super(ClockAppTestCase, self).setUp()

        launch()

    def get_launcher_method_and_type(self):
        if os.path.exists(self.local_location_backend):
            launcher = self.launch_test_local
            test_type = 'local'
        elif os.path.exists(self.installed_location_backend):
            launcher = self.launch_test_installed
            test_type = 'deb'
        else:
            launcher = self.launch_test_click
            test_type = 'click'
        return launcher, test_type

    @autopilot_logging.log_action(logger.info)
    def launch_test_local(self):
        self.app = self.launch_test_application(
            base.get_qmlscene_launch_command(),
            self.local_location_qml,
            "-I", self.local_location_backend,
            app_type='qt',
            emulator_base=toolkit_emulators.UbuntuUIToolkitEmulatorBase)

    @autopilot_logging.log_action(logger.info)
    def launch_test_installed(self):
        self.app = self.launch_test_application(
            base.get_qmlscene_launch_command(),
            self.installed_location_qml,
            "-I", self.installed_location_backend,
            app_type='qt',
            emulator_base=toolkit_emulators.UbuntuUIToolkitEmulatorBase)

    @autopilot_logging.log_action(logger.info)
    def launch_test_click(self):
        self.app = self.launch_click_package(
            "com.ubuntu.clock.devel",
            emulator_base=toolkit_emulators.UbuntuUIToolkitEmulatorBase)

    def temp_move_sqlite_db(self):
        try:
            shutil.rmtree(self.backup_dir)
        except:
            pass
        else:
            logger.warning("Prexisting backup database found and removed")

        try:
            shutil.move(self.sqlite_dir, self.backup_dir)
        except:
            logger.warning("No current database found")
        else:
            logger.debug("Backed up database")

    def restore_sqlite_db(self):
        if os.path.exists(self.backup_dir):
            if os.path.exists(self.sqlite_dir):
                try:
                    shutil.rmtree(self.sqlite_dir)
                except:
                    logger.error("Failed to remove test database and restore" /
                                 "database")
                    return
            try:
                shutil.move(self.backup_dir, self.sqlite_dir)
            except:
                logger.error("Failed to restore database")

    @property
    def main_view(self):
        return self.app.wait_select_single(emulators.MainView)
