# encoding:utf-8
import scrapy
import requests
import json
import re
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import logging

auth = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjdXRlYyIsImV4cCI6MTYxOTA4MTMyNSwiaWF0IjoxNjE5MDc0MTI1LCJ1c2VySWQiOiIxIn0.ft7W1WEu7JC_doual1-Yl3NBuPuTUWIg_BGvrGlj5KU'

class SwitchSpider(scrapy.Spider):
    name = "switch"

    def clean_value(self, raw):
        if raw is None:
            return ''
        if type(raw) == str:
            return raw
        if type(raw) == list:
            if len(raw) == 0:
                return ''
            elif len(raw) == 1:
                return raw[0]
            else:
                return ",".join(raw)



    def start_requests(self):

        host = 'https://www.nintendo.com/'
        

        url = 'http://127.0.0.1:81/game-crawl-info/1/5200'
        headers = {
            'auth': auth
        }
        response = requests.get(url, headers = headers)
        print(response.status_code)
       
        for item in json.loads(response.content):
            if item != None:
                url = ''
                if len(item['slug']):
                    url = host + 'games/detail/' +item['slug'] + '/'
                elif len(item['url']):
                    url = host + item['url'] + '/'
                nsuid = item['nsuid']

                yield scrapy.Request(url=url, callback=self.parse, meta={'nsuid': nsuid})    

   


    def parse(self, response):

        # item = 
        item = {}
        item['nsuid'] = response.meta['nsuid']
        
        sel = Selector(response)

        # soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')

        # js = soup.find_all("script")

        # for i in js:
        #     str = i.string
        #     if str:
        #         if 'window.game = Object.freeze' in str:
        #             # item['script'] = str
        #             jsList = str.split(',')
        #             for jsBean in jsList:
        #                 if jsBean.find("productCode") != -1:
        #                     item['code'] = jsBean.split(':')[1].replace("\"", "")
        #                     break

        item['fileSize'] = self.clean_value(sel.css('div .file-size dd::text').extract())
        item['gallery'] = self.clean_value(sel.css('product-gallery-item::attr(src)').extract())

        item['publisher'] = self.clean_value(sel.css('div .publisher dd::text').extract())
        item['players'] = self.clean_value(sel.css('div .players dd::text').extract())
        item['developer'] = self.clean_value(sel.css('div .developer dd::text').extract())
        item['availability'] = self.clean_value(sel.css('div .availability::text').extract().replace('\t','').replace('\n',''))


        print(json.dumps(item))


        datajson = json.dumps(item, ensure_ascii=False)
        headers = {'Content-Type': 'application/json',
                   'auth': auth}
        requests.post('http://127.0.0.1:81/game', headers=headers, data=datajson.encode())
        yield item
