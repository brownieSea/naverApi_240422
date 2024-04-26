from urllib.request import *
from urllib.parse import *
import json
import datetime

class NaverApi:
    # 응답결과 체크하는 함수
    def getRequestUrlCode(self, url):
        requestUrl = Request(url)

        client_id = "n2zUeggmoMub8v0qgMsa"
        client_secret = "Pq2qmHgwJ_"
        requestUrl.add_header("X-Naver-Client-Id", client_id)
        requestUrl.add_header("X-Naver-Client-Secret", client_secret)

        naverResult = urlopen(requestUrl) # 네이버에서 요청에 의한 응답 결과 반환
        if naverResult.getcode() == 200:  # 응답결과가 정상이면
            print(f"네이버 API 요청 정상 진행 - {datetime.datetime.now()}")
            return naverResult.read().decode('utf-8') # 결과를 utf-8로 인코딩해서 반환해라.
        else:
            print(f"네이버 API 요청 실패 - {datetime.datetime.now()}")
            return None # 응답결과가 비정상이면 아무것도 반환하지 않는다

    # url을 조합해서 결과값을 json으로 반환하는 만드는 함수
    def getNaverSearch(self, node, keyword, start, display):
        baseUrl = "https://openapi.naver.com/v1/search/"  # 네이버 api 기본 url
        #node = f"{node}"  # {node}.json 인데 json이 default 값이어서 생략 가능
        params = f"?query={quote(keyword)}&start={start}&display={display}"  # quote(keyword) 한글 검색어 처리

        url = baseUrl + node + params
        result = self.getRequestUrlCode(url)
        if result != None:  # 네이버에서 결과가 정상적으로 왔다면.
            return json.loads(result)  # json 형태로 네이버 결과값 반환
        else:
            print("네이버 응답 실패 : 에러발생!")
            return None