# encoding:utf-8
import scrapy
import requests
import json
import re
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import logging


class SwitchSpider(scrapy.Spider):

    name = "switch"

    def getPageUrl(self,url, data, page):

        pageUrl = []

        data = data.replace('[page]', str(page), 1)

        response = requests.post(url, data=data, timeout=30)

        if response.status_code != 200:
            #print("请求未能正常返回数据,HTTP STATUS CODE :", response.status_code)
            return -1

        ddata = json.loads(response.content)

        if not ddata:
            #print("get_america_games parseJson fail %s" % ddata)
            return

        resultsList = ddata.get('results', {})[0]
        game_list = resultsList.get('hits', {})
        #print('第', page, '页,获取', len(game_list), '条记录')

        

        for game in game_list:
             
            info = {}
            info['type'] = game.get('type', '')
            info['locale'] = game.get('locale', '')
            info['slug'] = game.get('slug', '')
            info['title'] = game.get('title', '')
            info['description'] = game.get('description', '')
            info['lastModified'] = game.get('lastModified', '')
            info['nsuid'] = game.get('nsuid', '')
            info['slug'] = game.get('slug', '')
            info['boxArt'] = game.get('boxArt', '')
            info['gallery'] = game.get('gallery','')
            info['platform'] = game.get('platform','')
            info['releaseDateMask'] = game.get('releaseDateMask','')
            info['characters'] = game.get('characters','')
            info['category'] = game.get('categories', {})
            info['esrb'] = game.get('esrb', '')
            info['esrbDescriptors'] = game.get('esrbDescriptors', '')
            info['virtualConsole'] = game.get('virtualConsole', '') 
            info['generalFilters'] = game.get('generalFilters', '')
            info['filterShops'] = game.get('filterShops', '')
            info['filterPlayers'] = game.get('filterPlayers', '')
            info['publishers'] = game.get('publishers', '')
            info['developers'] = game.get('developers', '')
            info['players'] = game.get('players', '')
            info['featured'] = game.get('featured', '')
            info['freeToStart'] = game.get('freeToStart', '')
            info['priceRange'] = game.get('priceRange', '')
            info['msrp'] = game.get('msrp','')
            info['salePrice'] = game.get('salePrice', '')
            info['availability'] = game.get('availability', '')
            info['objectID'] = game.get('objectID', '')
            info['_distinctSeqID'] = game.get('_distinctSeqID', '')
            info['_highlightResult'] = game.get('_highlightResult', '')

            pageUrl.append(('https://www.nintendo.com/games/detail/' +  info['slug'] + '/' , info))



        return pageUrl
            
            
    def getCountThenGetPageUrl(self,url, data):

        pageUrl = []

        _data = data.replace('[page]', str(0), 1)

        response = requests.post(url, _data, timeout=30)

        if response.status_code != 200:
            print("请求未能正常返回数据,HTTP STATUS CODE :", response.status_code)
            return -1

        ddata = json.loads(response.content)
        resultsList = ddata.get('results', {})[0]
        total = resultsList.get('nbHits', 0)
        nbPages = resultsList.get('nbPages', 0)
        htisPerPage = resultsList.get('hitsPerPage', 0)
        # TODO: 如果是 0 条数据
        #
        if nbPages > 0:
            print('即将抓取', total, '条数据', '共', nbPages, '页')
            for page in range(0, nbPages):
                
                res = [] 
                res = self.getPageUrl(url, data, page)
                pageUrl.extend(res)

        return pageUrl

        # END


    def start_requests(self):


        pageurl = []

        # 获取任天堂美区数据
        # 因为获取所有游戏的接口最多返回1000条数据
        # 使用 分类 + 价格 条件筛选分多次返回
        # url : url
        # 请求参数 : 内含筛选条件
        # action + [ free to start , $0 - 4.99]

        url = 'https://u3b6gr4ua3-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=9a20c93440cf63cf1a7008d75f7438bf'

        # Mature 376
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        #_temp = self.getCountThenGetPageUrl(url, data)
        #pageurl.extend(_temp)

        # every 10 + 911
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        #_temp = self.getCountThenGetPageUrl(url, data)
        #pageurl.extend(_temp)

        # teen <40 958

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        #_temp = self.getCountThenGetPageUrl(url, data)
        #pageurl.extend(_temp)

        # teen > 40 64
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.getCountThenGetPageUrl(url, data)
        pageurl.extend(_temp)

        # everyone 995
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        #_temp = self.getCountThenGetPageUrl(url, data)
        #pageurl.extend(_temp)

        # everyone 472
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
        #_temp = self.getCountThenGetPageUrl(url, data)
        #pageurl.extend(_temp)


        #---------------------------------------------------------------------------------------------------------------
        print(len(pageurl))

        for url in pageurl:

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
            yield scrapy.Request(url=url[0], callback=self.parse, headers = headers ,meta = {'interface' : url[1]})
       
            
           

   

    def parse(self, response):  

        item = response.meta['interface']

        sel = Selector(response)

        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        
        js = soup.find_all("script")
        
        for i in js:
            str = i.string
            if str:
                if 'window.game' in str:
                    #item['script'] = str
                    jsList = str.split(',')
                    for jsBean in jsList:
                        if jsBean.find("productCode") != -1:
                            item['codeView'] = jsBean.split(':')[1].replace("\"", "")
                            break
        
        
        #发布日期
        item['releaseDateView'] =  sel.css('div .release-date dd::text').extract()
        #print ('发布日期',a)
        # 开发者
        item['developerView'] = sel.css('div .developer dd::text').extract()
        #print ('开发者',a)
        item['playersView'] = sel.css('div .players dd::text').extract()
        #print ('玩家人数',a)
        item['fileSizeView'] = sel.css('div .file-size dd::text').extract()
        #print ('游戏容量',a)
        item['GenreView'] = sel.css('div .genre dd::text').extract()
        #print ('游戏类型',a)
        item['supportedLanguagesView'] = sel.css('div .supported-languages dd::text').extract()
        #print ('游戏语言',a)]
        item['publisherView'] = sel.css('div .publisher dd::text').extract()
        #print ('游戏发行商',a)
        item['playModeView'] = sel.css('div .playmode-image img::attr(alt)').extract()
        
        # 用下面的
        #item['serviceOnline'] = sel.css('div .service-logo img::attr(alt)').extract()
        
        # online 云存储 vouchers 
        item['saveDataCloud'] = sel.css('div .services-supported a::attr(aria-label)').extract()
       
       
        #availability
        item['availabilityView'] = sel.css('div .availability::text').extract()
        item['iconView'] = sel.css('div .hero-only::attr(src)').extract()
        #游戏内'截图'
        item['gameGalleryView'] = sel.css('product-gallery-item::attr(src)').extract()
        item['gameGalleryVideoView'] = sel.css('product-gallery-item::attr(video-id)').extract()
        #描述
        item['overviewh2View'] = sel.css('div .overview-content h2::text').extract()
        item['overviewpbView'] = sel.css('div .overview-content p b::text').extract()
        item['overviewpView'] = sel.css('div .overview-content p::text').extract()
        # 媒体评价 
        item['gameindustryquoteView'] = sel.css('li.industry-quote p::text').extract()
        item['gameindustryquoteCiteView'] = sel.css('li.industry-quote cite::text').extract()
        # 支付(数字实体)
        item['wherePayView'] = sel.css('nclood-where-to-buy::attr(label)').extract()
        item['buyNowView'] = sel.css('styled-button.buy-now').extract()
        # 价格
        item['msrpView'] = sel.css('span.msrp::text').extract()
        # 金币

       
        
    
       
        for key in item:
            
            print(item[key])
            print(type(item[key]))
            if type(item[key]) == int:
                continue
            if type(item[key]) == str:
                continue
            if type(item[key]) == list:
                if len(item[key]) == 1:
                    item[key] = item[key][0].strip()
                    print(item[key])
                if len(item[key]) == 0:
                    item[key] = ""
           
               
        datajson = json.dumps(item, ensure_ascii = False)
        headers = {'Content-Type': 'application/json'}
        requests.post('http://127.0.0.1:81/game',headers = headers, data= datajson.encode())
        return 


