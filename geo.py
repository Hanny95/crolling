import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def getData(result):

    dataURL = 'http://data.ex.co.kr/link/linkList?pn=1&linkId=1&serviceType=LOD&keyWord=&searchDayFrom=2014.12.01&searchDayTo=2019.12.23&CATEGORY=&GROUP_TR='

    driver = webdriver.Chrome()
    driver.get(dataURL)

    time.sleep(2)

    # 첫페이지 크롤링
    for n in range(11):
        icNameCla = driver.find_element(By.CSS_SELECTOR, '#\30  > td.ICNAME')
        routeNameCla = driver.find_element(By.CSS_SELECTOR, '#\30  > td.ROUTENAME')

        icName = icNameCla.text
        routeName = routeNameCla.text



        print(f'icName : {icName} \t routeName : {routeName}')


    # 2-51 페이지 크롤링
    # for i in range(1, 51):
    #
    #     try:
    #         nextBtn = driver.find_element(By.CSS_SELECTOR, '#pagenation > li.next > a')
    #         driver.execute_script('arguments[0].click()', nextBtn)
    #
    #         time.sleep(1)
    #
    #         for j in range(1, 7):
    #
    #             storeInfoEle = driver.find_element(By.CSS_SELECTOR, f'#shopInfo > tr:nth-child({j}) > td:nth-child({1})')
    #             storeAddressEle = driver.find_element(By.CSS_SELECTOR, f'#shopInfo > tr:nth-child({j}) > td.al > a')
    #
    #             storeList = storeInfoEle.text.split()
    #             storeName = storeList[0].strip()
    #             storePhone = storeList[2].strip()
    #             storeAddress = storeAddressEle.text
    #
    #             print(f'storeName : {storeName} \t storePhone : {storePhone} \t storeAddress : {storeAddress}')
    #
    #             result.append([storeName] + [storePhone] + [storeAddress])
    #
    #             if i == 50:
    #                 break




    #     except Exception as e:
    #         print(e)
    #
    # return




def main():

    result = []

    getData(result)
#
#     eider_tbl = pd.DataFrame(result, columns=('StoreName', 'Phone', 'Address'))
#
#     eider_tbl.to_csv('./resources/eiderInfo.csv', encoding='cp949', mode='w', index=True)
#

if __name__ == '__main__':
    main()