import pandas as pd
import pymongo
import unidecode
import re 
import string
import nltk
import sys
import tensorflow_datasets as tfds
import tensorflow as tf
import os
from pathlib import Path
import tarfile
import gdown
from symspellpy import SymSpell, Verbosity

def get_dataframe_from_mongo(mongo_conn, collection):
    products_df = mongo_conn.db[collection].find({}).sort('created', pymongo.DESCENDING)
    
    return pd.DataFrame(products_df[0]['df']) if products_df else ''

def get_cleaned_predictor(sym_spell, description, product_name):
    description = list(map(get_description_and_name, description))
    product_name = list(map(get_description_and_name, product_name))

    X = join_all_predictors(description, product_name)

    X = correct_word_spelling(sym_spell, X)
    return X

def get_description_and_name(data):    
    stop_words = nltk.corpus.stopwords.words('portuguese')

    data = unidecode.unidecode(data[0]).lower()
    data = re.sub(r'['+string.punctuation+']', '', data)
    data = [word for word in data.split() if word not in stop_words]
    
    return ' '.join(data)   

def join_all_predictors(description, product_name):
    count = 0
    X = []

    for name in product_name:
        X.append(name + ' ' + description[count])
        count += 1

    return X

def preprocessing_fn(X, token_path):
    X, tokenizer = tokenize_data(X, token_path)
    X = padding_matrix(X)

    print('Preprocessing_fn finished')
    sys.stdout.flush()
    return X, tokenizer

def tokenize_data(data, token_path):
    tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(
        data, target_vocab_size=2**14)

    tokenizer.save_to_file(token_path)
    data = [tokenizer.encode(sentence) for sentence in data]

    return data, tokenizer

def padding_matrix(data):
    max_sentence_len = max([len(sentence) for sentence in data])
    data = tf.keras.preprocessing.sequence.pad_sequences(data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=max_sentence_len)

    return data

def read_file(file_name, content=''):
    if content:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name), 'w') as _file:
            _file.write(str(content))
            _file.close()
    else:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
            return _file.read()

def get_model_files_by_version(model_name, model_version):
    splitted_name = model_name.split('/')
    bucket = 'category-model' if 'category_model' in splitted_name else 'food-model'

    url = 'https://{}.s3.amazonaws.com/{}'.format(bucket, model_version + '.tar.gz')

    if 'category_model' in splitted_name and model_version not in os.listdir(model_name):
        download_model(url, model_name + model_version + '.tar.gz')

    elif 'food_model' in splitted_name and model_version not in os.listdir(model_name):
        download_model(url, model_name + model_version + '.tar.gz')

def download_model(url, output):
    gdown.download(url, output, quiet=False) 

    tar = tarfile.open(output)
    tar.extractall('/'.join(output.split('/')[0:-1]))
    tar.close()
    os.remove(output)

def instantiate_spelling_corrector():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    sym_spell.load_dictionary('./src/utils/datasets/dictionary.txt', term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary('./src/utils/datasets/word_bigram.txt', 0, 2)

    return sym_spell

def correct_word_spelling(sym_spell, corpus):
    final_corpus = []
    print('Correcting word spelling')
    for phrase in corpus:
        new_phrase = []
        for input_term in phrase.split():
            suggestion = sym_spell.lookup(input_term, Verbosity.TOP, 
                                    max_edit_distance=2)
        
            if len(suggestion) > 0:
                new_phrase.append(suggestion[0].term)               

        final_corpus.append(' '.join(new_phrase))

    return final_corpus
