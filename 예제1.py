### 서울 시민생활 데이터로 평일 외출이 적은 20~24세 남성 1인가구 집단 시각화하기

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

# 20~24세 남성 추출
data_tmp = data_merge[data_merge['연령대'] == 20][data_merge['성별'] == 1]

# 지도 시각화
fig = plt.figure()
data_tmp.plot(column='평일 외출이 적은 집단',
                 legend=True,
                 cmap='YlGn',
                 edgecolor='k',
                 legend_kwds={'label': '명'})
plt.axis('off')
plt.tight_layout()

# 지도 다운로드 및 표출
plt.savefig('예제1.png')
plt.show()