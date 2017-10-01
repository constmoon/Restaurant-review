from bs4 import BeautifulSoup
import time,requests,re
from konlpy.tag import Twitter
start_time = time.time()


#쓸데없는 스크립트 제거함수
def onlytext(string):
    string=string.replace('<div align="center">', ' / ')
    #string = string.replace('<br/>', ' / ')
    string = string.replace('<br>', ' / ')
    #string = string.replace('<p>', ' / ' )
    #string = string.replace('</p>', ' / ')

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
        output =string
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

#공백제거함수
def enter_tab(string):
    output = string.replace("\t", " ")
    output = output.replace("\n", " ")
    output = output.replace("\r", " ")
    return output


##----seting-----##

# fake 로 입력되지만 실제론 real인 링크들... 추가해야함
errorset={
'http://m.blog.naver.com/syukoring/220943748599','http://m.blog.naver.com/ktr0520/220699589679',
'http://m.blog.naver.com/ktr0520/220699589679', 'http://m.blog.naver.com/leenoh1004/220774329866',
'http://m.blog.naver.com/sarmter/220634012962', 'http://m.blog.naver.com/sky5891/220814997305',
'http://m.blog.naver.com/bluej6969/220128328020','http://m.blog.naver.com/sky5891/220814997305',
'http://m.blog.naver.com/mih2000/110141783718','http://m.blog.naver.com/825kyr/220722322579',
'http://m.blog.naver.com/jjunjooh/220658652901','http://m.blog.naver.com/aurryburry/220213474987',
'http://m.blog.naver.com/giantbabysh/220778779809','http://m.blog.naver.com/momthetable/220942882429',
'http://m.blog.naver.com/muhairsalon/220789399221','http://m.blog.naver.com/jwramhouse/220465325124',
'http://m.blog.naver.com/dorysister/220937325434','http://m.blog.naver.com/gjeownd07/220882090460',
'http://m.blog.naver.com/propsing/220260125444','http://m.blog.naver.com/propsing/220152282129',
'http://m.blog.naver.com/haniswell/220462980189','http://m.blog.naver.com/jjw5650/220943506037',
'http://m.blog.naver.com/sizyoung/220744547891','http://m.blog.naver.com/paksangman10/221014575879',
'http://m.blog.naver.com/13100m/220188253945','http://m.blog.naver.com/nicesadari/220882915013',
'http://m.blog.naver.com/sjin569/220659341521','http://m.blog.naver.com/daheeee_l/221040292735',
'http://m.blog.naver.com/itsukayuki/221055875733',  'http://m.blog.naver.com/itsukayuki/221047685996',
'http://m.blog.naver.com/24hour_man/221022257330','http://m.blog.naver.com/6020mk/221046931581',
'http://m.blog.naver.com/slivecall/221001215189', 'http://m.blog.naver.com/aftm2030/220840929120',
'http://m.blog.naver.com/leeso2014/220541196914','http://m.blog.naver.com/ugogirl1219/220318780377',
'http://m.blog.naver.com/rushtothesky/220871075837'}

page = 67#67
url_set = set({}) # 크롤하는 모든 url 모음 set. fake, real, mix간 중복이 없기 위함
##-----fake------##

list1=[]
keywordlist = ["맛집 \"제공 받아\"", "맛집 \"제공 받고\"", "맛집 \"후원 받아\"", "맛집 \"후원 받고\"", "맛집 \"소정의\" \"받고\"", "맛집 \"소정의\" \"받아\"",
               "맛집 \"원고료를\"", "맛집 \"지원 받고\"", "맛집 \"지원 받아\"", "맛집 \"업체로부터\""]
for keyword in keywordlist:
    start = 1

    while start <= page * 15:
        url = "https://m.search.naver.com/search.naver?where=m_blog&query=" + keyword + "&start=%d" % (start)  # blog

        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, "lxml")
        for link in soup.find_all("a", class_="total_wrap"):
            temp=link.get("href")
            if "http://m.blog.naver.com" in temp:
                list1.append(temp)
        start += 15
    datastring = ''
print(len(list1))

nlp = Twitter()  # Twitter 라이브러리 사용
list1 = list(set(list1)) # 중복된 url 제거하는 원시적인 코드...
negative=('아니다','절대','검색','그냥','듯','같다','대부분','어디서', '그렇다' ,'전혀')
regex = r'[가-힣, \s ]+'
data = open('reviews_rawdata_4.txt', 'w', encoding='UTF-8')
for url in list1:
    try:
        datastring = ''
        source_code = requests.get(url, timeout=5)
        soup = BeautifulSoup(source_code.text, "lxml")

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

            #블로그 본문 내용 찾기
            if soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area"):
                article = soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area")[0]
            else:
                article = soup.find_all("div", class_="post_ct")[0]

            # 지도 javascript code 삭제, 정보 저장

            restname=''
            temp = soup.find_all("span", class_="_mapInfo")  ##네이버 지도1
            temp2 = soup.find_all('a', class_='se_map_link __se_link')  ##네이버 지도2
            if temp:
                restname= str(soup.find_all("a", class_= "tit"))
                restname=onlytext(restname)
                temp[0].decompose()

            elif temp2:
                restname = str( soup.find_all("div", class_ = "se_title" )[0] )
                restname = onlytext(restname)
                temp2[0].decompose()


            # 사진,이모티콘 정보 저장
            photo = 0
            temp = soup.find_all("span", class_="_img")  # 사진테그1
            temp_= soup.find_all("img", class_="fx")  # 사진테그1-2
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
            for Searchekyword in ["제공받아", "제공 받고", "제공받고", "후원 받아", "후원받아", "후원 받고", "후원받고", "소정의", "원고료를", "지원 받고", "지원받고", "지원 받아", "지원받아", "업체로부터","제공 받아"]:
                KWindex = mainarticle.find(Searchekyword)
                if KWindex != -1:
                    for a in range(KWindex,-1,-1):
                        if not re.findall(regex, mainarticle[a]):
                            index1 = a
                            break
                    for a in range(KWindex,len(mainarticle)):
                        if not re.findall(regex, mainarticle[a]):
                            index2 =a
                            break

                    sentence = mainarticle[index1+1:index2]
                    sentence = [x[0] for x in nlp.pos(sentence, norm=True, stem=True)]
                    for neg in negative:
                        if neg in sentence:
                            errorset.add(url)
                            print(url, sentence)
                            break
                    break

            if url in errorset:
                datastring = datastring + "real\t%s\t%s\t%s\t%d\t%d\t%s\n" % (url, enter_tab(post_title), mainarticle[:index1+1] + ' ' + mainarticle[index2+1:], photo, imo, restname)
            else:
                url_set.add(url)
                datastring = datastring + "fake\t%s\t%s\t%s\t%d\t%d\t%s\n" % (url, enter_tab(post_title), mainarticle[:index1+1] + ' ' + mainarticle[index2+1:], photo, imo, restname)
            data.write(datastring)
    except :
        print("error at fake")
print(len(url_set))



##-----real------##
keywordlist = ["맛집 \"제 돈\"", "맛집 \"제돈\"", "맛집 \"오빠가 사준\"", "맛집 \"내돈\"", "맛집 \"내 돈 \"", "맛집 \"개인 사비\""]
list1=[]
for keyword in keywordlist:
    start = 1

    while start <= page * 15:
        url = "https://m.search.naver.com/search.naver?where=m_blog&query=" + keyword + "&start=%d" % (start)  # blog
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, "lxml")
        for link in soup.find_all("a", class_="total_wrap"):
            temp=link.get("href")
            if "http://m.blog.naver.com" in temp:
                list1.append(temp)
        start += 15
    datastring = ''

list1 = list(set(list1))  # 중복된 url 제거하는 원시적인 코드...
for url in list1:
    try:
        if url not in url_set:
            datastring = ''
            source_code = requests.get(url, timeout=5)
            soup = BeautifulSoup(source_code.text, "lxml")

            # 글 제목 태그 정보
            if soup.find_all("h3", class_="tit_h3"):
                title = soup.find_all("h3", class_="tit_h3")[0]
            else:
                title = soup.find_all("h3", class_="se_textarea")[0]
            post_title = ""
            for i in range(len(title.contents)):
                post_title = post_title + str(title.contents[i])

            # 글 제목에 맛집이 포함될 때
            if "맛집" in post_title:
                # 블로그 본문 내용 찾기
                if soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area"):
                    article = soup.find_all("div", class_="se_component_wrap sect_dsc __se_component_area")[0]
                else:
                    article = soup.find_all("div", class_="post_ct")[0]

                # 지도 javascript code 삭제, 정보 저장
                restname=''
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

                post_article = str(article)
                mainarticle = onlytext(post_article)
                index1 =0
                index2 =0
                for Searchekyword in ["제돈", "제 돈", "내돈", "내 돈", "오빠가 사준", "오빠가사준", "개인사비", "개인 사비"]:
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
                        #print(url, sentence)

                datastring = datastring + "real\t%s\t%s\t%s\t%d\t%d\t%s\n" % (url, enter_tab(post_title), mainarticle[:index1 + 1] + ' ' + mainarticle[index2+1:], photo, imo,restname)
                data.write(datastring)
                url_set.add(url)
    except:
        print("error at real")
print(len(url_set))


data.close()
end_time = time.time()
print("모든 프로세스: %f 분" % ((end_time - start_time) / 60))
