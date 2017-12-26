'''
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from collections import namedtuple
from gensim.models import doc2vec
import pickle

import csv
from konlpy.tag import Twitter
import time

start_time = time.time()
data_ = csv.reader(open("rawdata.txt",'r',encoding='utf-8'), delimiter='\t')#


dataset_labels = []


count = 0
for row in data_:
    count+=1
    #가짜 리뷰 type은 0, 진짜 리뷰 type은 1
    if row[0] =='\ufefffake' or row[0] == 'fake':
        type ='0'
    elif row[0] =='real':
        type ='1'

    dataset_labels.append(type)



vectorizer = TfidfVectorizer(ngram_range=(1, 2))

fileObject = open("dataset_data_tfidf.txt",'rb')
dataset_data = pickle.load(fileObject,encoding='utf-8')

clf =svm.SVC(kernel='linear', C=1)
clf.fit(dataset_data,dataset_labels)
end_time = time.time()

print("종료: ", (end_time - start_time) / 60, "분")





end_time = time.time()

print("종료: ", (end_time - start_time) / 60, "분")

'''

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
import numpy as np
import csv
from konlpy.tag import Twitter
import time



nlp = Twitter()  # Twitter 라이브러리 사용
data_ = csv.reader(open("4test.txt",'r',encoding='utf-8'), delimiter='\t') #rawdata.txt

def tokenize(nlp,data):
    dataset_data = []
    dataset_labels = []

    count = 0
    for row in data:
        count+=1
        #가짜 리뷰 type은 0, 진짜 리뷰 type은 1
        if row[0] =='\ufefffake' or row[0] == 'fake':
            type ='0'
        elif row[0] =='real':
            type ='1'
        else:
            type='1'

        #형태소 분석 후 임시리스트에 저장
        pos = nlp.pos(row[3],stem=True, norm=True)
        total_string = ""



        for word in pos:
            POS=word[1]
            string = ''


            #알파벳, 숫자, 외국어 제외
            if POS != 'Foreign' and POS != 'Alpha' and POS!='Number':
                if word[0] != '||':

                    string+=word[0]+  word[1][0] +word[1][-1]

                if string == ('연락처 Nn' or '전화번호 Nn' or '전번 Nn' or '전화 Nn'):
                    string = '폰넘버 Nn'

                total_string = total_string + " " + string
                #print(string)


        dataset_data.append(total_string)
        dataset_labels.append(type)
    print("thitithithithishdithpdiht",count)
    clf(dataset_data, dataset_labels)

def clf(dataset_data,dataset_labels):
    start_time1 = time.time()
    # lowercase 굳이 할필요 없을 것 같아서 False로 두었고,
    # 나머지 옵션들은 무슨 의미인지 몰라서 아직 추가하지 않았다.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2) ,lowercase=False)

    # TFIDF vectorizer로 fit해서 벡터화
    vtr_dataset = vectorizer.fit_transform(dataset_data)

    #Classfier
    from sklearn.externals import joblib
    #joblib.dump(vectorizer.get_feature_names(), 'tfidf_features_name.pkl')

    clf =svm.SVC(kernel='linear', C=1)
    from sklearn.pipeline import Pipeline
    tfidf_svm= Pipeline([('tfidf',vectorizer) , ( 'svc', clf) ] )
    tfidf_svm.fit(dataset_data, dataset_labels) #vtr_dataset
    #clf.fit(vtr_dataset, dataset_labels)
   
    joblib.dump(tfidf_svm, 'tfidf_svm-linear_2.pkl')
    #clf = joblib.load('tfidf_svm-linear.pkl')

    '''
    scores = cross_val_score(clf, vtr_dataset, dataset_labels, cv=5)
    print(scores)
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    print(feature_names)
    coef=clf.coef_
    coef =coef.toarray()
    coefsq=[]
    for i in range(len(coef)):
        coefsq.append(coef[i] * coef[i])
    #print(type(a))
    #print(len(coef))

    top10 = np.argsort(coef[0])[-100:]
    top10sq = np.argsort(coef[0])[-100:]

    print("역순으로 top20          : %s" % (" / ".join(feature_names[j] for j in top10)))
    print("역순으로 teo20(squared) : %s" % (" / ".join(feature_names[j] for j in top10sq)))


    #print(top10)


    #scores = cross_val_score(clf, vtr_dataset, dataset_labels, cv=5)
    '''
    end_time = time.time()
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    print("time: ", (end_time - start_time1) / 60, "분")



tokenize(nlp,data_)