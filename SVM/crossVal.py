
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score


import csv
from konlpy.tag import Twitter
import time


start_time = time.time()
nlp = Twitter()  # Twitter 라이브러리 사용
data_ = csv.reader(open("4test.txt",'r',encoding='utf-8'), delimiter='\t')

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

        #형태소 분석 후 임시리스트에 저장
        pos = nlp.pos(row[3],stem=True, norm=True)
        total_string = ""



        for word in pos:
            POS=word[1]
            string = ''
            #알파벳, 숫자, 외국어 제외
            if POS != 'Foreign' and POS != 'Alpha' and POS!='Number':
                if word[0] != '/':

                    string+=word[0]+word[1][0] +word[1][-1]

                if string == ('연락처Nn' or '전화번호Nn' or '전번Nn' or '전화Nn'):
                    string = '폰넘버Nn'

                total_string = total_string + " " + string


        dataset_data.append(total_string)
        dataset_labels.append(type)
    print("thitithithithishdithpdiht",count)
    clf(dataset_data, dataset_labels)

def clf(dataset_data,dataset_labels):

    #Classfier
    for kernel in ['linear','rbf','poly']:
        print("\n\n\n\n\n",kernel)
        clf =svm.SVC(kernel=kernel, C=1, cache_size=200)


        #lowercase 굳이 할필요 없을 것 같아서 False로 두었고,
        #나머지 옵션들은 무슨 의미인지 몰라서 아직 추가하지 않았다.
        vectorizer = TfidfVectorizer(lowercase=False)

        #TFIDF vectorizer로 fit해서 벡터화
        vtr_dataset = vectorizer.fit_transform(dataset_data)

        print(vtr_dataset)

        #교차검증 실행
        scores = cross_val_score(clf, vtr_dataset, dataset_labels, cv=5)
        end_time = time.time()

        print(print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)))

        print("time: ", (end_time-start_time)/60,"분")


tokenize(nlp,data_)