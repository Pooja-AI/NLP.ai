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

#input data file
datafileNm="/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/tickets.csv"
tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
tktdf['Final Solution']=tktdf['Final Solution'].dropna()
tktdf['Case Title']=tktdf['Case Title'].dropna()
tktdf['Case Number']=tktdf['Case Number'].dropna()
tktdf['Product']=tktdf['Product'].dropna()
tktdf['Description']=tktdf['Description'].dropna()


dest ='/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/'
if not os.path.exists(dest):
    os.makedirs(dest)

#collect requried fields
tktdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time', \
                  'Description','Final Solution']])
tktdf_rev['title_desc']=tktdf_rev['Product']+" "+tktdf_rev['Case Title']

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
##txtdf_rev_desc_lst=set(txtdf_rev_desc_lst)

# define the elements for document cleaning
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

# clean document
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# define features
def find_features(document):
    words = set(word.lower() for word in document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

tktdescdf=tktdf_rev['title_desc']
tktdescdf_lst=tktdescdf.tolist()


#clearing the documents
doc_clean = [clean(doc).split() for doc in tktdescdf_lst]
##pprint.pprint(doc_clean)


#Dictionary – a mapping between words and their integer ids 
#
dictionary = gensim.corpora.Dictionary(doc_clean)
##print("Number of words in dictionary:",len(dictionary))
##for i in range(len(dictionary)):
##    print(i, dictionary[i])
# save to the file system which will be called in the client
dictionary.save(os.path.join(dest,"tktCare1.dict"))

#Convert document (a list of words) into the bag-of-words
#
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in doc_clean]
##print('...corpus')
##print(corpus)

# transformation into TF_IDF matrix 
tf_idf = gensim.models.TfidfModel(corpus)
##print(tf_idf)
# save to the file system which will be called in the client
tf_idf.save(os.path.join(dest,"tktCare1.tfidf"))

#functions and classes for computing similarities across a collection of documents
spend = gensim.similarities.Similarity('//home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1',tf_idf[corpus],
                              num_features=len(dictionary))

spend.save(os.path.join(dest,"tktCare1.model"))



###############################
## get the SME cases for a given title
##################################
def getSME(tstStr):
##    print('Generating Queries...')
    query_title=tstStr1
    print('Getting the best Nokia Contact & resolutions for ..',query_title)
    query_doc = clean(query_title)
    query_doc = [w.lower() for w in word_tokenize(query_doc)]
    ##print(query_doc)
    dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(dest,"tktCare1.dict"))
    query_doc_bow = dictionary_qry.doc2bow(query_doc)
    ##print(query_doc_bow)
    tf_idf_qry=gensim.models.TfidfModel.load(os.path.join(dest,"tktCare1.tfidf"))
    query_doc_tf_idf = tf_idf_qry[query_doc_bow]
    ##print(query_doc_tf_idf)
    ##
    ### get best 3 SME 
    spend.num_best = 3
##    print(spend[query_doc_tf_idf])

    print('')
    print('')
    ##
    for i in spend[query_doc_tf_idf]:
        print("SME :: ",tktdf_rev_contact_lst[i[0]],"\nconfidence1 :: ",i[1]*100,"%")
        #print("possible Sol ::",tktdf_rev_fnlSol_lst[i[0]])
        print('------------------------------------------------------------------------------------------------')
        print('')


tstStr1='NT HLR FE 15.5 SW LUP failing for 2G/3G after NT-HLR 15.5 Upgrade location update being cancelled SW system specified customer'
print('calling getSME function...')
getSME(tstStr1)




