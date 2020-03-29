from cqhttp import CQHttp
import requests
from bs4 import BeautifulSoup 
import re
from datetime import datetime
from datetime import timedelta
import json

bot_id = 2739725869

bot = CQHttp(api_root='http://127.0.0.1:5700/')
turnip_path = "./turnip.json"


def get_now():
    now = datetime.now()
    if now.hour < 5:
        now -= timedelta(days=1);
        datetime.timestamp
    return now

def record_turnip(event, message):
    args = message.split()
    if len(args) != 2 or args[0] != "记录大头菜":
        return None
    try:
        price = int(args[1])
    except:
        return "参数非法"
    now = get_now()
    now_str = datetime.strftime(now,'%Y-%m-%d')
    f = open(turnip_path, "a+", encoding='utf-8')
    f.seek(0)
    content = f.read() 
    if content != "":
        data = json.loads(content, encoding='utf-8')
        if data["date"] != now_str:
            data["date"] = now_str
            data["prices"] = dict()
    else:
        data = dict()
        data["date"] = now_str
        data["prices"] = dict()
    data["prices"][str(event["sender"]["user_id"])] = price
    j = json.dumps(data,ensure_ascii=False,sort_keys=True, indent=4)
    f.seek(0)
    f.truncate();
    f.write(j)
    f.close()
    return "记录成功"
    
def get_min(d):
    min_value = int("inf")
    min_key = None
    for key, value in d.items():
        if value < min_value:
            min_value = value
            min_key = key
    return min_key, min_value



def get_turnip(event, message):
    args = message.split()
    if len(args) != 1 or args[0] != "大头菜价格":
        return None
    now = get_now()
    now_str = datetime.strftime(now,'%Y-%m-%d')
    f = open(turnip_path, "r", encoding='utf-8')
    content = f.read() 
    if content != "":
        data = json.loads(content, encoding='utf-8')
        if data["date"] != now_str:
            return "今日未记录"
    else:
        return "今日未记录"
    if now.isoweekday() == 7:
        if now.hour >= 12 or now.hour < 5:
            return "现在无法交易大头菜"
        key = min(data["prices"], key=data["prices"].get)
        return "最低价为%d，岛主为[CQ:at,qq=%s]" % (data["prices"][key], key)
    else:
        key = max(data["prices"], key=data["prices"].get)
        return "最高价为%d，岛主为[CQ:at,qq=%s]" % (data["prices"][key], key)
    f.close()

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


@bot.on_message
def handle_msg(event):
    if event["message_type"] == "group" and "[CQ:at,qq=%d]" % bot_id not in event["message"]:
        return 
    message = event['message']
    message = message.replace("[CQ:at,qq=%d]" % bot_id, "")
    bot.logger.info(event)
    try:
        result = get_turnip(event, message);
        if result != None: 
            bot.send(event, result); 
            return
        result = record_turnip(event, message);
        if result != None: 
            bot.send(event, result); 
            return
        result = search_wiki(event, message);
        if result != None: 
            bot.send(event, result); 
            return
        
    except Exception as e:
        bot.send(event, '出错: ' + repr(e))

@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(event):
    bot.send(event, message='欢迎新人，群名片请改成系统用户名+角色名+岛屿，祝您无人岛移居愉快', auto_escape=True)  # 发送欢迎新人


@bot.on_request('group', 'friend')
def handle_request(event):
    return {'approve': True}  # 同意所有加群、加好友请求


bot.run(host='127.0.0.1', port=8080, debug=True)