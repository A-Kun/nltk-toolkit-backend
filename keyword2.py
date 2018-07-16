# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wang Tianqi (tianqi.wang@sjtu.edu.cn)
# Key Word Extraction

# ===============================================================================
# WordSmith Tools (Scott, 1996):
# 1st Step: a word list is computed, containing all the different types in the
#           reference corpus and the frequencies of each
# 2nd Step: the same sort of word list is computed for the text whose key words
#           one wishes to find
# 3rd Step: each word in the individual word list is compared with the reference
#           corpus word list. If the percentage is similar, the item may be
#           ignored. Where there is a great disparity in frequency, it is
#           possible to identify an item as key. The actual calculation of
#           "keyness" is done using the chi-square statistics, but the important
#           point to grasp here is that the notion underlying it is one of
#           outstandingness.
#           Two thresholds to be set when computing key words:
#           1. chi-square cut-off point (min significance): 0.000001
#           2. minimum frequency requirement: 2 (i.e. any word which occurs only
#              once would be ignored)
# 4th Step: all potentially key items are ordered in terms of their relative
#           keyness after having been identified
# Output Format:
# Key Words | Frequency | Percentage | Frequency - Corpus | Percentage - Corpus
# ===============================================================================

from __future__ import division
from nltk.corpus import PlaintextCorpusReader
from nltk import *
import scipy
from scipy.stats import chisquare
import shutil
import codecs
import utils

def main(text):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('tmp/keyword_2'):
        os.mkdir('tmp/keyword_2')

    dir_name = utils.rand_dir_name()
    while os.path.exists('tmp/keyword_2/' + dir_name):
        dir_name = utils.rand_dir_name()

    dir_name = 'tmp/keyword_2/' + dir_name
    os.mkdir(dir_name)

    with codecs.open(dir_name + '/text.txt', 'w', encoding='utf8') as f:
        f.write(text)

    # Upload reference corpus
    #corpus_root = '/Users/apple/Desktop/Paper/corpora'
    corpus_root = dir_name

    corpora = PlaintextCorpusReader(corpus_root, '.*')
    corpora.fileids()

    reference_corpus = corpora.words(corpora.fileids()[:])
    reference_corpus_clean = [word.lower() for word in reference_corpus
                              if word.isalpha()]

    # Reference corpus - wordlist & word frequency
    reference_word_list_freq = FreqDist(reference_corpus_clean)
    reference_word_list = reference_word_list_freq.keys()

    # Upload the text to find key words
    text = corpora.words(corpora.fileids()[0])
    text_clean = [word.lower() for word in text if word.isalpha()]

    # Text - wordlist & word frequency
    word_list_freq = FreqDist(text_clean)
    word_list = word_list_freq.keys()

    # Key word extraction
    num_of_word_ref = len(reference_corpus_clean)
    num_of_word = len(text_clean)
    result_tuple = []

    for i in range(len(word_list)):
        if word_list[i] in reference_word_list_freq:
            if word_list_freq[word_list[i]] >= 2:    # threshold 2
                freq = word_list_freq[word_list[i]]
                other_word_freq = num_of_word - freq
                freq_ref = reference_word_list_freq[word_list[i]]
                other_word_freq_ref = num_of_word_ref - freq_ref
                obs = [freq, other_word_freq]
                exp = [freq_ref, other_word_freq_ref]
                chi2, p, ddof, expected = scipy.stats.chi2_contingency([obs, exp])
                print p
                if p < 0.000001:                     # threshold 1
                    result_tuple = result_tuple + [(round(chi2,3),
                                                    word_list[i].upper(),
                                                    freq,
                                                    '(%.1f%%)' % ((freq/num_of_word) * 100),
                                                    freq_ref,
                                                    '(%.6f%%)' % ((freq_ref/num_of_word_ref) * 100))]

    sorted_data = sorted(result_tuple, key = lambda result: result[0], reverse = True)

    shutil.rmtree(dir_name)

    print sorted_data
    #from tabulate import tabulate
    #print tabulate(sorted_data, headers = ['Keyness',
                                           #'Key Word',
                                           #'Freq-My',
                                           #'%-My',
                                           #'Freq-Ref',
                                           #'%-Ref'])
