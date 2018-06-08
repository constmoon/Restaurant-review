def backend():
    from sklearn.externals import joblib

    from sklearn import svm
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import cross_val_score
    import numpy as np
    import csv
    from konlpy.tag import Twitter



    nlp = Twitter()  # Twitter 라이브러리 사용
    data_ = csv.reader(open("tempdata.txt",'r',encoding='utf-8'), delimiter='\t')


    dataset_data = []
    dataset_labels = []

    count = 0

    for row in data_:
        count+=1



        #형태소 분석 후 임시리스트에 저장
        pos = nlp.pos(row[3],stem=True, norm=True)
        total_string = ""
        templist = []


        for word in pos:
            POS=word[1]
            string = ''

            #알파벳, 숫자, 외국어 제외
            if POS != 'Foreign' and POS != 'Alpha' and POS!='Number':
                if word[0] != '/': #||

                    string+=word[0]+word[1][0] +word[1][-1]

                if string == ('연락처Nn' or '전화번호Nn' or '전번Nn' or '전화Nn'):
                    string = '폰넘버Nn'

                total_string = total_string + " " + string
                templist.append(string)



        dataset_data.append(total_string)
        dataset_labels.append(type)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    test_data = vectorizer.fit_transform(dataset_data)

    clf = joblib.load('tfidf_svm-linear_2.pkl')

    return(clf.predict(dataset_data)[0] ) #test_data
