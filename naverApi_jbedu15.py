import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from naverSearchAPI import *

form_class = uic.loadUiType("ui/ui.ui")[0]  #index 0 = 외부에서 가져올때, index 1 = 내부(파이썬)에서 만든 ui를 가져올 때

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("네이버 뉴스 검색 앱")
        self.setWindowIcon(QIcon("img/image20240426102037.png"))
        self.statusBar().showMessage("Naver News Search Application v1.0")
        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.input_keyword.returnPressed.connect(self.searchBtn_clicked)

    def searchBtn_clicked(self):
        keyword = self.input_keyword.text().strip()   #사용자가 입력한 검색 키워드 가져오기

        if keyword == "":
            QMessageBox.warning(self, "입력오류", "검색어는 필수 입력 사항입니다.")

        else:
            naverApi = NaverApi()   #import 된 naverSearchApi내의 naverapi 클래스로 객체 생성
            searchResult = naverApi.getNaverSearch("news", keyword, 1, 10)
            print(searchResult)
            newsResult = searchResult['items']
            self.outputTable(newsResult)

    def outputTable(self, newsResult):   #뉴스검색결과를 테이블위젯에 출력하는 함수
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(3)  #출력되는 테이블을 3열로 설정
        self.result_table.setRowCount(len(newsResult))  #출력되는 테이블의 행 갯수 설정
        #newsResult 내의 원소 개수 만큼 줄 개수를 설정

        # 테이블의 첫 행(열 이름) 설정
        self.result_table.setHorizontalHeaderLabels(["기사제목", "기사링크", "게시시간"])
        #각 칼럼의 넓이(length)지정 : 총 길이 620을 3등분
        self.result_table.setColumnWidth(0, 300)
        self.result_table.setColumnWidth(1, 200)
        self.result_table.setColumnWidth(2, 120)

        #테이블에 출력되는 검색결과 수정 금지 기능 추가
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)



        for i, news in enumerate(newsResult):   #i -> 0~9
            newsTitle = news['title']  #뉴스 제목
            newsLink = news['originallink'] #뉴스의 오리지널 url 링크
            newsDate = news['pubDate']  #뉴스 게시일
            newsDate = newsDate[0:25]

            self.result_table.setItem(i,0, QTableWidgetItem(newsTitle))
            self.result_table.setItem(i,1, QTableWidgetItem(newsLink))
            self.result_table.setItem(i,2, QTableWidgetItem(newsDate))
            print(65)









app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exit(app.exec_())

