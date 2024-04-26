# 네이버 검색 API 예제 - 뉴스 검색
import os
import sys
import urllib.request
client_id = "n2zUeggmoMub8v0qgMsa"
client_secret = "Pq2qmHgwJ_"
encText = urllib.parse.quote("BTS")  # 검색할 텍스트를 URL에서 사용할 수 있도록 인코딩. 한글 검색어 때문임.
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url) # 요청 객체를 생성합니다. 이 객체는 요청을 보낼 URL을 가지고 있다.
# HTTP 요청 헤더에 클라이언트 ID와 시크릿을 추가합니다. 이는 인증을 위해 필요합니다.
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request) # 요청을 보내고 응답을 받는다.
rescode = response.getcode() # 응답 상태 코드 가져오기
if(rescode==200):
    response_body = response.read()  # 응답 본문을 읽고
    print(response_body.decode('utf-8')) # 바이트 스트림을 문자열로 디코딩하여 출력합니다.
else:
    print("Error Code:" + rescode) # 응답이 실패했을 경우, 에러 코드를 출력