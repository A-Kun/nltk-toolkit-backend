# -*- coding: utf-8 -*-
# Andrew Wang (me@andrewwang.ca)

from flask import Flask
from flask import request
from flask_cors import CORS
import os

import dic
import count_word
import keyphrase_extraction_N_gram
import N_gram_extraction
import search_sent

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/count_word/', methods=['POST'])
def process_count_word():
    text = request.form['text']
    words = request.form['words']
    if not text or not words:
        raise Exception
    return count_word.main(text, words)

@app.route('/dic/', methods=['POST'])
def process_dic():
    word = request.form['word']
    if not word:
        raise Exception
    return dic.main(word)

@app.route('/keyphrase_extraction_N_gram/', methods=['POST'])
def process_keyphrase_extraction_N_gram():
    text = request.form['text']
    if not text:
        raise Exception
    return keyphrase_extraction_N_gram.main(text)

@app.route('/N_gram_extraction/', methods=['POST'])
def process_N_gram_extraction():
    text = request.form['text']
    if not text:
        raise Exception
    return N_gram_extraction.main(text)

@app.route('/search_sent/', methods=['POST'])
def process_search_sent():
    text = request.form['text']
    key_phrase = request.form['key_phrase']
    if not text:
        raise Exception
    return search_sent.main(text, key_phrase)

if __name__ == "__main__":
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')
    nltk.download('wordnet')
    app.run(port=int(os.environ.get('PORT', 5000)))
