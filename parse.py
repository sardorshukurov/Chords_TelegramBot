import requests
from bs4 import BeautifulSoup


async def parse_with(url):
    api = requests.get(url)
    api_content = api.text
    soup = BeautifulSoup(api_content, 'html.parser')
    text = soup.find_all(class_='b-podbor__text')
    f = open("file.txt", "w")
    for i in range(len(text)):
        f.write(text[i].get_text() + "\n")
    f.close()


async def parse_without(url):
    api = requests.get(url)
    api_content = api.text
    soup = BeautifulSoup(api_content, 'lxml')
    text = soup.find_all('div', {'class': 'Lyrics__Container-sc-1ynbvzw-6'})
    f = open("file.txt", "w")
    print(len(text))
    for i in range(len(text)):
        f.write(text[i].get_text(separator="\n") + "\n")
    f.close()
