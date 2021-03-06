# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.test import TestCase
from ..models import DatabaseUpgrade
from .factory import DatabaseUpgradeFactory


class DatabaseUpgradeTestCase(TestCase):

    def setUp(self):
        self.database_upgrade = DatabaseUpgradeFactory()

    def tearDown(self):
        self.database_upgrade.delete()

    def test_update_step(self):
        self.assertIsNone(self.database_upgrade.started_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.WAITING)
        self.assertEqual(self.database_upgrade.current_step, 0)

        self.database_upgrade.update_step(1)
        self.assertIsNotNone(self.database_upgrade.started_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.RUNNING)
        self.assertEqual(self.database_upgrade.current_step, 1)

        started_at_first = self.database_upgrade.started_at
        self.database_upgrade.update_step(2)
        self.assertEqual(self.database_upgrade.started_at, started_at_first)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.RUNNING)
        self.assertEqual(self.database_upgrade.current_step, 2)

    def test_status_error(self):
        self.assertIsNone(self.database_upgrade.finished_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.WAITING)

        self.database_upgrade.set_error()
        self.assertIsNotNone(self.database_upgrade.finished_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.ERROR)

    def test_status_success(self):
        self.assertIsNone(self.database_upgrade.finished_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.WAITING)

        self.database_upgrade.set_success()
        self.assertIsNotNone(self.database_upgrade.finished_at)
        self.assertEqual(self.database_upgrade.status, DatabaseUpgrade.SUCCESS)

    def test_is_status_error(self):
        self.assertFalse(self.database_upgrade.is_status_error)

        self.database_upgrade.set_error()
        self.assertTrue(self.database_upgrade.is_status_error)

    def test_can_do_retry(self):
        self.assertTrue(self.database_upgrade.can_do_retry)

    def test_can_do_retry_to_other_database(self):
        self.assertTrue(self.database_upgrade.can_do_retry)

        new_upgrade = DatabaseUpgradeFactory()
        self.assertTrue(new_upgrade.can_do_retry)

        self.assertTrue(self.database_upgrade.can_do_retry)

    def test_cannot_do_retry(self):
        self.assertTrue(self.database_upgrade.can_do_retry)

        new_upgrade = DatabaseUpgradeFactory(
            database=self.database_upgrade.database,
            source_plan=self.database_upgrade.source_plan
        )
        self.assertTrue(new_upgrade.can_do_retry)

        old_upgrade = DatabaseUpgrade.objects.get(id=self.database_upgrade.id)
        self.assertFalse(old_upgrade.can_do_retry)
