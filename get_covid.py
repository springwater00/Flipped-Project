#외부데이터 - 코로나 사용
#코로나 데이터는 공공데이터 포털에 있는 '보건복지부 코로나19 감염 현황＇ 을 사용함
#아래 코드를 이용하여 불러왔으며, 불러온 데이터를 엑셀 파일로 저장하여 엑셀에서 수정하여 사용하였음.
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
from datetime import datetime
import pandas as pd
today = datetime.now().strftime('%Y%m%d')   

serviceKey = 'RY8GwXEX5npt3x%2F4E6PWiOZmTFyd4IZBbmw5NtJtE4Jt8sQ2JvGO849mBoLwVGnThJ%2BlMv9PWs3DsFKtkluvww%3D%3D'  
params = {'ServiceKey':parse.unquote(serviceKey),   
            'startCreateDt':20200201,
            'endCreateDt':20210228}   

url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'

res = requests.get(url, params=params)
soup = bs(res.text, 'lxml')
response = {'seq': '고유번호',
              'statedt': '기준일',
              'statetime': '기준시간',
              'decidecnt': '확진자',
              'clearcnt': '격리해제',
              'examcnt': '검사진행',
              'deathcnt': '사망자',
              'carecnt': '치료중',
              'resutlnegcnt': '음성',
              'accexamcnt': '누적검사',
              'accexamcompcnt': '누적검사완료',
              'accdefrate': '누적확진률',
              'createdt': '등록일시',
              'updatedt': '수정'}

items = soup.find_all('item')

dic1 = dict(covid19=[])

for item in items:
    dic = {}
    for x in item:
        if x.name in set(response):
            dic[x.name] = x.text
    dic1['covid19'].append(dic)

#xml을 dictionary로 바꿔 리스트 원소로 추가
lst = []
for y in items:
    l = {}
    for x in y:
        l[x.name] = x.text
    lst.append(l)
lst

df = pd.DataFrame(lst)
df.columns = df.columns.map(response)
df.to_csv('covid19.csv')