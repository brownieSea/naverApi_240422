import webbrowser
import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from naverSearchAPI import *

form_class = uic.loadUiType("ui/ui_nord.ui")[0]  #index 0 = 외부에서 가져올때, index 1 = 내부(파이썬)에서 만든 ui를 가져올 때

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("네이버 뉴스 검색 앱")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.statusBar().showMessage("Naver News Search Application v1.0")

        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.input_keyword.returnPressed.connect(self.searchBtn_clicked)
        self.result_table.doubleClicked.connect(self.link_doubleClicked) # 테이블의 항목이 더블클릭되면 함수 호출

        #self.select_nord.currentIndexChanged.connect(self.nord_selected)

    def searchBtn_clicked(self):
        nord = self.select_nord.currentText().lower()
        keyword = self.input_keyword.text()  # 사용자가 입력한 검색어 가져오기
        if keyword == "":
            QMessageBox.warning(self, "입력오류\n검색어는 필수 입력사항입니다")
        else:
            naverApi = NaverApi()  # import 된 naverSearchAPI 클래스로 객체 생성
            searchResult = naverApi.getNaverSearch(nord, keyword, 1, 20)

            if nord == 'news':
                newsResult = searchResult['items']  # json으로 응답온 텍스트 중 뉴스 내용만 저장
                self.outputTable(newsResult)
            elif nord == 'blog':
                blogResult = searchResult['items']  # json으로 응답온 텍스트 중 뉴스 내용만 저장
                self.outputTable(blogResult)
            else:
                cafeResult = searchResult['items']  # json으로 응답온 텍스트 중 뉴스 내용만 저장
                self.outputTable(cafeResult)

    def outputTable(self, searchResult):  # 뉴스  검색 결과를 테이블 위젯에 출력하는 함수
        nord = self.select_nord.currentText().lower()
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)  # json 값 가져올때 무조건 넣는다
        self.result_table.setColumnCount(3)  # 출력되는 테이블을 3열로 설정
        self.result_table.setRowCount(len(searchResult))  # 출력되는 테이블 행 수를 설정. 가변적인 경우가 많으므로 가져온 데이터의 갯수를 행으로 설정.

        # 테이블의 첫 행(열 이름 설정
        self.result_table.setHorizontalHeaderLabels(['Title', 'Link', 'Date'])
        self.result_table.setColumnWidth(0, 300) # 1열의 넓이 설정
        self.result_table.setColumnWidth(1, 190) # 2열의 넓이 설정
        self.result_table.setColumnWidth(2, 120) # 3열의 넓이 설정

        #테이블에 출력되는 검색결과를 클릭시 수정 안되게 하는 기능 추가
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, article in enumerate(searchResult):  # enumerate 는 index 값을 i 에 반환한다  i = 0~게시글수
            # newsTitle = article['title'] # 뉴스 제목
            # newsTitle = article.replace('&quot', '').replace(';','').replace('<b>','').replace('</b>','')
            # newsDate = article['pubDate']  # 뉴스게시일
            # newsDate = newsDate[0:25]

            # html 코드 제거해서 반환하는 함수
            def remove_html_tags(text):
                clean = re.compile('<.*?>')
                return re.sub(clean, '', text)

            articleTitle = article['title']
            articleTitle = remove_html_tags(articleTitle)  # html 코드 제거
            if nord == 'news':
                articleLink = article['originallink']  # 뉴스 링크
                str_date = article['pubDate']
                articleDate = datetime.datetime.strptime(str_date, '%a, %d %b %Y %H:%M:%S %z')
                articleDate = articleDate.strftime('%y.%m.%d(%a) %H:%M:%S')
            elif nord == 'blog':
                articleLink = article['link']  # blog 링크
                articleDate = article['postdate']

            else:
                self.result_table.setHorizontalHeaderLabels(['Title', 'Link', 'Cafe Name'])
                articleLink = article['link']  # blog 링크
                articleDate = article['cafename']

            self.result_table.setItem(i, 0, QTableWidgetItem(articleTitle))
            self.result_table.setItem(i, 1, QTableWidgetItem(articleLink))
            self.result_table.setItem(i, 2, QTableWidgetItem(articleDate))

    def link_doubleClicked(self):  # 링크를 더블클릭하면 호출되는 함수
        selectedRow = self.result_table.currentRow() # 더클클릭하여 선택되어 있는 행의 인덱스 반환
        selectedLink = self.result_table.item(selectedRow, 1).text()  # 더블클릭한 셀의 text를 반환
        webbrowser.open(selectedLink)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())