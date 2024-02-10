from playwright.sync_api import sync_playwright
import time
from requests import get
from bs4 import BeautifulSoup
import csv

# p = sync_playwright().start()

# broswer = p.chromium.launch()

# page = broswer.new_page()

# page.goto("https://www.oliveyoung.co.kr/store/main/getBestList.do?t_page=%ED%99%88&t_click=GNB&t_gnb_type=%EB%9E%AD%ED%82%B9&t_swiping_type=N")

# time.sleep(3)

# content = page.content()

# p.stop()


from tkinter import *            # tkinter 라이브러리에 모든 함수를 사용하겠다.
root = Tk()                      # root라는 창을 생성
root.geometry("600x400")       # 창 크기설정
root.title("yeachan_yeachan")    # 창 제목설정
root.option_add("*Font","맑은고딕 25") # 폰트설정
root.resizable(False, False)  # x, y 창 크기 변경 불가

count = 0                    # 변수 생성

def btnpress():              # 함수 btnpress() 정의
    global count             
    count += 1
    btn.config(text = count)

btn = Button(root)           # root라는 창에 버튼 생성
btn.config(text=count)       # 버튼 내용
btn.config(width=10)         # 버튼 크기
btn.config(command=btnpress) # 버튼 기능 (btnpress() 함수 호출)
btn.pack()                   # 버튼 배치

root.mainloop()              # 창 실행



baseURL = get("https://www.oliveyoung.co.kr/store/main/getBestList.do?t_page=%ED%99%88&t_click=GNB&t_gnb_type=%EB%9E%AD%ED%82%B9&t_swiping_type=N")

def function():
    soup = BeautifulSoup(baseURL.text, "html.parser")
    cats = soup.select(".common-menu li")

    prods_db = []

    for cat in cats:
        if cat.find("button"):
            num = 1
            catNo = cat.find("button")["data-ref-dispcatno"]
            catName = cat.find("button").text
            print(catNo)
            resultURL = get(f"https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo={catNo}&pageIdx=1&rowsPerPage=8&t_page=랭킹&t_click=판매랭킹_{catName}")

            # p2 = sync_playwright().start()
            # broswer = p2.chromium.launch()
            # page = broswer.new_page()   
            # page.goto(resultURL)
            # time.sleep(3)
            # content = page.content()

            resultSoup = BeautifulSoup(resultURL.text, "html.parser")
            prods = resultSoup.find_all("div", class_="prd_info")

            for prod in prods:
                rank = num
                brand = prod.find("span", class_="tx_brand").text
                prod_name = prod.find("p", class_="tx_name").text
                category = prod.find("button", class_="cartBtn")["data-ref-goodscategory"]
                link = prod.find('a')['href']
                num = num + 1
                prod = {
                    "랭킹 카테고리": catName,
                    "순위": rank,
                    "브랜드명": brand,
                    "상품명": prod_name,
                    "제품 카테고리": category,
                    "링크": link
                }
                prods_db.append(prod)
            else:
                print("over")

    # p.stop()

    file = open("oy_prods.csv", "w")
    writer = csv.writer(file)
    
    writer.writerow([f"{today} 올리브영 랭킹"])
    writer.writerow(["랭킹 카테고리","순위", "브랜드명", "상품명", "제품 카테고리", "링크"])

    for prod in prods_db:
        writer.writerow(prod.values())