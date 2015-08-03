# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys
import re
from stemming.porter2 import stem

class Borg:
  __shared_state = {}

  def __init__(self):
    self.__dict__ = self.__shared_state

  def get_n_grams_list(self, n):
    if n not in self.__dict__:
      Borg._Borg__shared_state[n] = initialize_n_grams_list(n)
      self.__dict__ = self.__shared_state
    return self.__dict__[n]

def initialize_n_grams_list(n):
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  n_grams_table = []
  if n == 1:
    for i in alphabet:
      n_grams_table.append(i)
    return n_grams_table
  else:
    n_grams_table = initialize_n_grams_list(n-1)
    n_grams_table2 = []
    for i in n_grams_table:
      for j in alphabet:
        n_grams_table2.append(i+j)
    return n_grams_table2

def clean(string):
  return re.sub("[^a-z\s]", "", string)

def get_n_grams_from_string(string, n_grams=3):
  n_grams_list = []
  for i in xrange(len(string)-n_grams+1):
    n_grams_list.append(string[i:i+n_grams])
  return n_grams_list

def count_n_grams(data, n_grams=3):
  n_grams_map = {}
  for word in data:
    for gram in get_n_grams_from_string(word, n_grams):
      if gram in n_grams_map:
        n_grams_map[gram] += 1.
      else:
        n_grams_map[gram] = 1.
  return n_grams_map

def get_n_grams_vec(data, n_grams=3, popular_dictionary=None):
  stat_list = []
  data = clean(data.lower()).split()
  data = map(stem, data)
  if popular_dictionary is not None:
    data = filter(lambda x: x not in popular_dictionary, data)
  stat_map = count_n_grams(data, n_grams)
  for key in Borg().get_n_grams_list(n_grams):
    if key not in stat_map:
      stat_list.append(0.)
    else:
      stat_list.append(stat_map[key])
  return stat_list

