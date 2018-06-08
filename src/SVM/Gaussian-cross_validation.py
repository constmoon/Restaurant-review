from sklearn.model_selection import cross_val_score
import Tokenized_data as DATA_
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from collections import Counter
import time
start_time = time.time()

# -------------setting -------------------#
bnb = BernoulliNB()
mnb = MultinomialNB()
gnb = GaussianNB()
rfc = RandomForestClassifier(n_estimators=100)
rfc2 = RandomForestClassifier(n_estimators=500)
rfc3 = RandomForestClassifier(n_estimators=1000)
num = -5  # 감정변수 추가하면 -6 으로 변경
DATA = DATA_.resultlist[1:]
tokens = [word for data in DATA for word in data[0][:num]]  # Train 안에있는 정보들 중에서 단어들만 넣음// 틀릴수도 있음
selected_word_num = 3000 # 변경가능
while selected_word_num<5001: #s

    selected = [i[0] for i in Counter(tokens).most_common(selected_word_num)]  # 위에서 선택된 단어들 중 가장 흔한 것들만 모음

    XM = []
    XG = []
    XR = []
    y = []  # Training_sample 들의 진리값 저장



    for data in DATA:
        y.append(data[-1])  # 진리값 저장
        G = []
        M = []
        R = []
        length = len(data) + num
        length = length / 100
        for word in selected:
            value = data[0].count(word)
            M.append(value)  # length으로 나눠서 정규화..?
            G.append(value / length)  # length으로 나눠서 정규화..?
            if value:
                R.append(1)
            else:
                R.append(0)

        index = num
        while index != 0:
            value = data[0][index]
            M.append(value)
            G.append(value / length)
            if value:
                R.append(1)
            else:
                R.append(0)
            index += 1
        XM.append(M)
        XG.append(G)
        XR.append(R)

    print(selected_word_num)
    scores = cross_val_score(bnb, XR, y, cv=5)
    print("Bernoulli  ", scores.mean())
    scores = cross_val_score(mnb, XM, y, cv=5)
    print("Multinominal  ", scores.mean())
    scores = cross_val_score(gnb, XG, y, cv=5)
    print("Guassian  ", scores.mean())
    scores = cross_val_score(rfc, XR, y, cv=5)
    print("Random forest 100  ", scores.mean())
    scores = cross_val_score(rfc2, XR, y, cv=5)
    print("Random forest 500  ", scores.mean())
    scores = cross_val_score(rfc3, XR, y, cv=5)
    print("Random forest 1000  ", scores.mean())

    end_time = time.time()
    print("현재까지 :  %f 분" % ((end_time - start_time) / 60))
    print("\n\n")
    selected_word_num += 1000


end_time = time.time()
print("모든 프로세스: %f 분" % ((end_time - start_time) / 60))





