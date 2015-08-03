# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from stats import get_all_vectors, load_clusters

class TestStats(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_get_all_vectors(self):
    get_all_vectors('test/lines_test.txt', 'test/google-10000-english.txt')

  def test_load_clusters(self):
    self.assertEqual(len(load_clusters('test/clusters.txt')), 3356)

if __name__ == '__main__':
  unittest.main()
