from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

from collections import namedtuple
from gensim.models import doc2vec

import csv
from konlpy.tag import Twitter
import time


start_time = time.time()
nlp = Twitter()  # Twitter 라이브러리 사용
data_ = csv.reader(open("reviews_rawdata_4.txt",'r',encoding='utf-8'),delimiter='\t')

def tokenize(nlp,data):
    train_data = []
    train_labels = []
    test_data =[]
    test_labels = []

    train_data2 = []
    test_data2 = []

    flag = 0 #training data와 testing data 2:1 분리


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

                templist.append(string)

        if templist:
            temptu= (templist, type)

        if flag % 3 == 0:
            test_data.append(string)
            test_labels.append(type)
            test_data2.append(temptu)

        else:
            train_data.append(string)
            train_labels.append(type)
            train_data2.append(temptu)

        flag += 1


    vectorizer = TfidfVectorizer(min_df=1,
                             max_df = 0.9,
                             sublinear_tf=True,
                             use_idf=True, ngram_range = (1,2))
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

    TaggedDocument = namedtuple('TaggedDocument', 'words tags')

    tagged_train_docs = [TaggedDocument(d, [c]) for d, c in train_data2]
    tagged_test_docs = [TaggedDocument(d, [c]) for d, c in test_data2]

    #doc2vec
    vectorizer2 = doc2vec.Doc2Vec(size=500, alpha=0.025, min_alpha=0.025, seed=1234)
    vectorizer2.build_vocab(tagged_train_docs)

    for epoch in range(10):
        vectorizer2.train(tagged_train_docs,total_examples=vectorizer2.corpus_count, epochs=vectorizer2.iter)
        vectorizer2.alpha -= 0.002  # decrease the learning rate
        vectorizer2.min_alpha = vectorizer2.alpha  # fix the learning rate, no decay
    # Perform classification with SVM, kernel=rbf

    train_x = [vectorizer2.infer_vector(doc.words) for doc in tagged_train_docs]
    train_y = [doc.tags[0] for doc in tagged_train_docs]

    test_x = [vectorizer2.infer_vector(doc.words) for doc in tagged_test_docs]
    test_y = [doc.tags[0] for doc in tagged_test_docs]

    '''
    #word2vec
    vectorizer3 = word2vec.Word2Vec(size=500, alpha=0.025, min_alpha=0.025, seed=1234)
    vectorizer3.build_vocab(tagged_train_docs)
    vectorizer3.train(tagged_train_docs, epochs=vectorizer3.iter)

    train_xw = [vectorizer3.infer_vector(doc.words) for doc in tagged_train_docs]
    train_yw = [doc.tags[0] for doc in tagged_train_docs]

    test_xw = [vectorizer3.infer_vector(doc.words) for doc in tagged_test_docs]
    test_yw = [doc.tags[0] for doc in tagged_test_docs]
    '''
    print("-------------------Tf-idf Below----------------")
    classify(train_vectors, train_labels, test_vectors, test_labels)
    print("-------------------doc2vec Below----------------")
    classify(train_x, train_y, test_x, test_y)
    print("-------------------wor2vec Below----------------")
    #classify(train_xw, train_yw, test_xw, test_yw)

# Perform classification with SVM, kernel=rbf


def classify(train_vectors, train_labels, test_vectors, test_labels):
    # rbf 방식의 classification
    classifier_rbf = svm.SVC()
    classifier_rbf.fit(train_vectors, train_labels)
    prediction_rbf = classifier_rbf.predict(test_vectors)

    # classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    classifier_linear.fit(train_vectors, train_labels)
    prediction_linear = classifier_linear.predict(test_vectors)

    # Perform classification with SVM, kernel=liblinear
    classifier_liblinear = svm.LinearSVC()
    classifier_liblinear.fit(train_vectors, train_labels)
    prediction_liblinear = classifier_liblinear.predict(test_vectors)


    print("Results for SVC(kernel=rbf)")
    print(classification_report(test_labels, prediction_rbf))
    print("Accuracy of kernel rbf :", classifier_rbf.score(test_vectors, test_labels))


    print("Results for SVC(kernel=linear)")
    print(classification_report(test_labels, prediction_linear))
    print("Accuracy of kernel linear :", classifier_linear.score(test_vectors, test_labels))
    print("Results for LinearSVC()")
    print(classification_report(test_labels, prediction_liblinear))
    classifier_liblinear.score(test_vectors, test_labels)
    print("Accuracy of kernel liblinear :", classifier_liblinear.score(test_vectors,test_labels))

    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression(random_state=1234)
    classifier.fit(train_vectors, train_labels)
    print("LogisticRegression accuracy:", classifier.score(test_vectors, test_labels))

tokenize(nlp, data_)