#coding=utf-8
import requests
from bs4 import BeautifulSoup 
import re

def search_wiki(event, message):
    args = message.split()
    if len(args) != 2:
        return "请输入名称+属性!"
    r = requests.get('https://wiki.biligame.com/dongsen/' + args[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    h = soup.find(text=re.compile(args[1]))
    if h is None:
        return "找不到该属性"
    return h.find_next().text.strip()