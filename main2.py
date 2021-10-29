from bs4 import BeautifulSoup as bs
import time
from urllib import request as rq
import mariadb

for i in range(20):

    financeNewsURL = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=259&sid1=101&date=20211028&page={i+1}'

    financeNewsHTML = rq.urlopen(financeNewsURL)

    financeNewsText = bs(financeNewsHTML, 'html.parser')

    main_content = financeNewsText.find('div', {'id':'main_content'})

    dls = main_content.find_all('dl')

    for idx, dl in enumerate(dls):

        dts = dl.find_all('dt')

        # title, title_href

        title = ''
        title_href = ''
        imgURL = ''

        if len(dts) == 1:  # 사진이 없는 경우
            title = dts[0].find('a').string.strip()   # title # strip() : 공백제거
            title_href = dts[0].find('a').attrs['href']

        elif len(dts) == 2:  # 사진이 있는 경우
            imgURL = dts[0].find('a').find('img').attrs['src']
            title_href = dts[0].find('a').attrs['href']
            title = dts[1].find('a').string.strip()

            imgFileName = str(time.time()).replace('.', '') + '.jpg'  # 이미지 파일명

            rq.urlretrieve(imgURL, "C:/chh_server/project/newsPjt/src/main/webapp/resources/newimgs/" + imgFileName)

        # article
        lede = dl.find('span', {'class':'lede'}).string

        # publisher
        writing = dl.find('span', {'class':'writing'}).string


        print(f'imgURL[{idx}] : {imgURL}')
        print(f'title : {title}')
        print(f'title_href : {title_href}')
        print(f'lede : {lede}')
        print(f'writing : {writing}')



        # 예외처리 필수
        conn = mariadb.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='1234',
                               db='newsdb')

        cur = conn.cursor()

        n_title = title;     n_title_href = title_href;     n_photo_name = imgFileName
        n_article = lede;    n_publisher = writing

        if n_article == None:
            n_article = 'null'

        sql = 'INSERT INTO tbl_news(n_title, n_title_href, n_photo_name, n_article, n_publisher, n_reg_date) ' \
              'VALUES(?, ?, ? ,? ,?, NOW()) '

        cur.execute(sql, (n_title, n_title_href, n_photo_name, n_article, n_publisher))

        conn.commit()

        conn.close()