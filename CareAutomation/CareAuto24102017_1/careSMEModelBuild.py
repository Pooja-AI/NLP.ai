#!/usr/bin/python
#######
import pandas as pd
import numpy as np
import gensim
import sklearn.utils
from nltk.classify.scikitlearn import SklearnClassifier
##from sklearn.navie_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import os

class careSMEModel:
    ''' care model creation class '''
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    def __init__(self):
        print('creating care model class instance for provide relevant solutions...')
        
        self.dest ='/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/'
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

    # clean document
    def clean(self,doc):
        ''' clean the documents '''
        stop_free = " ".join([i for i in doc.lower().split() if i not in self.stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in self.exclude)
        normalized = " ".join(self.lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    def createSMEModel(self,uuid1):
        '''create model function '''
        print('in create model function...', uuid1)
        datafileNm="/home/tcs/Documents/nok/NokiaCareAutomation/CareAuto24102017_1/tickets.csv"

        #input data file
        tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
        ##print(tktdf.head(5))
        ##txtdf_rev_desc_lst=set(txtdf_rev_desc_lst)
        
        tktdf['Final Solution']=tktdf['Final Solution'].dropna()
        tktdf['Case Title']=tktdf['Case Title'].dropna()
        tktdf['Case Number']=tktdf['Case Number'].dropna()
        tktdf['Product']=tktdf['Product'].dropna()
        tktdf['Description']=tktdf['Description'].dropna()

       #collect requried fields
        tktdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time','Description','Final Solution']])
        tktdf_rev['title_desc']=tktdf_rev['Product']+" "+tktdf_rev['Case Title']
        #+" "+tktdf_rev['Description']
       ##tktdf_rev=tktdf_rev.head(n=100) # use if need to restict samples for testing
        tktdf_rev=tktdf_rev

        # define the attribute list used further in the processing
        tktdf_rev_prod_lst=tktdf_rev['Product'].tolist()
        tktdf_rev_desc_lst=tktdf_rev['Description'].tolist()
        tktdf_rev_case_lst =tktdf_rev['Case Number'].tolist()
        tktdf_rev_title_lst =tktdf_rev['Case Title'].tolist()
        tktdf_rev_fnlSol_lst =tktdf_rev['Final Solution'].tolist()
        tktdf_rev_title_desc_lst =tktdf_rev['title_desc'].tolist()
        tktdf_rev_contact_lst=tktdf_rev['Nokia Contact'].tolist()
       #tktdf_rev_contact_lst=set(tktdf_rev_contact_lst)
        #clearing the documents
        doc_clean = [self.clean(doc).split() for doc in tktdf_rev_desc_lst]
        ##print(type(doc_clean))
        print(doc_clean)
        #Dictionary – a mapping between words and their integer ids 
        dictionary = gensim.corpora.Dictionary(doc_clean)
        ##print("Number of words in dictionary:",len(dictionary))
        ##for i in range(len(dictionary)):
        ##    print(i, dictionary[i])
        # save to the file system which will be called in the client
        dictionary.save(os.path.join(self.dest,"tktCare1.dict"))

        #Convert document (a list of words) into the bag-of-words
        #
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in doc_clean]
        ##print('...corpus')
        ##print(corpus)

        # transformation into TF_IDF matrix 
        tf_idf = gensim.models.TfidfModel(corpus)
        ##print(tf_idf)
        # save to the file system which will be called in the client
        tf_idf.save(os.path.join(self.dest,"tktCare1.tfidf"))

        #functions and classes for computing similarities across a collection of documents
        spend = gensim.similarities.Similarity('/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1',tf_idf[corpus],
                                      num_features=len(dictionary))

        spend.save(os.path.join(self.dest,"tktCare1.model"))

#creatinig model
#careMdl=careSMEModel()
#careMdl.createSMEModel('1112')


