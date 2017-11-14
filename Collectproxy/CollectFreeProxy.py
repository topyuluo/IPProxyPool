# -*- coding: utf-8 -*-
#! /usr/bin/env python

from lxml import etree
import  re
from Utils.Download import downloadPage
from Utils.Util import time
from Utils.Logger import Logger
import json

"""
收集免费代理类
"""
logger = Logger("scheduler").getLog()
class CollectFreeProxy(object):

    @staticmethod
    @time('快代理')
    def firstFreeProxy(page =4):
        """
        kuaidaili  fetch
        :param page:
        :return:
        """
        url_list = ('http://www.kuaidaili.com/free/inha/{page}/'.format(page=page) for page in range (1 ,page+1 ))
        for url in url_list:
            logger.info('dowload url : %s ' % url)
            html = downloadPage(url)
            if html:
                etree_html = etree.HTML(html)
                for ip in etree_html.xpath('.//div[@id="list"]//tbody/tr'):
                    yield  ':'.join(ip.xpath('./td/text()')[0:2])
            else:
                logger.error('firstFreeProxy-快代理 download fail')

    @staticmethod
    @time('代理66网站抓取')
    def secondFreeProxy(proxy_number = 100):
        """
        66ip fetch
        :param proxy_number:
        :return:
        """
        url = 'http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip'.format(proxy_number)
        logger.info('dowload url : %s ' % url)
        html = downloadPage(url)
        if html:
            ip_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for ip in ip_list:
                yield ip
        else:
            logger.error('secondFreeProxy-代理66 download fail')

    @staticmethod
    @time('云代理')
    def thirdFreeProxy(page=5):
        """
        ip3366 fetch
        :param page:
        :return:
        """
        # url_list = ('http://www.kuaidaili.com/free/inha/{page}/'.format(page=page) for page in range(1, page + 1))
        url_list = ('http://www.ip3366.net/?stype=1&page={page}'.format(page=page) for page in range(1 , page+1))
        for url in url_list:
            logger.info('dowload url : %s ' % url)
            html = downloadPage(url)
            if html:
                etree_html = etree.HTML(html)
                for ip in etree_html.xpath('.//div[@id="list"]//tbody/tr'):
                    yield ':'.join(ip.xpath('./td/text()')[0:2])
            else:
                logger.error('thirdFreeProxy-云代理 download fail')

    @staticmethod
    @time('西刺代理')
    def fourFreeProxy(page = 9 ):
        """
        xicidaili fetch
        :param page:
        :return:
        """
        url_list = ('http://www.xicidaili.com/nn/{page_num}'.format(page_num=page_num) for page_num in range(1, page+1))
        for url in url_list:
            logger.info('dowload url : %s ' % url)
            url_content = downloadPage(url)
            if url_content:
                tr_list = etree.HTML(url_content).xpath('.//table[@id="ip_list"]//tr')
                for tr in tr_list:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])
            else:
                logger.error('fourFreeProxy-西刺代理 download fail')

    @staticmethod
    @time('代理360')
    def fiveFreeProxy():
        """
        proxy360 fetch
        :return:
        """
        url = 'http://www.proxy360.cn/Region/China'
        logger.info('dowload url : %s ' % url)
        html_content = downloadPage(url)
        if html_content:

            etree_html = etree.HTML(html_content)
            table_html = etree_html.xpath('.//table[@width="940px"]//div[@id="ctl00_ContentPlaceHolder1_upProjectList"]//div[@class="proxylistitem"]/div[1]')
            ipList=[]
            for span in table_html:
                ip = str(span.xpath('./span/text()')[0]).strip()
                port = str(span.xpath('./span/text()')[1]).strip()
                ipList.append(ip+":"+port)
            return ipList
        else:
            logger.error('fiveFreeProxy-代理360 download fail')

    @staticmethod
    @time('流年代理')
    def sixFreeProxy():
        """
        89ip fetch
        :return:
        """
        url = 'http://www.89ip.cn/tiqv.php?sxb=&tqsl=1000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
        logger.info('dowload url : %s ' % url)
        html = downloadPage(url)
        if html:
            ip_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for ip in ip_list:
                yield ip
        else:
            logger.error('sixFreeProxy-流年代理 download fail')

    @staticmethod
    @time('ip181')
    def sevenFreeProxy():
        """
        ip 181 fetch
        :return:
        """
        url = 'http://www.ip181.com/'
        logger.info('dowload url : %s ' % url)
        html = downloadPage(url)
        if html:
            etree_html = etree.HTML(html)
            tr_list = etree_html.xpath('//table/tbody/tr')
            for tr in tr_list:
                yield  ':'.join(tr.xpath('./td/text()')[0:2])
        else:
            logger.error('sevenFreeProxy-ip181 download fail')

    @staticmethod
    @time('极速代理')
    def eightFreeProxy():
        """
        superfastip fetch
        :return:
        """
        url = 'http://superfastip.com/welcome/getapi'
        logger.info('dowload url : %s ' % url)
        page = downloadPage(url)
        if page :
            for data in json.loads(page).get('data'):
                yield ':'.join(data[1:3])
        else:
            logger.error('eightFreeProxy-极速代理 download fail')


if __name__ =='__main__':
    proxy = CollectFreeProxy.freeProxyFifth()
    for ip in proxy:
        print (ip)