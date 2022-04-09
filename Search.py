from google_search_py import search
from parse import parse


async def find(text):
    result = search(text + " amdm.ru")
    url = result['url']
    await parse(url)
