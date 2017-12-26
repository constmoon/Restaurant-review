
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from collections import namedtuple
from gensim.models import doc2vec


import csv
from konlpy.tag import Twitter
import time



nlp = Twitter()  # Twitter 라이브러리 사용
data_ = csv.reader(open("review.txt",'r',encoding='utf-8'), delimiter='\t')

def tokenize(nlp,data):
    dataset_data = []
    dataset_labels = []
    dataset4doc2vec = []

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
        templist = []


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
                templist.append(string)
        if templist:
            temptu= (templist, type)
            dataset4doc2vec.append(temptu)


        dataset_data.append(total_string)
        dataset_labels.append(type)
    print("thitithithithishdithpdiht",count)
    clf(dataset_data, dataset_labels, dataset4doc2vec)

def clf(dataset_data,dataset_labels,dataset4doc2vec):
    # lowercase 굳이 할필요 없을 것 같아서 False로 두었고,
    # 나머지 옵션들은 무슨 의미인지 몰라서 아직 추가하지 않았다.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # TFIDF vectorizer로 fit해서 벡터화
    vtr_dataset = vectorizer.fit_transform(dataset_data)

    print(vtr_dataset)


    #doc2vec 트레이닝
    TaggedDocument = namedtuple('TaggedDocument', 'words tags')
    tagged_train_docs = [TaggedDocument(d, [c]) for d, c in dataset4doc2vec]
    vectorizer2 = doc2vec.Doc2Vec(size=500, alpha=0.025, min_alpha=0.025, seed=1234)
    vectorizer2.build_vocab(tagged_train_docs)
    for epoch in range(10):
        vectorizer2.train(tagged_train_docs,total_examples=vectorizer2.corpus_count, epochs=vectorizer2.iter)
        vectorizer2.alpha -= 0.002  # decrease the learning rate
        vectorizer2.min_alpha = vectorizer2.alpha  # fix the learning rate, no decay
    train_x = [vectorizer2.infer_vector(doc.words) for doc in tagged_train_docs]
    train_y = [doc.tags[0] for doc in tagged_train_docs]

    #Classfier
    for kernel in ['linear','rbf','poly']:

        clf =svm.SVC(kernel=kernel, C=1, cache_size=2000)


        #tfidf교차검증 실행
        print("\n\n\ntf-idf", kernel)
        start_time1 = time.time()
        scores = cross_val_score(clf, vtr_dataset, dataset_labels, cv=5)
        end_time = time.time()
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        print("time: ", (end_time - start_time1) / 60, "분")


        #doc2vec교차검증 실행
        print("\n\n\ndoc2vec", kernel)
        start_time2 = time.time()
        scores2 = cross_val_score(clf, train_x, train_y, cv=5)
        end_time2 = time.time()

        print("Accuracy: %0.2f (+/- %0.2f)" % (scores2.mean(), scores2.std() * 2))
        print("time: ", (end_time2-start_time2)/60,"분")

    from sklearn.ensemble import VotingClassifier

    voting_clf = VotingClassifier(
        estimators=[('lr', 'clf1'), ('rf', 'clf2'),('svc', 'clf3')],
        voting = 'soft')




tokenize(nlp,data_)