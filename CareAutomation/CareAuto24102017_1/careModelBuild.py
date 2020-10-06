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

class careSimiModel:
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

    def createSimiModel(self,uuid):
        '''create model function '''
        print('in create model function...', uuid)
        datafileNm="/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/tickets.csv"

        #input data file
        tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
        
        tktdf['Final Solution']=tktdf['Final Solution'].dropna()
        tktdf['Case Title']=tktdf['Case Title'].dropna()
        tktdf['Case Number']=tktdf['Case Number'].dropna()
        tktdf['Product']=tktdf['Product'].dropna()
        tktdf['Description']=tktdf['Description'].dropna()
      #collect requried fields
        txtdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time','Description','Final Solution']])
       
        txtdf_rev['title_desc']=txtdf_rev['Product']+" "+txtdf_rev['Case Title']+" "+txtdf_rev['Description']

        ##txtdf_rev_desc_lst=txtdf_rev['Description'].head(10).tolist()
        txtdf_rev_desc_lst=txtdf_rev['title_desc'].tolist()
        tktdf_rev_case_lst =txtdf_rev['Case Number'].tolist()
        tktdf_rev_title_lst =txtdf_rev['Case Title'].tolist()
        tktdf_rev_fnlSol_lst =txtdf_rev['Final Solution'].tolist()
        
        #clearing the documents
        doc_clean = [self.clean(doc).split() for doc in txtdf_rev_desc_lst]
        ##print(type(doc_clean))
        print(doc_clean)
        #Dictionary – a mapping between words and their integer ids 
        dictionary = gensim.corpora.Dictionary(doc_clean)

        # save to the file system which will be called in the client
        dictionary.save(os.path.join(self.dest,"tktCare.dict"))

        #Convert document (a list of words) into the bag-of-words
    
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in doc_clean]
        # transformation into TF_IDF matrix 
        tf_idf = gensim.models.TfidfModel(corpus)
        
        # save to the file system which will be called in the client
        tf_idf.save(os.path.join(self.dest,"tktCare.tfidf"))

        #functions and classes for computing similarities across a collection of documents
        sims = gensim.similarities.Similarity('/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1',tf_idf[corpus],
                                      num_features=len(dictionary))

        sims.save(os.path.join(self.dest,"tktCare.model"))

#creatinig model
#careMdl=careSimiModel()
#careMdl.createSimiModel('1112')

