from django.test import TestCase

from cogwheels.tests.conf import settings


class AppSettingTestCase(TestCase):

    def setUp(self):
        self.appsettingshelper = settings
        self.settings_prefix = settings._prefix
        # Always clear caches between tests
        self.appsettingshelper.reset_caches()
