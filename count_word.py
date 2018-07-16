# -*- coding: utf-8 -*-
# Count Word
# Tianqi Wang (tianqi.wang@sjtu.edu.cn)

from __future__ import division
from nltk import *
from nltk.corpus import PlaintextCorpusReader
from string import punctuation
from decimal import Decimal
import nltk
#import xlsxwriter
import os
import shutil
import codecs
import pyhtgen
import utils

# tokenize and normalize text
def token_norm(text):
    text_word = word_tokenize(text)
    text_remove_punct = [word.lower() for word in text_word
                         if word not in punctuation]
    text_remove_digit = [word for word in text_remove_punct
                         if not word.isdigit()]
    return text_remove_digit

# upload corpus
def upload_corpus(root):
    norm_text = []
    text_len = []
    corpora = PlaintextCorpusReader(root, '.*')
    all_text = corpora.fileids()
    for i in range(len(all_text)):
        text_raw = corpora.raw(all_text[i])
        token = token_norm(text_raw)
        norm_text = norm_text + [token]
        text_len = text_len + [len(token)]
    return all_text, norm_text, text_len

# count word
def count_word(text, word):
    count_list = []
    word_list = word
    for i in range(len(text)):
        fdist = FreqDist(text[i])
        count = []
        for j in range(len(word_list)):
            count = count + [fdist[word_list[j]]]
        count_list = count_list + [count]
    return count_list

# calculate percentage
def percentage(freq_list, total_word):
    percent_list = []
    for i in range(len(freq_list)):
        percent = []
        for j in range(len(freq_list[i])):
            percent = percent + [round(((freq_list[i][j]/total_word[i]) * 100), 2)]
        percent_list = percent_list + [percent]
    return percent_list

# data out
def data_combine(file_name, freq_list, percent_list):
    data = []
    for i in range(len(freq_list)):
        data_pair = []
        data_pair = data_pair + [file_name[i]]
        for j in range(len(freq_list[i])):
            data_pair = data_pair + [freq_list[i][j], percent_list[i][j]]
        data = data + [data_pair]
    return data

def header_index_generate():
    # alphabet
    alphabet = [chr(i) for i in range(97,123)]
    header_index = []
    for i in range(len(alphabet)):
        header_index = header_index + [alphabet[i].upper() + '1']
    return header_index

def data_output(name, data, word):
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()

    # format
    bold_black = workbook.add_format({'bold': 1})
    bold_red = workbook.add_format({'bold': 1, 'font_color': 'red'})
    worksheet.set_column('A:A', 15)

    # data headers
    index_excerpt = header_index_generate()[0:len(data[0])]
    worksheet.write(index_excerpt[0], 'Corpus', bold_black)
    for i in range(len(word)):
        worksheet.write(index_excerpt[2*i+1], word[i], bold_red)
        worksheet.write(index_excerpt[2*i+2], 'Freq (%)', bold_black)

    # start from the first cell below the headers
    for i in range(len(data)):
        for j in range(len(index_excerpt)):
            worksheet.write(i+1, j, data[i][j])

    workbook.close()
    print 'Complete'

def html_output(data, word):
    count = []
    freq = []
    for i in range(1, len(data[0])):
        if i % 2 != 0:
            count.append(str(data[0][i]))
        else:
            freq.append(str(data[0][i]))

    rows = []
    for i in range(len(word)):
        rows.append([word[i], count[i], freq[i]])

    return rows

def main(text, words):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('tmp/count_word'):
        os.mkdir('tmp/count_word')

    dir_name = utils.rand_dir_name()
    while os.path.exists('tmp/count_word/' + dir_name):
        dir_name = utils.rand_dir_name()

    dir_name = 'tmp/count_word/' + dir_name
    os.mkdir(dir_name)

    with codecs.open(dir_name + '/text.txt', 'w', encoding='utf8') as f:
        f.write(text)

    corpusRoot = dir_name
    wordToCount = words.split(',')
    fileName, allTextNorm, wordTotal = upload_corpus(corpusRoot)
    wordFreq = count_word(allTextNorm, wordToCount)
    wordPercent = percentage(wordFreq, wordTotal)
    dataCombine = data_combine(fileName, wordFreq, wordPercent)
    htmlOutput = html_output(dataCombine, wordToCount)

    shutil.rmtree(dir_name)

    header_row = ['Word', 'Count', 'Frequency']
    htmlcode = pyhtgen.table(htmlOutput, header_row=header_row)

    return htmlcode

if __name__ == '__main__':
    print main('i can should test this text file.', 'can,could,may,might,must,will,would,shall,should')
    #corpusRoot = '/Users/apple/Desktop/IFRS_corpus'
    #wordToCount = ['can', 'could', 'may', 'might', 'must', 'will', 'would', 'shall', 'should']
    #outputFile = 'result.xlsx'
    #fileName, allTextNorm, wordTotal = upload_corpus(corpusRoot)
    #wordFreq = count_word(allTextNorm, wordToCount)
    #wordPercent = percentage(wordFreq, wordTotal)
    #dataCombine = data_combine(fileName, wordFreq, wordPercent)
    #dataOutput = data_output(outputFile, dataCombine, wordToCount)
