from google_search_py import search
from parse import parse_with, parse_without


async def find_with(text):
    result = search(text + " amdm.ru")
    url = result['url']
    await parse_with(url)


async def find_without(text):
    result = search(text + " текст песни genius.com")
    url = result['url']
    await parse_without(url)
