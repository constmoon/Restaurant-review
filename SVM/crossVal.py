
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import cross_val_score
from sklearn import datasets

import csv
from konlpy.tag import Twitter
import time


start_time = time.time()
nlp = Twitter()  # Twitter 라이브러리 사용
data_ = csv.reader(open("reviews_rawdata_4.txt",'r',encoding='utf-8'), delimiter='\t')

def tokenize(nlp,data):
    dataset_data = []
    dataset_labels = []


    for row in data:
        if row[0] =='\ufefffake' or row[0] == 'fake':
            type ='0'
        elif row[0] =='real':
            type ='1'


        pos = nlp.pos(row[3],stem=True, norm=True)
        templist = []



        for word in pos:
            POS=word[1]
            if POS != 'Foreign' and POS != 'Alpha' and POS!='Number':

                string=''
                string+=word[0]+word[1][0] +word[1][-1]


                if string == ('연락처Nn' or '전화번호Nn' or '전번Nn' or '전화Nn'):
                    string = '폰넘버Nn'


                #문장부호는 끝에 pn이라고 붙는데 이걸 방지
                if not string[len(string)-3:] == "Pn":
                    templist.append(string)


            dataset_data.append(string)
            dataset_labels.append(type)

    clf(dataset_data, dataset_labels)

def clf(dataset_data,dataset_labels):
    clf =svm.SVC(kernel='linear', C=1)
    vectorizer = TfidfVectorizer(lowercase=False)
    vtr_dataset = vectorizer.fit_transform(dataset_data)

    scores = cross_val_score(clf, vtr_dataset, dataset_labels, cv=5)
    print(print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)))


    print("time: ", start_time)


tokenize(nlp,data_)
