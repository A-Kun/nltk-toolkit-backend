# -*- coding: utf-8 -*-
# Search sentences containing key phrases extracted
# Tianqi Wang (tianqi.wang@sjtu.edu.cn)

from nltk import *
from nltk.corpus import PlaintextCorpusReader
from nltk import sent_tokenize
import nltk
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
    corpus_string = corpus_raw.encode('unicode-escape').decode('string_escape')
    corpus_text_norm = replace_newLine(corpus_string)
    return corpus_text_norm

# tokenize the text into sentences and words
def text_tokenize(text):
    text_unicode = text.encode('string_escape').decode('unicode-escape')
    text_sent = sent_tokenize(text_unicode)
    text_word = [word_tokenize(sent) for sent in text_sent]
    return text_sent, text_word

# convert all characters into lowercase
def text_lower(text):
    text_lowercase = [[word.lower() for word in sent] for sent in text]
    return text_lowercase

# n_gram extraction
def n_gram(text, n):
    n_gram_sent = []
    for i in range(len(text)):
        n_gram_list = []
        for j in range(len(text[i])-n+1):
            n_gram_list = n_gram_list + [text[i][j:(j+n)]]
        n_gram_sent = n_gram_sent + [n_gram_list]
    return n_gram_sent

# search sentences
def search_sent(keyPhrase, text):
    sent_index_list = []
    keyPhrase_lower = keyPhrase.lower()
    keyPhrase_tokenize = word_tokenize(keyPhrase_lower)
    text_n_gram = n_gram(text, len(keyPhrase_tokenize))
    for i in range(len(text_n_gram)):
        if keyPhrase_tokenize in text_n_gram[i]:
            sent_index_list = sent_index_list + [i]
    return sent_index_list

# get sentences containing key phrases extracted
def get_sent(sent, index):
    sent_list = []
    for i in range(len(index)):
        sent_list = sent_list + [str(sent[index[i]])[:-1]]
    return sent_list

# data output
def data_output(name, keyPhrase, data):
    f = open(name, 'w')
    f.write('==================================================================================')
    f.write('\n')
    f.write('Search result:' + ' ' + str(len(data)) + ' ' + 'sentences contain the phrase' + ' ' + keyPhrase.upper())
    f.write('\n')
    f.write('==================================================================================')
    f.write('\n')
    for i in range(len(data)):
        f.write('[' + str(i+1) + ']' + ' ' + data[i])
        f.write('\n')
        f.write('----------------------------------------------------------------------------------')
        f.write('\n')
    f.close()

def text_output(keyPhrase, data):
    result = ''
    result += ('==================================================================================')
    result += ('\n')
    result += ('Search result:' + ' ' + str(len(data)) + ' ' + 'sentences contain the phrase' + ' ' + keyPhrase.upper())
    result += ('\n')
    result += ('==================================================================================')
    result += ('\n')
    for i in range(len(data)):
        result += ('[' + str(i+1) + ']' + ' ' + data[i])
        result += ('\n')
        result += ('----------------------------------------------------------------------------------')
        result += ('\n')
    return result

def main(text, key_phrase):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('tmp/search_sent'):
        os.mkdir('tmp/search_sent')

    dir_name = utils.rand_dir_name()
    while os.path.exists('tmp/search_sent/' + dir_name):
        dir_name = utils.rand_dir_name()

    dir_name = 'tmp/search_sent/' + dir_name
    os.mkdir(dir_name)

    with codecs.open(dir_name + '/text.txt', 'w', encoding='utf8') as f:
        f.write(text)

    corpus_root = dir_name
    file_name = 'text.txt'
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_lower = text_lower(corpus_word)
    search_result_index = search_sent(key_phrase, corpus_lower)
    search_result_sent = get_sent(corpus_sent, search_result_index)
    shutil.rmtree(dir_name)
    return text_output(key_phrase, search_result_sent)

if __name__ == '__main__':
    corpus_root = '/Users/apple/Desktop'
    file_name = 'Chinese copyright law.txt'
    result_name = 'search_result.txt'
    corpus_norm = upload_corpus(corpus_root, file_name)
    corpus_sent, corpus_word = text_tokenize(corpus_norm)
    corpus_lower = text_lower(corpus_word)
    # enter the keyphrase
    key_phrase = input("Enter the key phrase:")
    search_result_index = search_sent(key_phrase, corpus_lower)
    search_result_sent = get_sent(corpus_sent, search_result_index)
    # output the data in txt file
    data_output(result_name, key_phrase, search_result_sent)
    print 'Search complete'
