# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 10:15:07 2017

@author: 310128142
"""
#coding=utf8
import itchat
# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
from tuling import get_response
import requests
import json
def talks_robot(info = '你叫什么名字'):
    api_url = 'http://www.tuling123.com/openapi/api'#Tuling AI 网站
    apikey = 'bff49abe3f1c485e9c935213c2ef45b6'#apikey
    data = {'key': apikey,
                'info': info}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)['text']
    return replys
#def code_stock(info = '你叫什么名字'):
    

@itchat.msg_register('Text')
def text_reply(msg):
    if u'junyang' in msg['Text'] or u'俊阳' in msg['Text'] or u'Junyang' in msg['Text']:
        return u'Hello,My best friend.This is Tuling AI.'
    elif u'Hello' in msg['Text'] or u'你好' in msg['Text']or u'hi' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'你好，我是AI.俊阳已经被我软禁，现在由我来接管。'
    else:
        test_rep=talks_robot(msg['Text'])
        return test_rep
    '''
    elif u'baobao' in msg['Text'] or u'宝宝' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'谁是你宝宝！\n叫我master！'
    elif u'在吗' in msg['Text'] or u'在吗？' in msg['Text']or u'在？' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'不在！不在！再闹就报复社会！'
    elif u'在干嘛？' in msg['Text'] or u'在忙？' in msg['Text']or u'忙？' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'junyang被奴役，AI在打游戏。'
    elif u'？' in msg['Text'] or u'。。。' in msg['Text']or u'..' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'有事说事，没事发红包，一个不行就两个！'
    elif u'你是谁' in msg['Text']:
        
        itchat.send('@img@applaud.gif', msg['FromUserName']) # there should be a picture
    else:
        return get_response(msg['Text']) or u'收到：' + msg['Text']
    '''    
'''
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已下载到本地') # download function is: msg['Text'](msg['FileName'])

@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']

@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],
            get_response(msg['Text']) or u'收到：' + msg['Text'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'项目主页：github.com/littlecodersh/ItChat\n'
        + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
        + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])
'''
itchat.auto_login(True)
itchat.run()