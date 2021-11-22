import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



data = pd.read_csv('아파트_실거래가_2011-2020 (3).csv',
            encoding='cp949')

print(data)

data.rename(columns={'연도':'year',
                     '행정구역(동)':'area',
                     '1㎡당 가격':'price'},
            inplace=True)   # 원본데이터 변경해줌

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 12

plt.figure(figsize=(13, 13))

# print(data)
# condition = data['area'] == '개포동'
# print(data[condition])



xValues = data['year'].unique()
areaList = data['area'].unique()

for areaValue in areaList:
    condition = data['area'] == areaValue
    yValues = data[condition]['price']


    plt.plot(xValues, yValues,
             label=areaValue)

plt.legend(title='강남구 행정구역',
           loc='upper right',
           shadow = True)

plt.show()