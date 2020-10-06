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

datafileNm="/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/tickets.csv"

dest ='/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/'
if not os.path.exists(dest):
    os.makedirs(dest)
#input data file
tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
##print(tktdf.head(5))

tktdf['Final Solution']=tktdf['Final Solution'].dropna()
tktdf['Case Title']=tktdf['Case Title'].dropna()
tktdf['Case Number']=tktdf['Case Number'].dropna()
tktdf['Product']=tktdf['Product'].dropna()
tktdf['Description']=tktdf['Description'].dropna()

#collect requried fields
txtdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time','Description','Final Solution']])
#txtdf_rev=txtdf_rev.head(500)
txtdf_rev['title_desc']=txtdf_rev['Product']+" "+txtdf_rev['Case Title']+" "+txtdf_rev['Description']

##txtdf_rev_desc_lst=txtdf_rev['Description'].head(10).tolist()
txtdf_rev_desc_lst=txtdf_rev['title_desc'].tolist()
tktdf_rev_case_lst =txtdf_rev['Case Number'].tolist()
tktdf_rev_title_lst =txtdf_rev['Case Title'].tolist()
tktdf_rev_fnlSol_lst =txtdf_rev['Final Solution'].tolist()

##txtdf_rev_desc_lst=set(txtdf_rev_desc_lst)

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

# clean document
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

#clearing the documents
doc_clean = [clean(doc).split() for doc in txtdf_rev_desc_lst]
##print(type(doc_clean))
print(doc_clean)

#Dictionary – a mapping between words and their integer ids 
#
dictionary = gensim.corpora.Dictionary(doc_clean)
##print("Number of words in dictionary:",len(dictionary))
##for i in range(len(dictionary)):
##    print(i, dictionary[i])
# save to the file system which will be called in the client
dictionary.save(os.path.join(dest,"tktCare.dict"))

#Convert document (a list of words) into the bag-of-words
#
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in doc_clean]
##print('...corpus')
##print(corpus)

# transformation into TF_IDF matrix 
tf_idf = gensim.models.TfidfModel(corpus)
##print(tf_idf)
# save to the file system which will be called in the client
tf_idf.save(os.path.join(dest,"tktCare.tfidf"))

#functions and classes for computing similarities across a collection of documents
sims = gensim.similarities.Similarity('/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1',tf_idf[corpus],
                              num_features=len(dictionary))

sims.save(os.path.join(dest,"tktCare.model"))



###############################
## get the similar cases for a given title
##################################
def getSimilarity(tstStr):
    ##print('Generating Queries...')
    query_title=tstStr1
    print('Getting the similar cases & resolutions for ..',query_title)
    query_doc = clean(query_title)
    query_doc = [w.lower() for w in word_tokenize(query_doc)]
    ##print(query_doc)
    dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(dest,"tktCare.dict"))
    query_doc_bow = dictionary_qry.doc2bow(query_doc)
    ##print(query_doc_bow)
    tf_idf_qry=gensim.models.TfidfModel.load(os.path.join(dest,"tktCare.tfidf"))
    query_doc_tf_idf = tf_idf_qry[query_doc_bow]
    ##print(query_doc_tf_idf)
    ##
    ### get best 3 similarity documents
    sims.num_best = 3
    ##    print(sims[query_doc_tf_idf])

    print('')
    print('')
    ##
    for i in sims[query_doc_tf_idf]:
        print("Case Number :: ",tktdf_rev_case_lst[i[0]],"::",tktdf_rev_title_lst[i[0]],"\nconfidence :: ",i[1]*100,"%")
        print("possible Sol ::",tktdf_rev_fnlSol_lst[i[0]])
        print('------------------------------------------------------------------------------------------------')
        print('')


tstStr1='NT HLR FE 15.5 SW LUP failing for 2G/3G after NT-HLR 15.5 Upgrade location update being cancelled SW system specified customer'
print('calling similarity function...')
getSimilarity(tstStr1)




