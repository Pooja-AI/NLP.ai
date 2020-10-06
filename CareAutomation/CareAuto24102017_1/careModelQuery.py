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
import json, os
import re

###############################
## get the similar cases for a given title
##################################
class careSimiQuery:

    ''' care predict solution creation class '''
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()
    
    def __init__(self):
        print('creating care predict solution class instance...')
        
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
        
    def remove_char(self,lst):
          lst=list(map(lambda x: str(x).replace('"', ''), lst))
          lst=list(map(lambda x: str(x).replace('\t', ''), lst))
          lst=list(map(lambda x: str(x).replace('\n', ''), lst))
          lst=list(map(lambda x: str(x).replace('\\', ''), lst))
          return lst

    def getMatchedWords(self,qryDoc, matchDoc):
        #print('getting matched words ...')
        query_doc = self.clean(qryDoc)
        match_doc = self.clean(matchDoc)
        query_doc = [w.lower() for w in word_tokenize(query_doc)]
        match_doc = [w.lower() for w in word_tokenize(match_doc)]    
        dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(self.dest,"tktCare.dict"))
        query_doc_bow = dictionary_qry.doc2bow(query_doc)
        matched_doc_bow = dictionary_qry.doc2bow(match_doc)
        wrds=[]
        wrds=[dictionary_qry[i[0]] for i in matched_doc_bow for j in query_doc_bow if(i[0]==j[0])]
        return wrds
    def getSimilarity(self,tstStr):
        datafileNm="/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/tickets.csv"
        tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
        tktdf['Final Solution']=tktdf['Final Solution'].dropna()
        tktdf['Case Title']=tktdf['Case Title'].dropna()
        tktdf['Case Number']=tktdf['Case Number'].dropna()
        tktdf['Product']=tktdf['Product'].dropna()
        tktdf['Description']=tktdf['Description'].dropna()
        #collect requried fields
        txtdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time','Description','Final Solution']])
        txtdf_rev['title_desc']=txtdf_rev['Product']+" "+txtdf_rev['Case Title']+" "+txtdf_rev['Description']
        txtdf_rev_prod_lst=txtdf_rev['Product'].tolist()
        txtdf_rev_desc_lst=txtdf_rev['title_desc'].tolist()
        tktdf_rev_case_lst =txtdf_rev['Case Number'].tolist()
        tktdf_rev_title_lst =txtdf_rev['Case Title'].tolist()
        tktdf_rev_fnlSol_lst =txtdf_rev['Final Solution'].tolist()
        
        tktdf_rev_fnlSol_lst=self.remove_char(tktdf_rev_fnlSol_lst)
        tktdf_rev_title_lst=self.remove_char(tktdf_rev_title_lst)
        query_json=tstStr
        # json dump for converting dict to string.
        # .decode("utf-8") to convert binary string to normal string and then json.loads() to parse the json
        queryData=json.loads(query_json)
        QryStr=queryData["product"]+" "+queryData["title"]
        print('Getting the similar cases & resolutions for ..',QryStr)
        query_doc = self.clean(QryStr)
        query_doc = [w.lower() for w in word_tokenize(query_doc)]
        dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(self.dest, "tktCare.dict"))
        query_doc_bow = dictionary_qry.doc2bow(query_doc)
        tf_idf_qry=gensim.models.TfidfModel.load(os.path.join(self.dest,"tktCare.tfidf"))
        query_doc_tf_idf = tf_idf_qry[query_doc_bow]
        ### get best 3 similarity documents
        sims = gensim.similarities.Similarity.load(os.path.join(self.dest,"tktCare.model"))
        sims.num_best = 3
        ## print(sims[query_doc_tf_idf])
        qryRespStr=""
        # changed single quotes around the keys and values to double quotes and restructured to valid json format
        qryRespStr='{"uuid":'+str(queryData["uuid"])+',"simiRecords":['
        ##
        for i in sims[query_doc_tf_idf]:
            wrds1=self.getMatchedWords(QryStr,txtdf_rev_prod_lst[i[0]]+" "+tktdf_rev_title_lst[i[0]])
            wrds1=";".join(wrds1)
            qryRespStr=qryRespStr+'{"simiRec":{"casenumber":"'+tktdf_rev_case_lst[i[0]]+'","confidence":"'+i[1].astype(str)+'","solution":"'+ tktdf_rev_fnlSol_lst[i[0]]+'","title":"'+tktdf_rev_title_lst[i[0]]+'","matchedWords":"'+wrds1+'"}},'
            
        qryRespStr=qryRespStr[:-1]+"]}"
        print('returning response json as ..',qryRespStr)
        return qryRespStr

#tstStr1='{"uuid": "2341234523gafsda", "product": "One-NDS", "title": "Provisioning Scripting for CRM system - Multi-SIM"}'
#print('calling similarity function...')
#prdsol=careSimiQuery()
#prdsol.getSimilarity(tstStr1)


