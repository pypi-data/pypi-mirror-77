import sys
import os
import os.path
from sys import argv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import tensorflow_datasets as tfds
import pickle
import shutil
import subprocess
import tarfile
import json
import seaborn as sns

from utils import utils
from database.db_mongo import MongoDatabase
from nkia.ml.deploy_model import DeployModel
from nkia.ml.cnn_nlp_model import CNN

class trainProductsModel(object):

    def __init__(self, model_to_train, show_confusion_matrix=False):
        self.model_to_train = model_to_train
        self.confusion_matrix = show_confusion_matrix
        self.new_model_path, self.last_model_path = self.create_saved_model_folder(model_to_train)
        self.train_model()

    def create_saved_model_folder(self, model_name):
        last_model_version = json.loads(utils.read_file(os.getcwd() + '/config.txt'))['version']
        new_model_version = self.get_new_model_version(last_model_version)

        model_path = os.path.join('./src/nkia/ml/saved_model/' + model_name + '/')
        
        if os.path.exists(model_path + new_model_version):
            shutil.rmtree(model_path + new_model_version)
        os.makedirs(model_path + new_model_version)

        versions_stored = os.listdir(model_path)
        
        if len(versions_stored) > 1:
            versions_stored.remove(new_model_version) 
            last_model_path = model_path + versions_stored[0]        
        else:
            utils.get_model_files_by_version(model_path, last_model_version)
            last_model_path = model_path + last_model_version        

        model_path = model_path + new_model_version
        return model_path, last_model_path

    def get_new_model_version(self, last_model_version):
        new_model_version = last_model_version.split('.')
        new_model_version.insert(1, str(int(new_model_version.pop(1)) + 1))
        return '.'.join(new_model_version)

    def train_model(self):
        dataframe, y = self.get_data()
        X = self.get_previsors_attrib(dataframe)

        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.2,
                                                            random_state=1,
                                                            stratify=y) 

        cnn = self.create_model_instance(y, self.tokenizer.vocab_size)
        self.loss_f = 'sparse_categorical_crossentropy' if self.model_to_train == 'category_model' else 'binary_crossentropy'
        cnn.compile(loss=self.loss_f, optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.new_model_path + '/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)
        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 1,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        self.evaluate_and_deploy_model(cnn, X_test, y_test, y)
        
        if self.confusion_matrix:
            self.predict_and_plot_matrix(cnn, X_test, y_test)

    def get_data(self):
        collection = 'food_df' if self.model_to_train == 'category_model' else 'not_food_df'
        self.open_mongo_connections()
        dataframe = utils.get_dataframe_from_mongo(self.mongo_conn, collection)
        self.close_mongo_connection()
        
        dataframe['description'].fillna('', inplace=True)

        y = self.encode_class_value(
            dataframe['Category'].values, self.new_model_path + '/label_encoder.pkl')

        print('Restored data from Mongo')
        sys.stdout.flush()
        return dataframe, y

    def open_mongo_connections(self):
        self.mongo = MongoDatabase('dev')
        self.mongo.connect()
        self.mongo_conn = self.mongo

    def close_mongo_connection(self):
        self.mongo.close_connection()

    def encode_class_value(self, class_value, encoder_path):
        encoder = LabelEncoder()
        y = encoder.fit_transform(class_value)

        output_encoder = open(encoder_path, 'wb')
        pickle.dump(encoder, output_encoder)
        output_encoder.close()
        
        return y

    def get_previsors_attrib(self, dataframe):
        description = [[x] for x in dataframe['description']]
        product_name = [[x] for x in dataframe['name']]

        X = utils.get_cleaned_predictor(description, product_name)
        
        X, self.tokenizer = utils.preprocessing_fn(
            X, self.new_model_path + '/token')

        print('Pre-processed data')
        return X

    def create_model_instance(self, y, vocab_size):
        nb_classes = len(set(y))

        cnn = CNN(vocab_size=vocab_size, emb_dim=300, nb_filters=100,
            ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

        print('Created model instance')
        sys.stdout.flush()
        return cnn

    def evaluate_and_deploy_model(self, cnn, X_test, y_test, y):
        model_version = '{"version": "%s"}' %(self.new_model_path.split('/')[-1])

        new_model_accuracy, new_model_f1 = self.evaluate_model(cnn, X_test, y_test)

        last_model_accuracy, last_model_f1 = self.get_last_model_performance(
            self.last_model_path, X_test, y_test, y)

        if new_model_f1 >= last_model_f1 and (new_model_accuracy - last_model_accuracy) >= -1:
            shutil.rmtree(self.last_model_path)
            utils.read_file(os.getcwd() + '/config.txt', model_version)
            self.create_and_deploy_tarfile(self.new_model_path + '.tar.gz', self.new_model_path)
            subprocess.call(os.getcwd() + '/pypi-upload.sh')
        else: 
            shutil.rmtree(self.new_model_path)

    def get_last_model_performance(self, last_model_path, X_test, y_test, y):
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(last_model_path + '/token')
   
        last_cnn = self.create_model_instance(y, tokenizer.vocab_size)
        last_cnn.load_weights(last_model_path + '/model_checkpoint/cp.ckpt').expect_partial()

        last_cnn.compile(loss=self.loss_f, optimizer='adam', metrics=['accuracy'])
        return self.evaluate_model(last_cnn, X_test, y_test)

    def create_and_deploy_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        DeployModel().deploy_to_s3(self.new_model_path + '.tar.gz')
        os.remove(self.new_model_path + '.tar.gz')

    def evaluate_model(self, model, X_test, y_test):
        y_pred_test = model.predict(X_test)
        predicted = [result.argmax() for result in y_pred_test]
        
        f_score = f1_score(y_test, predicted , average='macro')
        accuracy = model.evaluate(X_test, y_test, batch_size=64)[1]

        print(classification_report(y_test, predicted))
        print('Accuracy: ', accuracy)

        return accuracy, f_score

    def predict_and_plot_matrix(self, model, X, y):
        y_pred_test = model.predict(X)
        predicted = [result.argmax() for result in y_pred_test]
        self.show_confusion_matrix(y, predicted)

    def show_confusion_matrix(self, y_test, predicted):
        fig, ax = plt.subplots(figsize=(10,10))
        cm = confusion_matrix(y_test, predicted)
        sns.heatmap(cm, annot=True)
        plt.show()

trainProductsModel(argv[1] if len(argv) > 1 else 'food_model')
