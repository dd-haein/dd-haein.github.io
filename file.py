import csv
from datetime import datetime

def save_to_file(file_name, prods):
    today = datetime.today().strftime("%Y/%m/%d")
    file = open(f"{today} 올리브영 랭킹.csv", "w")
    writer = csv.writer(file)
    
    writer.writerow([f"{today} 올리브영 랭킹"])
    writer.writerow(["랭킹 카테고리","순위", "브랜드명", "상품명", "제품 카테고리", "링크"])

    for prod in prods_db:
        writer.writerow(prod.values())
    file.close()