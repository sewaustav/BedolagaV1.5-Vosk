import requests
from bs4 import BeautifulSoup as BS


page = 4735
count = 1

with open('data.txt', 'w', encoding='utf-8') as f:
    while count < page:
        r = requests.get("https://www.unipage.net/ru/cities?page="+str(count)+"&per-page=10")
        html = BS(r.content, "html.parser")
        selector = html.select(".generated-card-header__title")

        if len(selector):
            for el in selector:
                text = el.select("a")
                for i in text:
                    f.write(i.text + '\n')
        else: print("ERROR")
        count += 1

print("[INFO] Success")
