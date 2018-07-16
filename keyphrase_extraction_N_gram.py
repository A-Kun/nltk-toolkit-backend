# -*- coding: utf-8 -*-
# Key Phrase Extraction
# Tianqi Wang (tianqi.wang@sjtu.edu.cn)

from __future__ import division
from nltk import *
from nltk.corpus import PlaintextCorpusReader
from nltk import sent_tokenize
from nltk.tag import pos_tag, map_tag
#from tabulate import tabulate
import nltk
import string
import math
#import xlsxwriter
import shutil
import codecs
import utils

# text normalization - replace '\r' and '\n'
def replace_newLine(text):
    if '\n' in text:
        text = text.replace('\n', '')
    else:
        text = text
    if '\r' in text:
        text = text.replace('\r', '. ')
        if '..' in text:
            text = text.replace('..', '.')
        else:
            text = text
    else:
        text = text
    return text

# upload corpus
def upload_corpus(root, name):
    corpora = PlaintextCorpusReader(root, [name])
    corpus_raw = corpora.raw(name)
    # if unicode
    # may have problems
    corpus_string = corpus_raw.encode('unicode-escape').decode('string_escape')
    corpus_text_norm = replace_newLine(corpus_string)
    return corpus_text_norm

# tokenize the text into sentences and words
def text_tokenize(text):
    text_unicode = text.encode('string_escape').decode('unicode-escape')
    text_sent = sent_tokenize(text_unicode)
    text_word = [word_tokenize(sent) for sent in text_sent]
    return text_sent, text_word

# part of speech tagging (POS tagging)
# ======================================================================
# Simplified Tags:
# VERB - verbs (all tenses and modes)
# NOUN - nouns (common and proper)
# PRON - pronouns
# ADJ  - adjectives
# ADV  - adverbs
# ADP  - adpositions (prepositions and postpositions)
# CONJ - conjunctions
# DET  - determiners
# NUM  - cardinal numbers
# PRT  - particles or other function words
# X    - other: foreign words, typos, abbreviations
# .    - punctuation
# ======================================================================

# pos tagging
def posTag(text):
    posTagged = [pos_tag(word) for word in text]
    simplifiedTags = [[(word, map_tag('en-ptb', 'universal', tag)) for
                      word, tag in sent] for sent in posTagged]
    return simplifiedTags

# n-gram extraction
def n_gram(text, n):
    n_gram_list = []
    for i in range(len(text)):
        for j in range(len(text[i])-n+1):
            n_gram_list = n_gram_list + [text[i][j:(j+n)]]
    return n_gram_list

# valid n-gram extraction
# ======================================================================
# Valid threshold:
#   Valid: at least 1 NOUN
#   Invalid: cannot be VERB, PRON, ADV, ADP, CONJ, DET, NUM, Punctuation
# ======================================================================

# get valid n-gram
def get_valid_list(text):
    valid_index_list = []
    invalid_tag_list = ['VERB', 'PRON', 'ADV', 'ADP', 'CONJ', 'DET', 'NUM', 'PRT', 'X', '.']
    tag_list = []
    for i in range(len(text)):
        n_gram_tag = []
        for j in range(len(text[i])):
            n_gram_tag = n_gram_tag + [text[i][j][1]]
        tag_list = tag_list + [n_gram_tag]

    for i in range(len(tag_list)):
        if 'NOUN' in tag_list[i]:
            invalid_count = 0
            for j in range(len(tag_list[i])):
                if tag_list[i][j] in invalid_tag_list:
                    invalid_count = invalid_count + 1
            if invalid_count == 0:
                valid_index_list = valid_index_list + [i]
    return valid_index_list

def valid_n_gram(text):
    valid_index = get_valid_list(text)
    valid_n_gram = []
    for i in range(len(valid_index)):
        valid_n_gram = valid_n_gram + [text[int(valid_index[i])]]
    return valid_n_gram

# text normalization
# text norm for corpus - original word
def text_norm(text):
    text_norm_list = []
    for i in range(len(text)):
        n_gram_norm = ''
        for j in range(len(text[i])):
            if j < len(text[i]) - 1:
                n_gram_norm = n_gram_norm + text[i][j][0] + ' '
            else:
                n_gram_norm = n_gram_norm + text[i][j][0]
        text_norm_list = text_norm_list + [n_gram_norm]
    return text_norm_list

# text norm for corpus - lowercase word
def text_norm_lower(text):
    text_norm_list = []
    for i in range(len(text)):
        n_gram_norm = ''
        for j in range(len(text[i])):
            if j < len(text[i]) - 1:
                n_gram_norm = n_gram_norm + text[i][j][0].lower() + ' '
            else:
                n_gram_norm = n_gram_norm + text[i][j][0].lower()
        text_norm_list = text_norm_list + [n_gram_norm]
    return text_norm_list

# text norm for ref corpus
def text_Norm(n_gram_list):
    text_norm = [[word.lower() for word in n_gram] for n_gram in n_gram_list] # may delete is.alpha()
    return text_norm

# get n-gram without punctuation and numbers
def get_n_gram_index_without_punct_and_num(text):
    valid_index_list = []
    invalid_tag_list = ['NUM', '.']
    tag_list = []
    for i in range(len(text)):
        n_gram_tag = []
        for j in range(len(text[i])):
            n_gram_tag = n_gram_tag + [text[i][j][1]]
        tag_list = tag_list + [n_gram_tag]

    for i in range(len(tag_list)):
        invalid_count = 0
        for j in range(len(tag_list[i])):
            if tag_list[i][j] in invalid_tag_list:
                invalid_count = invalid_count + 1
        if invalid_count == 0:
            valid_index_list = valid_index_list + [i]
    return valid_index_list

def n_gram_without_punct_and_num(text):
    valid_index = get_n_gram_index_without_punct_and_num(text)
    valid_n_gram = []
    for i in range(len(valid_index)):
        valid_n_gram = valid_n_gram + [text[int(valid_index[i])]]
    return valid_n_gram

# TF-IDF
# get n-gram frequency
def n_gram_freq(text):
    n_gram_freq = FreqDist(text)
    return n_gram_freq.keys(), n_gram_freq

# TF calculation
# n_gram_norm: n-gram without punctuation and numbers
def tf(n_gram, n_gram_freq, n_gram_norm):
    tf_list = []
    total_n_gram = len(n_gram_norm)
    for i in range(len(n_gram)):
        tf = n_gram_freq[n_gram[i]] / total_n_gram
        tf_list = tf_list + [tf]
    return tf_list

# IDF
# get all text
def get_all_text(file_path):
    all_file = PlaintextCorpusReader(file_path, '.*')
    all_file_list = all_file.fileids()
    all_text_list = []
    for i in range(len(all_file_list)):
        text = all_file.raw(all_file_list[i])
        # text normalization - replace '\r' and '\n'
        text_string_norm = replace_newLine(text)
        all_text_list = all_text_list + [text_string_norm]
    return all_text_list

def get_all_n_gram(file_path, n):
    all_text_list = get_all_text(file_path)
    # text tokenization - sents and words
    text_wordList = []
    for i in range(len(all_text_list)):
        text_sent = sent_tokenize(all_text_list[i])
        text_word = [word_tokenize(sent) for sent in text_sent]
        text_wordList = text_wordList + [text_word]
    # n-gram extraction
    all_n_gram_list = []
    for i in range(len(all_text_list)): # len(all_text_list) = len(text_wordList)
        n_gram_list = n_gram(text_wordList[i], n)
        all_n_gram_list = all_n_gram_list + [n_gram_list]
    # n-gram normalization
    all_n_gram_norm = []
    for i in range(len(all_text_list)): # len(all_text_list) = len(all_n_gram_list)
        n_gram_norm = text_Norm(all_n_gram_list[i])
        all_n_gram_norm = all_n_gram_norm + [n_gram_norm]
    # create n-gram string (convert n-gram list to n-gram string)
    all_n_gram_norm_str = []
    for i in range(len(all_n_gram_norm)):
        n_gram_norm_str = []
        for j in range(len(all_n_gram_norm[i])):
            n_gram_str = ''
            for m in range(len(all_n_gram_norm[i][j])):
                if m < len(all_n_gram_norm[i][j]) - 1:
                    n_gram_str = n_gram_str + all_n_gram_norm[i][j][m].lower() + ' '
                else:
                    n_gram_str = n_gram_str + all_n_gram_norm[i][j][m].lower()
            n_gram_norm_str = n_gram_norm_str + [n_gram_str]
        all_n_gram_norm_str = all_n_gram_norm_str + [n_gram_norm_str]
    return all_n_gram_norm_str

# IDF calculation
def idf(file_path, n, n_gram):
    idf_list = []
    all_n_gram = get_all_n_gram(file_path, n)
    count_sum = []
    for i in range(len(n_gram)):
        occur_count = 0
        for j in range(len(all_n_gram)):
            if n_gram[i] in all_n_gram[j]:
                occur_count = occur_count + 1
            else:
                occur_count = occur_count + 0
        count_sum = count_sum + [occur_count]
    for i in range(len(count_sum)):
        idf = math.log(len(all_n_gram)/(count_sum[i] + 1))
        idf_list = idf_list + [idf]
    return idf_list

# TF-IDF calculation
# n_gram_norm: n-gram without punctuation and numbers
def tf_idf(file_path, n, n_gram, n_gram_freq, n_gram_norm):
    tf_idf_list = []
    tf_value = tf(n_gram, n_gram_freq, n_gram_norm)
    idf_value = idf(file_path, n, n_gram)
    for i in range(len(tf_value)):
        tf_idf_value = tf_value[i]*idf_value[i]
        tf_idf_list = tf_idf_list + [tf_idf_value]
    return tf_idf_list

# get n-gram and corresponding TF-IDF
# get n-gram original form
# valid_n_gram_norm_lower: text_norm_lower
# valid_n_gram_norm: text_norm
def n_gram_original(n_gram, valid_n_gram_norm_lower, valid_n_gram_norm):
    valid_n_gram_index = []
    valid_n_gram_original = []
    for i in range(len(n_gram)):
        index = valid_n_gram_norm_lower.index(n_gram[i])
        valid_n_gram_index = valid_n_gram_index + [index]
    for i in range(len(valid_n_gram_index)): # len(valid_n_gram_index) = len(n_gram)
        n_gram_original = valid_n_gram_norm[valid_n_gram_index[i]]
        valid_n_gram_original = valid_n_gram_original + [n_gram_original]
    return valid_n_gram_original

# parameters: tf_idf, n_gram_original
def n_gram_tfidf(file_path, n, n_gram, n_gram_freq, n_gram_norm,
                 valid_n_gram_norm_lower, valid_n_gram_norm):
    n_gram_tfidf_list = []
    n_gram = n_gram_original(n_gram, valid_n_gram_norm_lower, valid_n_gram_norm)
    tfidf = tf_idf(file_path, n, n_gram, n_gram_freq, n_gram_norm)
    for i in range(len(n_gram)):
        pair = [n_gram[i], tfidf[i]]
        n_gram_tfidf_list = n_gram_tfidf_list + [pair]
    return n_gram_tfidf_list

# data output
# output result into xlsx or txt file
def data_output_xlsx(name, data):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    # start from the first cell. Rows and columns are zero indexed
    row = 0
    col = 0
    for n_gram, tfidf in (data):
        worksheet.write(row, col, n_gram)
        worksheet.write(row, col+1, tfidf)
        row = row + 1
    workbook.close()

def data_output_txt(name, data):
    f = open(name, 'a')
    for i in range(len(data)):
        f.write(data[i][0])
        f.write('\n')
    f.close()

def data_output(data):
    result = ''
    for i in range(len(data)):
        result += data[i][0]
        result += '\n'
    return result

def main(text):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('tmp/keyphrase_extraction_N_gram'):
        os.mkdir('tmp/keyphrase_extraction_N_gram')

    dir_name = utils.rand_dir_name()
    while os.path.exists('tmp/keyphrase_extraction_N_gram/' + dir_name):
        dir_name = utils.rand_dir_name()

    dir_name = 'tmp/keyphrase_extraction_N_gram/' + dir_name
    os.mkdir(dir_name)

    with codecs.open(dir_name + '/text.txt', 'w', encoding='utf8') as f:
        f.write(text)

    corpus_root = dir_name
    file_name = 'text.txt'
    N = 4
    filetype = 'txt'
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_posTagged = posTag(corpus_word)
    corpus_N_gram = n_gram(corpus_posTagged, N)
    valid_N_gram = valid_n_gram(corpus_N_gram)
    valid_N_gram_norm = text_norm(valid_N_gram)
    valid_N_gram_norm_lower = text_norm_lower(valid_N_gram)
    N_gram_without_punct_and_num = n_gram_without_punct_and_num(corpus_N_gram)
    N_gram, N_gram_freq = n_gram_freq(valid_N_gram_norm_lower)
    N_gram_tfidf = n_gram_tfidf(corpus_root, N, N_gram, N_gram_freq,
                                N_gram_without_punct_and_num,
                                valid_N_gram_norm_lower, valid_N_gram_norm)
    # sort and output data
    sorted_data = sorted(N_gram_tfidf, key = lambda result: result[1], reverse = True)
    shutil.rmtree(dir_name)
    return data_output(sorted_data)

if __name__ == '__main__':
    corpus_root = '/Users/apple/Desktop/IFRS_corpus'
    corpus_root = 'tmp/123'
    file_name = 'ifrs_01.txt'
    N = 4
    filetype = 'txt'
    filename = 'n_gram_result.txt'
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_posTagged = posTag(corpus_word)
    corpus_N_gram = n_gram(corpus_posTagged, N)
    valid_N_gram = valid_n_gram(corpus_N_gram)
    valid_N_gram_norm = text_norm(valid_N_gram)
    valid_N_gram_norm_lower = text_norm_lower(valid_N_gram)
    N_gram_without_punct_and_num = n_gram_without_punct_and_num(corpus_N_gram)
    N_gram, N_gram_freq = n_gram_freq(valid_N_gram_norm_lower)
    N_gram_tfidf = n_gram_tfidf(corpus_root, N, N_gram, N_gram_freq,
                                N_gram_without_punct_and_num,
                                valid_N_gram_norm_lower, valid_N_gram_norm)
    # sort and output data
    sorted_data = sorted(N_gram_tfidf, key = lambda result: result[1], reverse = True)
    # print tabulate(sorted_data, headers = ['N-gram', 'TF-IDF'])
    # output the data in xlsx file
    #if filetype == 'xlsx':
        #data_output_xlsx(filename, sorted_data)
    #if filetype == 'txt':
        #data_output_txt(filename, sorted_data)
    print data_output(sorted_data)

