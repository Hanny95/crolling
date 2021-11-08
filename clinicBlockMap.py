import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import rcParams, style
from matplotlib import font_manager, rc

printLog = True

data = pd.read_csv('./resources/clinicList.csv',
            index_col=0,
            encoding='CP949',
            engine='python')

if printLog:
    print(data.head())

new_data = pd.DataFrame(data, columns=['sido', 'gungu'])

if printLog:
    print(new_data.head())

# Date 컬럼 삭제 (인덱스로 설정되어있어서 reset 후 컬럼 삭제)
new_data = new_data.reset_index()
print(new_data)
new_data.drop('Date', axis=1, inplace=True)
new_data.columns = ['시도', '군구']
print(new_data)

if printLog:
    print(new_data.head())

addr_aliases = {'경기':'경기도', '경남':'경상남도', '경북':'경상북도', '충북':'충청북도',
                '서울':'서울특별시', '부산':'부산광역시', '대전':'대전광역시', '울산':'울산광역시',
                '충남':'충청남도', '전남':'전라남도', '전북':'전라북도', '광주':'광주광역시',
                '강원':'강원도', '대구':'대구광역시', '인천':'인천광역시',
                '세종':'세종특별자치시', '제주':'제주특별자치도'}

sido_all = new_data['시도'].apply(lambda v: addr_aliases.get(v, v))
gungu_all = new_data['군구'].unique()

if printLog:
    print(sido_all.unique())
    print(gungu_all)

new_data['시도군구'] = new_data.apply(lambda r:r['시도'] + ' ' + r['군구'], axis=1)

if printLog:
    print(new_data.head())

new_data['count'] = 0

if printLog:
    print(new_data.head())

address_group = pd.DataFrame(new_data.groupby(['시도', '군구', '시도군구'],
                                              as_index=False).count())
if printLog:
    print(address_group.head())

# 시도군구로 인덱스 설정
address_group = address_group.set_index("시도군구")
if printLog:
    print(address_group.head())


##### 행정구역별 인구수 데이터 ######

population = pd.read_excel('./resources/행정구역_시군구_별__성별_인구수_2.xlsx')

if printLog:
    print(f'population.head() : \n {population.head()}')

population = population.rename(columns={'행정구역(시군구)별(1)':'시도', '행정구역(시군구)별(2)':'군구'})

if printLog:
    print(f'population.head() : \n {population.head()}')

for element in range(0, len(population)):
    population['군구'][element] = population['군구'][element].strip()

population['시도군구'] = population.apply(lambda r:r['시도'] + ' ' + r['군구'], axis = 1)

if printLog:
    print(f'population.head()2 : \n {population.head()}')

population = population[population.군구 != '소계']
population = population.set_index('시도군구')

if printLog:
    print(f'population.head()3 : \n {population.head()}')

# address_group & population 결합

addr_population_merge = pd.merge(address_group, population,
                                 how='inner',
                                 left_index= True,
                                 right_index= True)

if printLog:
    print(f'addr_population_merge : \n {addr_population_merge.head()}')

clinic_population = addr_population_merge[['시도_x', '군구_x',
                                           'count', '총인구수 (명)']]

if printLog:
    print(f'clinic_population : \n {clinic_population.head()}')


# 컬럼 변경
clinic_population = clinic_population.rename(columns= {'시도_x':'시도',
                                                       '군구_x':'군구',
                                                       '총인구수 (명)':'인구수'})

clinic_count = clinic_population['count']

clinic_population['clinic_ratie'] = clinic_count.div(clinic_population['인구수'], axis=0)*100000

if printLog:
    print(f'clinic_population : \n {clinic_population.head()}')

## 블록맵으로 시각화 하기 ##

path = os.getcwd()

data_draw_korea = pd.read_csv(path+'./resources/data_draw_korea.csv',
                              index_col=0,
                              encoding='UTF-8',
                              engine='python')

if printLog:
    print(f'data_draw_korea : \n {data_draw_korea.head()}')

# 행정구역 이름 매핑하기

data_draw_korea['시도군구'] = data_draw_korea.apply(lambda r:r['광역시도'] + ' ' + r['행정구역'], axis=1)

data_draw_korea = data_draw_korea.set_index("시도군구")

if printLog:
    print(f'data_draw_korea : \n {data_draw_korea.head()}')

data_draw_korea_clinic_population_all = pd.merge(data_draw_korea, clinic_population,
                                                 how='outer',
                                                 left_index=True,
                                                 right_index=True)

if printLog:
    print(f'data_draw_korea_clinic_population_all : \n {data_draw_korea_clinic_population_all.head()}')


print(f'data_draw_korea : \n {data_draw_korea}' )

# 행정구역 블록 위치 x, y 정의
BORDER_LINES = [
    [(3, 2), (5, 2), (5, 3), (9, 3), (9, 1)], # 인천
    [(2, 5), (3, 5), (3, 4), (8, 4), (8, 7), (7, 7), (7, 9), (4, 9), (4, 7), (1, 7)], # 서울
    [(1, 6), (1, 9), (3, 9), (3, 10), (8, 10), (8, 9),
     (9, 9), (9, 8), (10, 8), (10, 5), (9, 5), (9, 3)], # 경기도
    [(9, 12), (9, 10), (8, 10)], # 강원도
    [(10, 5), (11, 5), (11, 4), (12, 4), (12, 5), (13, 5),
     (13, 4), (14, 4), (14, 2)], # 충청남도
    [(11, 5), (12, 5), (12, 6), (15, 6), (15, 7), (13, 7),
     (13, 8), (11, 8), (11, 9), (10, 9), (10, 8)], # 충청북도
    [(14, 4), (15, 4), (15, 6)], # 대전시
    [(14, 7), (14, 9), (13, 9), (13, 11), (13, 13)], # 경상북도
    [(14, 8), (16, 8), (16, 10), (15, 10),
     (15, 11), (14, 11), (14, 12), (13, 12)], # 대구시
    [(15, 11), (16, 11), (16, 13)], # 울산시
    [(17, 1), (17, 3), (18, 3), (18, 6), (15, 6)], # 전라북도
    [(19, 2), (19, 4), (21, 4), (21, 3), (22, 3), (22, 2), (19, 2)], # 광주시
    [(18, 5), (20, 5), (20, 6)], # 전라남도
    [(16, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10)], # 부산시
]


# 블록맵의 블록에 데이터 매핑하고 색 표시
def draw_blockMap(blockedMap, targetData, title, color):

    whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + min(blockedMap[targetData])

    datalabel = targetData

    vmin = min(blockedMap[targetData])
    vmax = max(blockedMap[targetData])

    mapdata = blockedMap.pivot(index='y', columns='x', values=targetData)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)


    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=color, edgecolor='#aaaaaa', linewidth=0.5)


    # 지역 이름 표시
    try:
        for idx, row in blockedMap.iterrows():

            annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다. (중구, 서구)
            # if row['광역시도'].endswith('시') and not row['광역시도'].startswith(''):
            if row['광역시도'].endswith('시') and row['광역시도'].endswith('도'):
                dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
                if len(row['행정구역']) <= 2:
                    dispname += row['행정구역'][-1]
            else:
                dispname = row['행정구역'][:-1]

            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 9.5, 1.5
            else:
                fontsize, linespacing = 11, 1.2

            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5),
                         weight='bold',
                         fontsize=fontsize,
                         ha='center',
                         va='center',
                         color=annocolor,
                         linespacing=linespacing)

        # 시도 경계 그린다.
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=4)

        plt.gca().invert_yaxis()
        # plt.gca().set_aspect(1)
        plt.axis('off')

        # 바 만들기기
        cb = plt.colorbar(shrink=1, aspect=10)
        cb.set_label(datalabel)

        plt.tight_layout()

        plt.savefig('./resources/clinicBlockMap_' + targetData + '.png')

        plt.show()

    except Exception as e:
        print(e)

draw_blockMap(data_draw_korea_clinic_population_all,
              'count',
              '행정구역별 코로나 선별진료소 수',
              'Blues')

draw_blockMap(data_draw_korea_clinic_population_all,
              'clinic_ratie',
              '행정구역별 인구수 대비 코로나 선별진료소 비율',
              'Reds')