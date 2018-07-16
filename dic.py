# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Wang Tianqi (tianqi.wang@sjtu.edu.cn)
# File: dic-all-in-one.py
# Introduction: 对有道单词查询的网页进行简单提取

import re
import time
import thread
import urllib
import urllib2
from urllib import quote

class Spider_Youdao:
    #初始化
    def __init__(self):
        #有道网页翻译段
        self.Trans_Youdao_Tag = re.compile(r'\s?<li>.*?</li>\s?')
        #21世纪大词典段
        self.Trans_Shiji_Tag = re.compile(r'\s?<span.*?class="def">.*?</span>')
        #退出标志
        self.run = True

    #获得查询的单词
    def SearchWord(self):
        S_Word = raw_input("\n#[输入单词]\n>")
        return S_Word

    #得到URL
    def GetUrl(self, SWord=None):
        if not SWord:
            SWord = self.SearchWord()
        #加上查询的单词以后
        if quote(SWord) == SWord:
            MyUrl = "http://dict.youdao.com/search?len=eng&q="+quote(SWord)+"&keyfrom=dict.top"
            return MyUrl

    #获得页面
    def GetPage(self, SWord=None):
        #获取URL
        Youdao_Url = self.GetUrl(SWord)
        #伪装成浏览器请求
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'
        headers = {'User-Agent' : user_agent}
        req = urllib2.Request(Youdao_Url, headers = headers)
        Res = urllib2.urlopen(req)
        #将其他编码的字符串转换成unicode编码
        ResultPage = Res.read().decode("utf-8")
        #ResultPage = Res.read()
        return ResultPage

    #开始提取网页中的信息
    def ExtractPage(self, SWord=None):
        result = u''
        #获得页面
        MyPage = self.GetPage(SWord)
        #提取有道的基本翻译
        YoudaoTrans = self.Trans_Youdao_Tag
        #提取21世纪词典的翻译
        ShijiTrans = self.Trans_Shiji_Tag
        result += u"--------------------------------------------\n"
        YouDaoTrans = self.Trans_Youdao_Tag
        TransYdIterator = YouDaoTrans.finditer(MyPage)
        result += u"#(翻译来自有道词典):\n"
        myItems = re.findall('<div.*?class="trans-container">(.*?)<div id="webTrans" class="trans-wrapper trans-tab">',MyPage,re.S)
        for item in myItems:
            YDTmp = item
        TransYdIterator = YouDaoTrans.finditer(YDTmp)
        for iterator in TransYdIterator:
            YouDao = iterator.group()
            YDTag = re.compile('\s?<.*?>')
            result += YDTag.sub('',YouDao)
            result += '\n'
        result += u"--------------------------------------------\n"
        TransSjIterator = ShijiTrans.finditer(MyPage)
        result += u"#(翻译来自21世纪大词典):\n"
        for iterator in TransSjIterator:
            ShiJi = iterator.group()
            SJTag = re.compile('\s?<.*?>')
            result += SJTag.sub('',ShiJi)
            result += '\n'
        result += u"--------------------------------------------\n"
        return result

    #启动爬虫
    def Start(self):
        while self.run:
            S_Word = raw_input("\n#[\"!\"号退出.回车继续.]\n>")
            if S_Word != "!":
                self.ExtractPage()
                #thread.start_new_thread(self.ExtractPage,())
                #time.sleep(5)
            else:
                self.run = False


def main(word):
    mydict = Spider_Youdao()
    return mydict.ExtractPage(word)


if __name__ == '__main__':
    mydict = Spider_Youdao()
    mydict.Start()
