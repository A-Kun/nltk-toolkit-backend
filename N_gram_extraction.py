# -*- coding: utf-8 -*-
# Key Phrase Extraction
# Tianqi Wang (tianqi.wang@sjtu.edu.cn)

from nltk import *
from nltk.corpus import PlaintextCorpusReader
from nltk import sent_tokenize
from nltk.tag import pos_tag, map_tag
from nltk.stem import WordNetLemmatizer
import nltk
import string
import math
#import xlsxwriter
import shutil
import codecs
import utils

# upload stopword list
def upload_stopword(stopword_file):
    f = open(stopword_file, 'r')
    f_read = f.read()
    f.close()
    stopword_list = list(f_read.split(', '))
    return stopword_list

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

# remove n_gram with stopword
# n_gram: valid_n_gram in valid_n_gram()
# stopword: upload stopword
def remove_stopword(n_gram, stopword):
    n_gram_list = n_gram
    stopword_list = stopword
    n_gram_without_stopword_index = []
    n_gram_filtered = []
    for i in range(len(n_gram_list)):
        invalid_count = 0
        for j in range(len(n_gram_list[i])):
            if n_gram_list[i][j][0].lower() in stopword_list:
                invalid_count = invalid_count + 1
            else:
                invalid_count = invalid_count + 0
        if invalid_count == 0:
            n_gram_without_stopword_index = n_gram_without_stopword_index + [i]
    for i in range(len(n_gram_without_stopword_index)):
        n_gram_filtered = n_gram_filtered + [n_gram_list[n_gram_without_stopword_index[i]]]
    return n_gram_filtered

# lemmatize nouns: lemmatize the LAST noun in the n-gram
# change 'tuple' to 'list' as 'tuple' object does not support item assignment
def tuple_to_list(n_gram):
    word_tag_list = []
    for i in range(len(n_gram)):
        n_gram_pair_list = []
        for j in range(len(n_gram[i])):
            pair_list = []
            for item in range(len(n_gram[i][j])):
                pair_list = pair_list + [n_gram[i][j][item]]
            n_gram_pair_list = n_gram_pair_list + [pair_list]
        word_tag_list = word_tag_list + [n_gram_pair_list]
    return word_tag_list

def lemmatize_noun(n_gram, n):
    n_gram_list = tuple_to_list(n_gram)
    wnl = WordNetLemmatizer()
    for i in range(len(n_gram_list)):
        if n_gram_list[i][n-1][1] == 'NOUN':
            n_gram_list[i][n-1][0] = wnl.lemmatize(n_gram_list[i][n-1][0].lower(), 'n')
    return n_gram_list

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

# get n-gram frequency
def n_gram_freq(text):
    n_gram_freq = FreqDist(text)
    return n_gram_freq.items()

def seperate_n_gram_and_freq(text):
    n_gram_freq_list = n_gram_freq(text)
    n_gram_list = []
    freq_list = []
    for i in range(len(n_gram_freq_list)):
        n_gram_list = n_gram_list + [n_gram_freq_list[i][0]]
        freq_list = freq_list + [n_gram_freq_list[i][1]]
    return n_gram_list, freq_list

# get the index of the items in target list
# source_list: n_gram_list in seperate_n_gram_and_freq()
# target_list: text_norm_list in text_norm_lower()
def get_index(source_list, target_list):
    index_list = []
    for i in range(len(source_list)):
        index_list = index_list + [target_list.index(source_list[i])]
    return index_list

# get the original form of n_gram and its corresponding freq
# index_list: index_list in get_index()
# original_list: text_norm_list in text_norm()
# freq_list: freq_list in seperate_n_gram_and_freq()
def original_n_gram_freq(index_list, original_list, freq_list):
    n_gram_freq_pairs = []
    total_n_gram_freq_pairs = []
    for i in range(len(index_list)):
        n_gram = original_list[index_list[i]]
        freq = freq_list[i]
        n_gram_freq_pairs = [n_gram, freq]
        total_n_gram_freq_pairs = total_n_gram_freq_pairs + [n_gram_freq_pairs]
    return total_n_gram_freq_pairs

# sort data
def sort_data(data):
    sorted_data = sorted(data, key = lambda result: result[1], reverse = True)
    return sorted_data

# frequency filter
def freq_filter(data, threshold):
    data_filtered = []
    for i in range(len(data)):
        if data[i][1] >= threshold:
            data_filtered = data_filtered + [data[i]]
    return data_filtered

# data output
# output result into xlsx or txt file
def data_output_xlsx(name, data):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    # start from the first cell. Rows and columns are zero indexed
    row = 0
    col = 0
    for n_gram, freq in (data):
        worksheet.write(row, col, n_gram)
        worksheet.write(row, col+1, freq)
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
    if not os.path.exists('tmp/N_gram_extraction'):
        os.mkdir('tmp/N_gram_extraction')

    dir_name = utils.rand_dir_name()
    while os.path.exists('tmp/N_gram_extraction/' + dir_name):
        dir_name = utils.rand_dir_name()

    dir_name = 'tmp/N_gram_extraction/' + dir_name
    os.mkdir(dir_name)

    with codecs.open(dir_name + '/text.txt', 'w', encoding='utf8') as f:
        f.write(text)

    corpus_root = dir_name
    file_name = 'text.txt'
    N = 3
    Min_freq = 1
    #filetype = 'xlsx'
    #filename = 'n_gram_result.xlsx'
    stopWordFile = 'stopword_list.txt'
    stopWord = upload_stopword(stopWordFile)
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_posTagged = posTag(corpus_word)
    corpus_N_gram = n_gram(corpus_posTagged, N)
    valid_N_gram = valid_n_gram(corpus_N_gram)
    valid_N_gram_filtered = remove_stopword(valid_N_gram, stopWord)
    valid_N_gram_lemmatized = lemmatize_noun(valid_N_gram_filtered, N)
    valid_N_gram_norm = text_norm(valid_N_gram_lemmatized)
    valid_N_gram_norm_lower = text_norm_lower(valid_N_gram_lemmatized)
    N_gram_list, Freq_list = seperate_n_gram_and_freq(valid_N_gram_norm_lower)
    N_gram_index = get_index(N_gram_list, valid_N_gram_norm_lower)
    N_gram_original_and_freq = original_n_gram_freq(N_gram_index,
                                                    valid_N_gram_norm,
                                                    Freq_list)
    N_gram_sorted = sort_data(N_gram_original_and_freq)
    N_gram_freq_filtered = freq_filter(N_gram_sorted, Min_freq)
    shutil.rmtree(dir_name)
    return data_output(N_gram_freq_filtered)

if __name__ == '__main__':
    corpus_root = '/Users/apple/Desktop'
    file_name = 'Chinese copyright law.txt'
    N = 3
    Min_freq = 1
    filetype = 'xlsx'
    filename = 'n_gram_result.xlsx'
    stopWordFile = '/Users/apple/Desktop/IFRS_corpus/stopword_list.txt'
    stopWord = upload_stopword(stopWordFile)
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_posTagged = posTag(corpus_word)
    corpus_N_gram = n_gram(corpus_posTagged, N)
    valid_N_gram = valid_n_gram(corpus_N_gram)
    valid_N_gram_filtered = remove_stopword(valid_N_gram, stopWord)
    valid_N_gram_lemmatized = lemmatize_noun(valid_N_gram_filtered, N)
    valid_N_gram_norm = text_norm(valid_N_gram_lemmatized)
    valid_N_gram_norm_lower = text_norm_lower(valid_N_gram_lemmatized)
    N_gram_list, Freq_list = seperate_n_gram_and_freq(valid_N_gram_norm_lower)
    N_gram_index = get_index(N_gram_list, valid_N_gram_norm_lower)
    N_gram_original_and_freq = original_n_gram_freq(N_gram_index,
                                                    valid_N_gram_norm,
                                                    Freq_list)
    N_gram_sorted = sort_data(N_gram_original_and_freq)
    N_gram_freq_filtered = freq_filter(N_gram_sorted, Min_freq)

    # output the data in xlsx / txt file
    if filetype == 'xlsx':
        data_output_xlsx(filename, N_gram_freq_filtered)
    if filetype == 'txt':
        data_output_txt(filename, N_gram_freq_filtered)
    print 'Data output complete'
