"""Tests for cpu_info module."""

import unittest

from system_intelligence.cpu_info import _get_cache_size


class Tests(unittest.TestCase):

    def test_cpu_cache_size(self):
        info = _get_cache_size(1, {'l1_cache_size': '512'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)

    def test_cpu_cache_size_with_units(self):
        info = _get_cache_size(1, {'l1_cache_size': '512 kB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1000)
        info = _get_cache_size(1, {'l1_cache_size': '512 KB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)
        info = _get_cache_size(1, {'l1_cache_size': '512 KiB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)
        info = _get_cache_size(1, {'l1_cache_size': '2 MB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 2 * 1024 ** 2)
        info = _get_cache_size(1, {'l1_cache_size': '4 MiB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 4 * 1024 ** 2)
