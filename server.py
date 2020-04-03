#coding=utf-8
from cqhttp import CQHttp
from wiki import search_wiki
from turnip import get_turnip, record_turnip

bot_id = 2739725869

bot = CQHttp(api_root='http://127.0.0.1:5700/')

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
        result = now_can_get(event, message);
        if result != None: 
            bot.send(event, result); 
            return
        result = today_can_get(event, message);
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


bot.run(host='0.0.0.0', port=7777)
