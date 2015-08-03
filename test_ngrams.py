# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
import numpy as np
from ngrams import initialize_n_grams_list, clean, get_n_grams_from_string, count_n_grams, get_n_grams_vec, Borg

class TestNgrams(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_initialize_n_grams_list(self):
    print initialize_n_grams_list(1)

  def test_clean(self):
    print clean("abecadło z pieca spadło123")

  def test_get_n_grams_from_string(self):
    print get_n_grams_from_string("string", 3)

  def test_count_n_grams(self):
    print count_n_grams("to jest testowy tekst".split(), 3)

  def test_n_grams_map_to_vec(self):
    self.assertItemsEqual([1.0, 0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 1.0, 2.0, 4.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0],
        get_n_grams_vec("to jest przykładowy tekst", n_grams=1))

  def test_borg(self):
    self.assertItemsEqual(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
        Borg().get_n_grams_list(1))


if __name__ == '__main__':
  unittest.main()

