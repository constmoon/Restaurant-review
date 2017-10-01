import trainlist_v6 as train , testlist_v6 as test, train_extra6 as trainex, test_extra6 as testex
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from collections import Counter
import time,pickle

start_time = time.time()


Train=train.resultlist[1:]
Test=test.resultlist[1:]
Trainex=trainex.resultlist[1:]
Testex=testex.resultlist[1:]

tokens = [t for d in Train for t in d[0]]

selected = [i[0] for i in Counter(tokens).most_common(5000)]
#selected = [x for x in selected if x not in trash]
#trash = ['/Pn', '.*Pn', '."Pn','//Pn','/**Pn','**Pn']
###


X=[]
y=[]

for i in Train:
    y.append(i[-1])
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)

for i in range(len(X)):
    X[i] = X[i] + Trainex[i]

'''
with open("restname_X.txt", "wb") as fp:
    pickle.dump(X,fp)
fp.close()

with open("restname_y.txt", "wb") as fp:
    pickle.dump(y,fp)
fp.close()
'''
###


with open("restname_X.txt", "rb") as fp:
    X= pickle.load(fp)
fp.close()

with open("restname_y.txt", "rb") as fp:
    y = pickle.load(fp)
fp.close()



clf = MultinomialNB()
clf.fit(X, y)
X=[]
y=[]
for i in Test:
    y.append(i[-1])
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)
for i in range(len(X)):
    X[i] = X[i] + Testex[i]
print('5000 ')
print( clf.score(X,y))

'''
#-------------------------
selected = [i[0] for i in Counter(tokens).most_common(4000)]
X=[]
for i in Train:
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)
for i in range(len(X)):
    X[i] = X[i] + Trainex[i]
clf2 = MultinomialNB()
clf2.fit(X, y)
X=[]
yy=[]
for i in Test:
    yy.append(i[-1])
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)

for i in range(len(X)):
    X[i] = X[i] + Testex[i]
print('4000 ')
print( clf2.score(X,yy))

#----------------------
selected = [i[0] for i in Counter(tokens).most_common(5000)]
selected = selected[500:5000]
X=[]

for i in Train:
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)

for i in range(len(X)):
    X[i] = X[i] + Trainex[i]
clf3 = MultinomialNB()
clf3.fit(X, y)
X=[]
yy=[]
for i in Test:
    yy.append(i[-1])
    temp = []
    for k in selected:
        temp.append(i[0].count(k))
    X.append(temp)

for i in range(len(X)):
    X[i] = X[i] + Testex[i]
print('500-5000 ')
print(clf3.score(X,yy))
#-------------------
'''


label= selected + ['Phone','NoMapNoPhone','Photo','Imoticon','Restname','City' ]
coef=clf.coef_[0]
informative=[]
for i in range(len(coef)):
    informative.append((coef[i],label[i]))

for i in informative:
    print(i)


print("----------------------------\n\n\n\n")
informative.sort(key=lambda x: x[0])
for i in informative:
    print(i)



end_time = time.time()
print("모든 프로세스: %f 분" % ((end_time - start_time) / 60))





