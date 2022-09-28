import requests
from pprint import pprint
import xmltodict
from bs4 import BeautifulSoup
import csv

API_KEY = ""

TrprId = "AIG20220000366720"
TrprDegr = "2"
TorgIdType = ["default", "facility_detail", "eqnm_detail"]
TorgId = TorgIdType[0]


### 구직자훈련과정 API
### 참고: https://www.hrd.go.kr/hrdp/ap/papco/PAPCO0700T.do

### 01. 목록
### 검색조건에 따라 훈련과정 목록을 표시
### 검색조건: 훈련지역 분류, 훈련분야 분류, 훈련유형, 훈련구분, 훈련 종류, 훈련시작일, 훈련과정 이름, 훈련기관 이름
### 검색 결과: 훈련과정별 콘텐츠, 수강비, 취업률, 훈련 이름 등...
URL01 = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=XML&authKey={API_KEY}"

### 02. 과정/기관정보
### 과정 ID/회차에 따라 과정/기관 정보를 표시
URL02 = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_2.jsp?returnType=XML&authKey={API_KEY}&srchTrprId={TrprId}&srchTrprDegr={TrprDegr}&outType=2&srchTorgId={TorgId}"
# print(URL02)
# result = requests.get(URL02)
# # print(result.text)
#
# xml = BeautifulSoup(result.text)
# inst_base_info = xml.select("inst_base_info > *")
# print(inst_base_info)

### 03. 훈련생 출결 정보
f = open("result1.csv", "w")
result_csv = csv.writer(f)

result_csv.writerow(["날짜", "출석상태", "이름", "요일", "입실시간", "퇴실시간"])





URL03 = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_4.jsp?returnType=XML&authKey={API_KEY}&srchTrprId={TrprId}&srchTrprDegr={TrprDegr}&outType=2&srchTorgId=undefined"
print(URL03)




raw = requests.get(URL03)
print(raw.elapsed)
result = BeautifulSoup(raw.text, 'html.parser')
# print(result)
atab_list = result.select("atab_list")

# <atendDe>20220425</atendDe>
# <atendSttusNm>출석</atendSttusNm>
# <cldrDe>20220425</cldrDe>
# <cstmrNm>강혜원</cstmrNm>
# <korDayNm>월</korDayNm>
# <levromTime>0000</levromTime>
# <lpsilTime>0000</lpsilTime>

for atab in atab_list:
    date = atab.select_one("cldrDe").text
    name = atab.select_one("cstmrNm").text
    weekday = atab.select_one("korDayNm").text
    try:
        status = atab.select_one("atendSttusNm").text
    except:
        status = ""
    try:
        enter = atab.select_one("levromTime").text
    except:
        enter = ""
    try:
        left = atab.select_one("lpsilTime").text
    except:
        left = ""

    print(date, status, name, weekday, enter, left)
    result_csv.writerow([date, status, name, weekday, enter, left])

f.close()


f2 = open("result.csv", "w")
result_csv2 = csv.writer(f2)
result_csv2.writerow(["출석일수", "생년월일", "수강생수", "훈련코드", "훈련회차", "훈련일수", "이름", "상태", "훈련타입", "휴가일수"])


URL04 = f"https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_4.jsp?returnType=XML&authKey={API_KEY}&srchTrprId={TrprId}&srchTrprDegr={TrprDegr}&outType=2&srchTorgId=student_detail"
print(URL04)

# <atendCnt>45</atendCnt>
# <lifyeaMd>19990820</lifyeaMd>
# <totTrneeCo>131</totTrneeCo>
# <tracseId>AIG20220000366720</tracseId>
# <tracseTme>1</tracseTme>
# <traingDeCnt>120</traingDeCnt>
# <trneeCstmrNm>강혜원</trneeCstmrNm>
# <trneeSttusNm>훈련중</trneeSttusNm>
# <trneeTracseSe>C0055</trneeTracseSe>
# <vcatnCnt>0</vcatnCnt>
raw = requests.get(URL04)
result = BeautifulSoup(raw.text, 'html.parser')
# print(result)
trne_list = result.select("trne_list")
for trne in trne_list:
    atendCnt = trne.select_one("atendCnt").text
    lifyeaMd = trne.select_one("lifyeaMd").text
    totTrneeCo = trne.select_one("totTrneeCo").text
    tracseId = trne.select_one("tracseId").text
    tracseTme = trne.select_one("tracseTme").text
    traingDeCnt = trne.select_one("traingDeCnt").text
    trneeCstmrNm = trne.select_one("trneeCstmrNm").text
    trneeSttusNm = trne.select_one("trneeSttusNm").text
    trneeTracseSe = trne.select_one("trneeTracseSe").text
    vcatnCnt = trne.select_one("vcatnCnt").text

    result_csv2.writerow([atendCnt, lifyeaMd, totTrneeCo, tracseId, tracseTme, traingDeCnt, trneeCstmrNm, trneeSttusNm, trneeTracseSe, vcatnCnt])
    print(atendCnt, lifyeaMd, totTrneeCo, tracseId, tracseTme, traingDeCnt, trneeCstmrNm, trneeSttusNm, trneeTracseSe, vcatnCnt)

f2.close()