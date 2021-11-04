from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def getBookStores(result):
    # 베스트셀러 홈페이지
    bookStoreURL = 'http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79'
    browser = webdriver.Chrome()
    browser.get(bookStoreURL)

    time.sleep(2)

    # for p in range(2, 31):
    for p in range(2, 28):
        bookGenre = browser.find_element(By.CSS_SELECTOR, f'#main_contents > div.box_sub_category.fixed_sub_category > ul > li:nth-child({p}) > a')
        bookGenre.click()

        for i in range(1, 21):

            try:
                bookTitleEle = browser.find_element(By.CSS_SELECTOR, f'#main_contents > ul > li:nth-child({i*6}) > div.detail > div.title > a > strong')
                bookAuthorEle = browser.find_element(By.CSS_SELECTOR, f'#main_contents > ul > li:nth-child({i*6}) > div.detail > div.author')
                bookPriceEle = browser.find_element(By.CSS_SELECTOR, f'#main_contents > ul > li:nth-child({i*6}) > div.detail > div.price > strong')



                bookTitle = bookTitleEle.text
                authorList = (bookAuthorEle.text).split('|')
                author = authorList[0].strip()
                publisher = authorList[1].strip()
                publishDate = authorList[2].strip()
                print(f'title : {bookTitle}')
                print(f'autohr : {author}')
                print(f'publishDate : {publishDate}')
                print(f'fublisher : {publisher}')
                print(f'price : {bookPriceEle.text}')

            except Exception as e:
                print(e)


                result.append([bookTitle] + [author] + [publisher] + [publishDate])

    return

def main():

    result = []

    getBookStores(result)

    bestBooks_tbl = pd.DataFrame(result, columns=('bookTitle', 'author', 'publisher', 'publishDate'))

    bestBooks_tbl.to_csv('./resources.bestBooks.csv', encoding='cp949', mode='w', index=True)



if __name__ == '__main__':
    main()

