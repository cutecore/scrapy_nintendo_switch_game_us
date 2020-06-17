# encoding:utf-8
import scrapy
import requests
import json
import re
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import logging




class GameInfo(object):
    # __slots__ = ('type','code', 'url', 'title', 'pubDate', 'pubDateUS', 'pubDateEU', 'pubDateJP', 'icon', 'iconFrom', 'nsuid', 'nsuidEu', 'nsuidJp',
    #              'chinese', 'playersMin', 'players', 'demo', 'category', 'pics', 'movies', 'moviesFrom', 'updateTime', 'alias',
    #              'demo', 'offlineMultiplayModel', 'localMultiplayModel', 'onlineMultiplayModel',
    #              'offlineMultiplayers', 'localMultiplayers', 'onlineMultiplayers',  'multiPlayModel',
    #              'playModelName', 'weight', 'softType', 'preorder', 'bannerImage', 'dlc', 'amiiboAble', 'amiibo', 'publisher', 'developer'
    #              , 'free', 'language', 'languageUS', 'languageEU', 'languageJP',  'languageHK', 'hd_rumble', 'proAble', 'internet', 'nso')

    pass

class SwitchAmercianSpider(scrapy.Spider):

    name = "switch_amercian"

    def get_america_games_web(self,game):
        
        if len(game.slug) == 0:
            return -1

        gameurl = 'https://www.nintendo.com/games/detail/' + game.slug
        response = requests.post(gameurl)
        sel = Selector(response)

        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
        
        js = soup.find_all("script")
        
        for i in js:
            str = i.string
            if str:
                if 'window.game' in str:
                    game.script = str
                    jsList = str.strip().split(',')
                    for jsBean in jsList:
                        if jsBean.find("productCode") != -1:
                            game.codeView = jsBean.split(':')[1].replace("\"", "")
                            break
        

        #发布日期
        game.releaseDateView =  sel.css('div .release-date dd::text').extract()
        #print ('发布日期',a)
        # 开发者
        game.developerView = sel.css('div .developer dd::text').extract()
        #print ('开发者',a)
        game.playersView = sel.css('div .players dd::text').extract()
        #print ('玩家人数',a)
        game.fileSizeView = sel.css('div .file-size dd::text').extract()
        #print ('游戏容量',a)
        game.GenreView = sel.css('div .genre dd::text').extract()
        #print ('游戏类型',a)
        game.supportedLanguagesView = sel.css('div .supported-languages dd::text').extract()
        #print ('游戏语言',a)]
        game.publisherView = sel.css('div .publisher dd::text').extract()
        #print ('游戏发行商',a)
        game.playModeView = sel.css('div .playmode-image img::attr(alt)').extract()
        
        # 用下面的
        #game.serviceOnline = sel.css('div .service-logo img::attr(alt)').extract()
        
        # online 云存储 vouchers 
        game.saveDataCloud = sel.css('div .services-supported a::attr(aria-label)').extract()
       
       
        #availability
        game.availabilityView = sel.css('div .availability::text').extract()
        game.iconView = sel.css('div .hero-only::attr(src)').extract()
        #游戏内'截图'
        game.gameGalleryView = sel.css('product-gallery-item::attr(src)').extract()
        game.gameGalleryVideoView = sel.css('product-gallery-item::attr(video-id)').extract()
        #描述
        game.overviewh2View = sel.css('div .overview-content h2::text').extract()
        game.overviewpbView = sel.css('div .overview-content p b::text').extract()
        game.overviewpView = sel.css('div .overview-content p::text').extract()
        # 媒体评价 
        game.gameindustryquoteView = sel.css('li.industry-quote p::text').extract()
        game.gameindustryquoteCiteView = sel.css('li.industry-quote cite::text').extract()
        # 支付(数字实体)
        game.wherePayView = sel.css('nclood-where-to-buy::attr(label)').extract()
        game.buyNowView = sel.css('styled-button.buy-now').extract()
        # 价格
        game.msrpView = sel.css('span.msrp::text').extract()
        # 金币
        
        overdict = game.__dict__
        datajson = json.dumps(overdict, ensure_ascii = False)
        headers = {'Content-Type': 'application/json'}
        requests.post('http://127.0.0.1:5060/game-service/game',headers = headers, data= datajson.encode())

       


       
        
        


        return 



    def fetchFromUrl(self,url, data, page):

        data = data.replace('[page]', str(page), 1)

        response = requests.post(url, data=data, timeout=5)

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
             
            info = GameInfo()
            info.type = game.get('type', '')
            info.locale = game.get('locale', '')
            info.slug = game.get('slug', '')
            info.title = game.get('title', '')
            info.description = game.get('description', '')
            info.lastModified = game.get('lastModified', '')
            info.nsuid = game.get('nsuid', '')
            info.slug = game.get('slug', '')
            info.boxArt = game.get('boxArt', '')
            info.gallery = game.get('gallery','')
            info.platform = game.get('platform','')
            info.releaseDateMask = game.get('releaseDateMask','')
            info.characters = game.get('characters','')
            info.category = game.get('categories', {})
            info.esrb = game.get('esrb', '')
            info.esrbDescriptors = game.get('esrbDescriptors', '')
            info.virtualConsole = game.get('virtualConsole', '') 
            info.generalFilters = game.get('generalFilters', '')
            info.filterShops = game.get('filterShops', '')
            info.filterPlayers = game.get('filterPlayers', '')
            info.publishers = game.get('publishers', '')
            info.developers = game.get('developers', '')
            info.players = game.get('players', '')
            info.featured = game.get('featured', '')
            info.freeToStart = game.get('freeToStart', '')
            info.priceRange = game.get('priceRange', '')
            info.msrp = game.get('msrp','')
            info.salePrice = game.get('salePrice', '')
            info.availability = game.get('availability', '')
            info.objectID = game.get('objectID', '')
            info._distinctSeqID = game.get('_distinctSeqID', '')
            info._highlightResult = game.get('_highlightResult', '')

            
            self.get_america_games_web(info)
            
            #with open('filename', 'a+',encoding='utf-8') as f:
            #    f.write(info.title + "\n")



    def fetchFromUrlWithFilter(self,url, data):

        _data = data.replace('[page]', str(0), 1)

        response = requests.post(url, _data, timeout=10)

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
                self.fetchFromUrl(url, data, page)

        # END


    def start_requests(self):

        # 获取任天堂美区数据
        # 因为获取所有游戏的接口最多返回1000条数据
        # 使用 分类 + 价格 条件筛选分多次返回
        # url : url
        # 请求参数 : 内含筛选条件
        # action + [ free to start , $0 - 4.99]

        url = 'https://u3b6gr4ua3-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=9a20c93440cf63cf1a7008d75f7438bf'

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%5D%2C%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%5D%2C%5B%22categories%3AAction%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)

        exit()

        # action + ['$5 -9']

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%5D%2C%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%5D%2C%5B%22categories%3AAction%22%5D%5D"}]}'
        
        self.fetchFromUrlWithFilter(url, data)

        # 10 - 19
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22categories%3AAction%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)
    
        # 20 - 39,40 + 
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22categories%3AAction%22%5D%5D"}]}'
        
        self.fetchFromUrlWithFilter(url, data)


        

        print ("a -end ")

        # adventure
        # adventure + free + 0-4 + 5-9
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3AAdventure%22%5D%2C%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3AAdventure%22%5D%2C%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)

        # adventure + 10-19 + 20-39 + 40 + 
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22categories%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22categories%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22categories%3AAdventure%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)

        print ("ad -end ")

        # appliation + edu + fitness + indie + music + party + racing 
        #
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3AApplication%22%2C%22categories%3AEducation%22%2C%22categories%3AFitness%22%2C%22categories%3AIndie%22%2C%22categories%3AMusic%22%2C%22categories%3AParty%22%2C%22categories%3ARacing%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3AApplication%22%2C%22categories%3AEducation%22%2C%22categories%3AFitness%22%2C%22categories%3AIndie%22%2C%22categories%3AMusic%22%2C%22categories%3AParty%22%2C%22categories%3ARacing%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)

        print ("app -end ")

        ## puzzle
        # 
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3APuzzle%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3APuzzle%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)

        ## role-playing
        # 
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3ARole-Playing%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3ARole-Playing%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)
        ##
        # sim sport 

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3ASimulation%22%2C%22categories%3ASports%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3ASimulation%22%2C%22categories%3ASports%22%5D%5D"}]}'
        self.fetchFromUrlWithFilter(url, data)

        ## strategy # 已确认
        #

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22categories%3AStrategy%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=categories&facetFilters=%5B%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22categories%3AStrategy%22%5D%5D"}]}'

        self.fetchFromUrlWithFilter(url, data)


    def parse(self, response):
        pass



if __name__ == "__main__":
    data = {"title": "title", "msrp": '123456','locale' : 'american'}
    datajson = json.dumps(data)
    
    headers = {'Content-Type': 'application/json'}
    requests.post('http://127.0.0.1:5060/game-service/game',headers = headers, data= datajson)
        

   





    
    