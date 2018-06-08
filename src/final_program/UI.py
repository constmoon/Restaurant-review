import sys
import GUI_backend

from tkinter import *

from bs4 import BeautifulSoup
import time, requests, re
from konlpy.tag import Twitter

start_time = time.time()


def analysis():
    blog_URL = getURL.get()  # URL을 받는것.
    # URL 을 타고 크롤링을 해서

    croll(blog_URL)

    # 진위여부를 판단해



    # 결과가 참 거짓 여부에 따라 TRUE, FALSE 문자열로 넘겨준다.
    TF = int(GUI_backend.backend())
    print(TF)
    result_pop(TF)
    return


def info():
    new_win = Tk()
    new_win.title("Information")
    new_win.geometry("850x700")
    sen = "0.1.0 ver. \n\n 해당 서비스는 기계학습을 통해 만들어진 리뷰 판별 모델을 이용하여 리뷰를 분석합니다.\n\n\n 1. 진짜 리뷰와 가짜 리뷰 글이 정말로 차이가 있나요?\n저희는 이를 검증하기 위해 네이버 블로그 중 맛집에 관련된 포스팅을 수집했습니다.\n수집한 포스팅은 총 11510개로 진짜 리뷰는 5368, 거짓 리뷰는 5782개였습니다.\n\n수집 리뷰의 판별 방법은 다음과 같습니다.\n\n진짜 리뷰 : “사비로 먹었다”, “내 돈으로 직접” 등의 내용을 포함\n가짜 리뷰 : “업체로부터 금전적 지원”, “후원을 받았다”, “원고료를 지원 받았다“ 등의 내용을 포함\n\n이렇게 수집한 데이터를 분석한 결과, 두 집단 간 통계적으로 유의미한 차이가 있음을 확인했습니다.\n\n\n2. 기계학습이 궁금해요.\n\n기계학습은 인공지능의 한 분야로 사람이 학습하듯 \n컴퓨터에게 수많은 데이터를 주고 학습하게 함으로써 새로운 지식을 얻어내도록 합니다.\n\n기계학습을 위한 방법론은 굉장히 다양하지만 본 서비스에서는 총 5가지의 알고리즘을 사용했으며 이는 다음과 같습니다.\n1. SVM(linear)\n2. SVM(ref)\n3. KNN\n4. Naive Bayes\n5. Random Forest\n\n각각의 알고리즘이 개별적인 리뷰 판별 모델을 만들고 우리의 서비스는 이를 종합하여 결과를 제공합니다.\n해당 리뷰 판별기는 평균적으로 80%의 정확도를 보입니다.\n\n"

    info_sen = Label(new_win, text=sen)
    info_sen.grid(padx=0, pady=0)
    return


def result_pop(TF):  # 새로운 창을 띄우기!
    new_win = Tk()
    new_win.title("결과창 두근두근!")
    new_win.geometry("300x150")

    if TF == True:
        result_sen = Label(new_win, text="참일 확률이 높습니다", font="Helvetica -20 bold")
    elif TF == False:
        result_sen = Label(new_win, text="거짓일 확률이 높습니다", font="Helvetica -20 bold")
    elif TF == "WURL":
        result_sen = Label(new_win, text="잘못된 URL 입니다", font="Helvetica -20 bold")
    else:
        result_sen = Label(new_win, text="ERROR", font="Helvetica -20 bold")

    result_sen.grid(padx=60, pady=40)
    return


# 쓸데없는 스크립트 제거함수
def onlytext(string):
    string = string.replace('<div align="center">', ' / ')
    # string = string.replace('<br/>', ' / ')
    string = string.replace('<br>', ' / ')
    # string = string.replace('<p>', ' / ' )
    # string = string.replace('</p>', ' / ')

    length = len(string)
    tagend = 0
    count = 0
    flag = 0
    if '<' in string:
        output = ''
        for i in range(length):

            if tagend == 1 and string[i] == "<":
                output = output + string[flag:flag + count]
                tagend = 0

            elif tagend == 1 and i + 1 == length:
                output = output + string[flag:flag + count + 1]
                tagend = 0

            elif string[i] == ">":
                flag = i + 1
                count = 0
                tagend = 1

            elif string[i] != "<":
                count += 1
    else:
        output = string
    output = output.replace('[', ' ')
    output = output.replace(']', ' ')
    output = output.replace('\ufeff;', ' ')
    output = output.replace('\u200b', ' ')
    output = output.replace('&nbsp;', ' ')
    output = output.replace('&gt;', ' / ')
    output = output.replace('&lt;', ' / ')
    output = output.replace('\xa0', ' ')
    output = output.replace("\t", " / ")
    output = output.replace("\n", " / ")
    output = output.replace("\r", " / ")
    return output


# 공백제거함수
def enter_tab(string):
    output = string.replace("\t", " ")
    output = output.replace("\n", " ")
    output = output.replace("\r", " ")
    return output


def croll(urlinput):
    # url_set = set({}) # 크롤하는 모든 url 모음 set. fake, real, mix간 중복이 없기 위함
    ##-----크롤링------##

    # list1=[]
    keywordlist = ["맛집 \"제공 받아\"", "맛집 \"제공 받고\"", "맛집 \"후원 받아\"", "맛집 \"후원 받고\"", "맛집 \"소정의\" \"받고\"",
                   "맛집 \"소정의\" \"받아\"",
                   "맛집 \"원고료를\"", "맛집 \"지원 받고\"", "맛집 \"지원 받아\"", "맛집 \"업체로부터\""]

    datastring = ''

    # urlinput="http://blog.naver.com/jys2432176/221156543724"

    # print(len(list1))



    nlp = Twitter()  # Twitter 라이브러리 사용
    # list1 = list(set(list1)) # 중복된 url 제거하는 원시적인 코드...
    negative = ('아니다', '절대', '검색', '그냥', '듯', '같다', '대부분', '어디서', '그렇다', '전혀')
    regex = r'[가-힣, \s ]+'
    data = open('tempdata.txt', 'w', encoding='UTF-8')

    if "m.blog.naver.com" in urlinput:
        url = urlinput
    elif "blog.naver.com" in urlinput:
        where = urlinput.find("blog")
        url = "http://m." + urlinput[where:]
    else:
        # print("Wrong URL")
        result_pop("WURL")
        sys.exit(1)

    '''
    http://blog.naver.com/sldkfjalskdfj
    blog.naver.com/sdlkfjlk
    '''

    try:
        datastring = ''
        source_code = requests.get(url, timeout=5)
        soup = BeautifulSoup(source_code.text, "html.parser")
        # 글 제목 태그 정보
        if soup.find_all("h3", class_="tit_h3"):
            title = soup.find_all("h3", class_="tit_h3")[0]
        else:
            title = soup.find_all("h3", class_="se_textarea")[0]
        post_title = ""
        for i in range(len(title.contents)):
            post_title = post_title + str(title.contents[i])
            # 글 제목에 맛집이 포함될 때
        if "맛집" in post_title and "위드블로그" not in post_title and "홍보" not in post_title and "광고" not in post_title and "앱" not in post_title and "어플" not in post_title:
            # 블로그 본문 내용 찾기
            if soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area"):
                article = soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area")[0]
            else:
                article = soup.find_all("div", class_="post_ct")[0]
                # 지도 javascript code 삭제, 정보 저장
            restname = ''
            temp = soup.find_all("span", class_="_mapInfo")  ##네이버 지도1
            temp2 = soup.find_all('a', class_='se_map_link __se_link')  ##네이버 지도2
            if temp:
                restname = str(soup.find_all("a", class_="tit"))
                restname = onlytext(restname)
                temp[0].decompose()
            elif temp2:
                restname = str(soup.find_all("div", class_="se_title")[0])
                restname = onlytext(restname)
                temp2[0].decompose()
                # 사진,이모티콘 정보 저장
            photo = 0
            temp = soup.find_all("span", class_="_img")  # 사진테그1
            temp_ = soup.find_all("img", class_="fx")  # 사진테그1-2
            temp2 = soup.find_all('img', class_='se_mediaImage __se_img_el')  # 사진테그2
            if temp or temp_:
                photo = len(temp) + len(temp_)
            elif temp2:
                photo = len(temp2)
            imo = 0
            temp = soup.find_all('img', class_='_sticker_img')  # 이모티콘
            temp2 = soup.find_all('img', class_='__se_img_el')  # 사진 + 이모티콘
            if temp:
                imo = len(temp)
            elif temp2:
                imo = len(temp2) - photo
                # 데이터 클렌징
            post_article = str(article)
            index1 = 0
            index2 = 0
            mainarticle = onlytext(post_article)
            for Searchekyword in ["제공받아", "제공 받고", "제공받고", "후원 받아", "후원받아", "후원 받고", "후원받고", "소정의", "원고료를", "지원 받고",
                                  "지원받고", "지원 받아", "지원받아", "업체로부터", "제공 받아", "제돈", "제 돈", "내돈", "내 돈", "오빠가 사준",
                                  "오빠가사준", "개인사비", "개인 사비"]:
                KWindex = mainarticle.find(Searchekyword)
                if KWindex != -1:
                    for a in range(KWindex, -1, -1):
                        if not re.findall(regex, mainarticle[a]):
                            index1 = a
                            break
                    for a in range(KWindex, len(mainarticle)):
                        if not re.findall(regex, mainarticle[a]):
                            index2 = a
                            break
                    sentence = mainarticle[index1 + 1:index2]
                    sentence = [x[0] for x in nlp.pos(sentence, norm=True, stem=True)]

                    '''                
                    for neg in negative:
                        if neg in sentence:
                            errorset.add(url)
                            print(url, sentence)
                            break
                    '''
                    # break

            datastring = datastring + "what\t%s\t%s\t%s\t%d\t%d\t%s\n" % (
            url, enter_tab(post_title), mainarticle[:index1 + 1] + ' ' + mainarticle[index2 + 1:], photo, imo, restname)
            data.write(datastring)
    except:
        print("error")
    # nt(len(url_set))




    data.close()
    end_time = time.time()
    print("모든 프로세스: %f 분" % ((end_time - start_time) / 60))


window = Tk()
window.title("Real_or_Fake")
window.geometry("550x350")

intro = Label(window, text="Service name", font="Helvetica -30 bold")
intro.grid(padx=175, pady=40)

intro2 = Label(window, text="맛집 리뷰가 진짜인지 거짓인지 확인해드립니다.")
intro2.grid()

intro3 = Label(window, text="* 네이버 블로그, 맛집 주제 리뷰의 주소를 넣어주세요.")
intro3.grid()

getURL = Entry(window, width=40)
getURL.grid(pady=12.5)

button = Button(window, text=" 확인 ", command=analysis)  # 클릭하면 analysis 실행
button.grid(pady=20)

help_but = Button(window, text=" Info ", command=info)  # 설명창을 띄우자. 확인 버튼과 나란히 두는 법 찾기.
help_but.grid()

window.mainloop()