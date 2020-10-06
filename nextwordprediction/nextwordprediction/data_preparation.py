import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import os
import html
import re
import string
import pickle
import collections
import string
class Preprocessing(object):
    def __init__(self,data_dir, sequence_len=None, test_size=0.2,  random_state=1, ensure_preprocessed=False):

        """
         Initiallizes an interface to load, preprocess and split data into train,
        validation and test sets
        :param data_dir: Data directory containing the dataset file 'dataset' with columns 'summary' and
                         'Description'
        :param sequence_len: Optional. Let m be the maximum sequence length in the dataset. Then, it's required that
                          sequence_len >= m. If sequence_len is None, then it'll be automatically assigned to m.
        :param test_size: Optional. 0<test_size<1. Represents the proportion of the dataset to included in the test
                          split. Default is 0.2
        :param random_state: Optional. Random seed used for splitting data into train, test and validation sets. Default is 0.
        :param ensure_preprocessed: Optional. If ensure_preprocessed=True, ensures that the dataset is already
                          preprocessed. Default is False
        """
        self.sequence_len = sequence_len
        self._input_file = os.path.join(data_dir, 'JIRA_solution.xlsx')
        self._features = None
        self._labels = None
        self.dictionary=None
        self.reverse_dictionary=None
        self.vocab_size = None
        self._content = None
        self._window=3
        self._lengths=None

 
        # Split data in train, validation and test sets
        self._current_index = 0
        self._epoch_completed = 0
        self.dictionary, self.reverse_dictionary =self.__preprocess()
        #print(self._dictionary)
        self._features,self._labels=self.__sampling(self._content,self.dictionary,self._window)
        self._features = np.array([np.array(xi) for xi in self._features])
        self._labels = np.array(self._labels)
        #print(self._features)
        indices = np.arange(len(self._labels))
        length = [self._window for i in range(len(self._features))]
        self._lengths = np.array(length)
        #print(self._lengths)
        #print(self._labels)
        x_tv, self._x_test, y_tv, self._y_test,tv_indices, test_indices = train_test_split(
            self._features,
            self._labels,
            indices,
            test_size=test_size,
            random_state=random_state)
        self._x_train, self._x_val, self._y_train, self._y_val,train_indices, val_indices = train_test_split(
            x_tv,
            y_tv,
            tv_indices,
            test_size=test_size,
            random_state=random_state)
        #print(self._y_train.shape)
        self._val_indices = val_indices
        self._test_indices = test_indices
        self._train_lengths = self._lengths[train_indices]
        self._val_lengths = self._lengths[val_indices]
        self._test_lengths = self._lengths[test_indices]
        
        
  
    def __preprocess(self):
        """
        Loads data from data_dir/data.csv, preprocesses each sample loaded and stores intermediate files to avoid
        preprocessing later.
        """
        # Load data
        isolar_data = pd.read_excel(self._input_file,encoding ="ISO-8859-1")
        isolar_data_pd = isolar_data[['Summary','Description']]
        isolar_data_pd = isolar_data_pd.dropna()
        isolar_data_pd['input_data'] = isolar_data_pd['Summary']+" "+isolar_data_pd['Description']
        isolar_list = isolar_data_pd['input_data'].tolist() 
        self._content = [x.strip() for x in isolar_list]
        self._content = [word for i in range(len(self._content)) for word in self._content[i].split() if len(word)>3 ]
        #print(self._content)
        # Prepare vocabulary dict
        count = collections.Counter(self._content).most_common()
        #print(len(count))
        self.dictionary = dict()
        for word, _ in count:
            self.dictionary[word] = len(self.dictionary)
        self.reverse_dictionary = dict(zip(self.dictionary.values(), self.dictionary.keys()))
        self.vocab_size = len(self.dictionary)
        self.n_classes =self.vocab_size
        #print(self._vocab_size)
        #print(list(self.dictionary)[0:30])
        return self.dictionary, self.reverse_dictionary
        
        
    def __sampling(self,words, dictionary, window):
        features = []
        labels = []
        sample=[]
        
        for index in range(0, len(words) -self._window):
            for i in range(0, self._window):
                sample.append(dictionary[words[index + i]])
                if (i + 1) % self._window == 0:
                    features.append(sample)
                    labels.append(dictionary[words[index + i + 1]])
                    sample=[]
        
        self.sequence_len, self._features = self.__apply_to_zeros(features, self.sequence_len)
        self._labels = self.__one_hot_encoding(labels, self.vocab_size)
        #print(self._labels[0][251])
        #print(self.sequence_len)
        return self._features,self._labels
        
        
    def next_batch(self, batch_size):
        """
        :param batch_size: batch_size>0. Number of samples that'll be included
        :return: Returns batch size samples (text_tensor, text_target, text_length)
        """
        start = self._current_index
        self._current_index += batch_size
        #print("ytrain")
        #print(len(self._y_train))
        if self._current_index > len(self._y_train):
            # Complete epoch and randomly shuffle train samples
            self._epoch_completed += 1
            
            ind = np.arange(len(self._y_train))
            np.random.shuffle(ind)
            self._x_train = self._x_train[ind]
            self._y_train = self._y_train[ind]
            self._train_lengths = self._train_lengths[ind]
            start = 0
            self._current_index = batch_size
        end = self._current_index
        #print(self._y_train[start:end])
        return self._x_train[start:end], self._y_train[start:end], self._train_lengths[start:end]
        
    def __apply_to_zeros(self,lst, sequence_len=None):
        """
        Pads lst with zeros according to sequence_len
        :param lst: List to be padded
        :param sequence_len: Optional. Let m be the maximum sequence length in lst. Then, it's required that
                          sequence_len >= m. If sequence_len is None, then it'll be automatically assigned to m.
        :return: padding_length used and numpy array of padded tensors.
        """
    # Find maximum length m and ensure that m>=sequence_len
        inner_max_len = max(map(len, lst))
        if sequence_len is not None:
            if inner_max_len > sequence_len:
                raise Exception('Error: Provided sequence length is not sufficient')
            else:
                inner_max_len = sequence_len
                # Pad list with zeros
        result = np.zeros([len(lst), inner_max_len], np.int32)
        #print(result)
        for i, row in enumerate(lst):
            for j, val in enumerate(row):
                result[i][j] = val
        return inner_max_len, result 
    
    def __one_hot_encoding(self, lst, size):
        result = np.zeros([len(lst), size], np.float32)
        for i , row in enumerate(lst):
            result[i][row] = 1
        return result
             
    def get_val_data(self):
        """
        :param original_text. Optional. Whether to return original samples or not.
        :return: Returns the validation data. If original_text returns (original_samples, text_tensor, text_target,
                 text_length), otherwise returns (text_tensor, text_target, text_length)
        """
       
        return self._x_val, self._y_val, self._val_lengths

    def get_test_data(self):
        """
        :param original_text. Optional. Whether to return original samples or not.
        :return: Returns the test data. If original_text returns (original_samples, text_tensor, text_target,
                 text_length), otherwise returns (text_tensor, text_target, text_length)
        """
        
        return self._x_test, self._y_test,self._test_lengths
data_dir = '/home/tcs/Documents/Infineon/tf_lstm_nwp/data'
sample = Preprocessing(data_dir)

