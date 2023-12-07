### 서울 시민생활 데이터로 휴일 외출이 적은 40대 1인가구 집단 시각화하기

# 필요한 모듈
# Window OS에서 geopanda 설치 오류가 발생하는 경우, 필수 의존성 패키지 설치를 확인
# https://geopandas.org/en/stable/getting_started/install.html
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 현재 작업 폴더로 디렉토리 변경
# 필요한 파일: 1인가구_관심집단.csv, 서울_행정동.shp
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 시각화 설정
mpl.rc('font', family='Malgun Gothic') # 한글 폰트 적용
mpl.rcParams["axes.unicode_minus"] = False # 마이너스 기호 깨짐 방지
plt.rcParams["figure.figsize"] = (20, 10) # 차트 사이즈 설정

# 행정동별 1인가구 데이터를 불러와서 컬럼 타입 통일
data = pd.read_csv('1인가구_관심집단.csv', encoding='cp949')
data['adm_cd'] = data['행정동코드'].astype(str)

# 행정동 shp 파일 불러와서 1인가구 데이터와 병합
geo = gpd.read_file('서울_행정동.shp')
df_geo = geo.iloc[:,[2,9]]
rdata = pd.merge(data, df_geo, on = 'adm_cd')
data_merge = gpd.GeoDataFrame(rdata, crs="EPSG:4326", geometry="geometry")

# 연령대별 병합: 20대(초기청년층), 30대(후기청년층), 40대(중년층), 50~64세(장년층), 65세 이상(노년층)
data_merge.loc[(data_merge['연령대'] == 25), '연령대'] = 20
data_merge.loc[(data_merge['연령대'] == 35), '연령대'] = 30
data_merge.loc[(data_merge['연령대'] == 45), '연령대'] = 40
data_merge.loc[(data_merge['연령대'] == 55), '연령대'] = 50
data_merge.loc[(data_merge['연령대'] == 60), '연령대'] = 50
data_merge.loc[(data_merge['연령대'] > 60), '연령대'] = 65

colname_ = list(data_merge.columns[5:17])
data_groupby = data_merge.groupby(["adm_cd",'연령대'])[colname_].sum()
data_groupby = data_groupby.reset_index()
data_groupby = pd.merge(data_groupby, df_geo, on = 'adm_cd')
data_groupby = gpd.GeoDataFrame(data_groupby, crs="EPSG:4326", geometry="geometry")

# 40대 추출
data_tmp = data_groupby[data_groupby['연령대']==40]

# 지도 시각화
fig = plt.figure()
data_tmp.plot(column='휴일 외출이 적은 집단',
                 legend=True,
                 cmap='YlGn',
                 edgecolor='k',
                 legend_kwds={'label': '명'})
plt.axis('off')
plt.tight_layout()

# 지도 다운로드 및 표출
plt.savefig('예제2.png')
plt.show()