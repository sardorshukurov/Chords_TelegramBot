import requests
from bs4 import BeautifulSoup


async def parse(url):
    api = requests.get(url)
    api_content = api.text
    soup = BeautifulSoup(api_content, 'html.parser')
    text = soup.find_all(class_='b-podbor__text')
    f = open("file.txt", "w")
    for i in range(len(text)):
        f.write(text[i].get_text() + "\n")
    f.close()
