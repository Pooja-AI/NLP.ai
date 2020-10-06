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
import json
import os

###############################
## get the SME cases for a given title
##################################
class careSMEQuery:

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

    def getMatchedWords(self,qryDoc, matchDoc):
        print('getting matched words ...')
        query_doc = self.clean(qryDoc)
        match_doc = self.clean(matchDoc)
        query_doc = [w.lower() for w in word_tokenize(query_doc)]
        match_doc = [w.lower() for w in word_tokenize(match_doc)]    
        ##print(query_doc)
        dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(self.dest,"tktCare.dict"))
        query_doc_bow = dictionary_qry.doc2bow(query_doc)
        matched_doc_bow = dictionary_qry.doc2bow(match_doc)
##        print(query_doc_bow)
##        print(matched_doc_bow)
        wrds=[]
        wrds=[dictionary_qry[i[0]] for i in matched_doc_bow for j in query_doc_bow if(i[0]==j[0])]
        return wrds
    
    def getSME(self,tstStr):
    ##    print('Generating Queries...')
        import pdb
        datafileNm="/home/allu/Documents/TCSProjetcs/NokiaCareAutomation _pooja/CareAuto24102017_1/tickets.csv"

        #input data file
        tktdf=pd.read_csv(datafileNm, encoding = "ISO-8859-1")
        tktdf['Final Solution']=tktdf['Final Solution'].dropna()
        tktdf['Case Title']=tktdf['Case Title'].dropna()
        tktdf['Case Number']=tktdf['Case Number'].dropna()
        tktdf['Product']=tktdf['Product'].dropna()
        tktdf['Description']=tktdf['Description'].dropna()

        #collect requried fields
        tktdf_rev=(tktdf[['Case Number','Case Title','Nokia Contact','Product','Created On','Solution Accepted Time', \
                  'Description','Final Solution']])
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

        query_json=tstStr
        # json dump for converting dict to string.
        # .decode("utf-8") to convert binary string to normal string and then json.loads() to parse the json
        queryData=json.loads(query_json)
        QryStr=queryData["product"]+" "+queryData["title"]
        print('Getting the best Nokia Contact & resolutions for ..',QryStr)
        query_doc = self.clean(QryStr)
        query_doc = [w.lower() for w in word_tokenize(query_doc)]
        ##print(query_doc)
        dictionary_qry = gensim.corpora.Dictionary.load(os.path.join(self.dest,"tktCare1.dict"))
        query_doc_bow = dictionary_qry.doc2bow(query_doc)
        ##print(query_doc_bow)
        tf_idf_qry=gensim.models.TfidfModel.load(os.path.join(self.dest,"tktCare1.tfidf"))
        query_doc_tf_idf = tf_idf_qry[query_doc_bow]
        ##print(query_doc_tf_idf)
        ##
        ### get best 3 SME
        spend = gensim.similarities.Similarity.load(os.path.join(self.dest,"tktCare1.model"))
        spend.num_best = 3
    ##    print(spend[query_doc_tf_idf])

        print('')
        print('')
        qryRespStr=""
        # changed single quotes around the keys and values to double quotes and restructured to valid json format
        qryRespStr='{"uuid1":'+str(queryData["uuid1"])+',"SMERecords":['
        ##
        for i in spend[query_doc_tf_idf]:
            wrds1=self.getMatchedWords(QryStr,tktdf_rev_prod_lst[i[0]]+" "+tktdf_rev_title_lst[i[0]])
            wrds1=";".join(wrds1)
            print(wrds1)
            qryRespStr=qryRespStr+'{"SMERec":{"SME":"'+tktdf_rev_contact_lst[i[0]]+'","confidence1":"'+i[1].astype(str)+'"}},'
            # +'","solution":"'+ tktdf_rev_fnlSol_lst[i[0]]+'","title":"'+tktdf_rev_title_lst[i[0]]+'","matchedWords":"'+wrds1
        qryRespStr=qryRespStr[:-1]+"]}"
        print('returning response json as ..',qryRespStr)
        return qryRespStr

    
#tstStr1='{"uuid1": "2341234523gafsda", "product": "One-NDS", "title": "Provisioning Scripting for CRM system - Multi-SIM"}'
#print('calling similarity function...')
#prdsol=careSMEQuery()
#prdsol.getSME(tstStr1)

