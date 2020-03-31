from datetime import datetime
from datetime import timedelta
import json


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
    if now.hour >= 12:
        now_str += " pm"
    else:
        now_str += " am"
    f = open(turnip_path, "r", encoding='utf-8')
    content = f.read() 
    if content != "":
        data = json.loads(content, encoding='utf-8')
        if data["date"] != now_str:
            return "未记录"
    else:
        return "未记录"
    if now.isoweekday() == 7:
        if now.hour >= 12:
            return "现在无法交易大头菜"
        key = min(data["prices"], key=data["prices"].get)
        return "最低价为%d，岛主为[CQ:at,qq=%s]" % (data["prices"][key], key)
    else:
        if now.hour >= 22 or now.hour < 8:
            return "现在无法交易大头菜"
        key = max(data["prices"], key=data["prices"].get)
        return "最高价为%d，岛主为[CQ:at,qq=%s]" % (data["prices"][key], key)
    f.close()