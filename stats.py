# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys
from operator import itemgetter
from ngrams import get_n_grams_vec
from stemming.porter2 import stem
from sklearn.cluster import KMeans
from numpy.linalg import norm
import itertools


def normalize_vector(vector):
  max_value = norm(vector)
  return map(lambda x: x / max_value, vector)

def get_all_vectors(file_with_lists, dictionary_file=None):
  dictionary = []
  if dictionary_file is not None:
    dictionary = [line.strip() for line in open(dictionary_file)]

  with open(file_with_lists) as f:
    lines = f.readlines()
  labels = {}
  vector_matrix = []
  for i in xrange(len(lines)):
    labels[lines[i].strip()] = i
    vector_matrix.append( normalize_vector(get_n_grams_vec(lines[i])) )
  return labels, vector_matrix

def load_clusters(file_with_clusters, reversed_cluster=False):
  lines = [line.strip() for line in open(file_with_clusters) if line]
  clusters_set = {}
  iterator = 0
  for line in lines:
    if line != "" and line != "##########":
      if reversed_cluster:
        clusters_set[line] = iterator
      else:
        if iterator not in clusters_set:
          clusters_set[iterator] = [line]
        else:
          clusters_set[iterator].append(line)
    elif line == "##########":
      iterator += 1
  return clusters_set

def get_precision_recall(clusters_set, clustering_results):
  pairs = list(itertools.combinations(clusters_set.keys(), 2))
  true_positives = 0.
  false_positives = 0.
  false_negatives = 0.
  for pair in pairs:
    if pair[0] in clustering_results and pair[1] in clustering_results:
      if clusters_set[pair[0]] == clusters_set[pair[1]]:
        if clustering_results[pair[0]] == clustering_results[pair[1]]:
          true_positives += 1
        else:
          false_negatives += 1
      elif clustering_results[pair[0]] == clustering_results[pair[1]]:
        false_positives += 1

  precision = true_positives / (true_positives + false_positives)
  recall = true_positives / (true_positives + false_negatives)
  f1_score = 2*precision*recall / (precision+recall)

  return precision, recall, f1_score

def get_knn_result(labels, vector_matrix):
  km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, verbose=True)
  km.fit(vector_matrix)

  clustering_results = {}
  for label in labels:
    clustering_results[label] = km.labels_[labels[label]]

  return clustering_results


if __name__ == '__main__':
  if len(sys.argv) >= 3:
    file_with_lists = sys.argv[1]
    file_with_clusters = sys.argv[2]
    most_popular_words_dictionary = sys.argv[3] if len(sys.argv) == 4 else None

    clusters_set = load_clusters(file_with_clusters, reversed_cluster=True)

    with open(file_with_lists) as f:
      true_k = min(sum(1 for _ in f), 3356)
    labels, vector_matrix = get_all_vectors(file_with_lists, dictionary_file=most_popular_words_dictionary)

    print "got vectors"

    knn_results_set = get_knn_result(labels, vector_matrix)
    print "got clusters"
    print get_precision_recall(clusters_set, knn_results_set)

  else:
    print("python stats.py [list] [clusters] [dictionary - optional]")

