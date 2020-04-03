#coding=utf-8
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup 
import re


def process(message):
    if "、" not in message:
        return message
    l = message.split("、")
    if "（" in l[0]:
        return l[0][1:-1]
    else:
        return l[0] + "~" + l[-1]

def get_now():
    now = datetime.now()
    if now.hour < 5:
        now -= timedelta(days=1);
        datetime.timestamp
    return now

def now_can_get(event, message):
    args = message.split()
    if args[0] != "现在":
        return None
    if len(args) == 3:
        if args[1] == "南半球" or args[1] == "北半球":
            r = requests.get('https://wiki.biligame.com/dongsen/' + args[2])
            soup = BeautifulSoup(r.text, 'html.parser')
            h = soup.find(text=re.compile(args[1]))
            if h is None:
                return "找不到该物种"
            months = h.find_next().text.strip().split("、")
            h = soup.find(text=re.compile("时间"))
            hours = h.find_next().text.strip().split("、")
            now = get_now()
            if str(now.month) in months and str(now.hour) in hours:
                return "现在可以捉到" + args[2]
            else:
                return "今天捉不到" + args[2]
        else:
            return "请输入：现在 (+【半球】)+【物种名】"
    elif len(args) == 2:
        r = requests.get('https://wiki.biligame.com/dongsen/' + args[1])
        soup = BeautifulSoup(r.text, 'html.parser')
        h = soup.find(text=re.compile("月份"))
        if h is None:
            return "找不到该物种"
        months = h.find_next().text.strip().split("、")
        h = soup.find(text=re.compile("时间"))
        hours = h.find_next().text.strip().split("、")
        now = get_now()
        if str(now.month) in months and str(now.hour) in hours:
            return "现在可以捉到" + args[1]
        else:
            return "现在捉不到" + args[1]
    else:
        return "请输入：现在 (+【半球】)+【物种名】"

def today_can_get(event, message):
    args = message.split()
    if args[0] != "今天":
        return None
    if len(args) == 3:
        if args[1] == "南半球" or args[1] == "北半球":
            r = requests.get('https://wiki.biligame.com/dongsen/' + args[2])
            soup = BeautifulSoup(r.text, 'html.parser')
            h = soup.find(text=re.compile(args[1]))
            if h is None:
                return "找不到该物种"
            months = h.find_next().text.strip().split("、")
            h = soup.find(text=re.compile("时间"))
            hours = h.find_next().text.strip().split("、")
            now = get_now()
            if str(now.month) in months:
                return "今天可以捉到" + args[2]
            else:
                return "今天捉不到" + args[2]
        else:
            return "请输入：今天 (+【半球】)+【物种名】"
    elif len(args) == 2:
        r = requests.get('https://wiki.biligame.com/dongsen/' + args[1])
        soup = BeautifulSoup(r.text, 'html.parser')
        h = soup.find(text=re.compile("月份"))
        if h is None:
            return "找不到该物种"
        months = h.find_next().text.strip().split("、")
        h = soup.find(text=re.compile("时间"))
        hours = h.find_next().text.strip().split("、")
        now = get_now()
        if str(now.month) in months:
            return "今天可以捉到" + args[1]
        else:
            return "今天捉不到" + args[1]
    else:
        return "请输入：今天 (+【半球】)+【物种名】"


def search_wiki(event, message):
    args = message.split()
    if len(args) != 2:
        return "请输入：【名称】+【属性】"
    r = requests.get('https://wiki.biligame.com/dongsen/' + args[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    h = soup.find(text=re.compile(args[1]))
    if h is None:
        return "找不到该属性"
    return process(h.find_next().text.strip())