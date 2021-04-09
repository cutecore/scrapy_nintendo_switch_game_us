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



    def get_page_url(self, url, data, page):

        pageUrl = []

        data = data.replace('[page]', str(page), 1)

        response = requests.post(url, data=data, timeout=30)

        if response.status_code != 200:
            # print("请求未能正常返回数据,HTTP STATUS CODE :", response.status_code)
            return -1

        ddata = json.loads(response.content)

        if not ddata:
            # print("get_america_games parseJson fail %s" % ddata)
            return

        resultsList = ddata.get('results', {})[0]
        game_list = resultsList.get('hits', {})
        # print('第', page, '页,获取', len(game_list), '条记录')

        for game in game_list:
            info = dict()
            info['type'] = self.clean_value(game.get('type', ''))
            info['locale'] = self.clean_value(game.get('locale', ''))
            info['slug'] = self.clean_value(game.get('slug', ''))
            info['title'] = self.clean_value(game.get('title', ''))
            info['description'] = self.clean_value(game.get('description', ''))
            info['nsuid'] = self.clean_value(game.get('nsuid', ''))
            info['slug'] = self.clean_value(game.get('slug', ''))
            info['boxArt'] = self.clean_value(game.get('boxArt', ''))
            info['platform'] = self.clean_value(game.get('platform', ''))

            info['gallery'] = self.clean_value(game.get('gallery', ''))

            if game.get('releaseDateMask', '') and "T" in game.get('releaseDateMask', ''):
                info['releaseDate'] = str(game.get('releaseDateMask', '')).split("T")[0]

            info['characters'] = self.clean_value(game.get('characters', ''))
            info['category'] = self.clean_value(game.get('categories', {}))
            info['esrb'] = self.clean_value(game.get('esrb', ''))
            info['esrbDescriptors'] = self.clean_value(game.get('esrbDescriptors', ''))
            info['publishers'] = self.clean_value(game.get('publishers', ''))
            info['developers'] = self.clean_value(game.get('developers', ''))
            info['players'] = self.clean_value(game.get('players', ''))
            info['featured'] = self.clean_value(game.get('featured', ''))
            info['freeToStart'] = self.clean_value(game.get('freeToStart', ''))
            info['msrp'] = self.clean_value(game.get('msrp', ''))
            info['availability'] = self.clean_value(game.get('availability', ''))
            pageUrl.append(('https://www.nintendo.com/games/detail/' + info['slug'] + '/', info))

        return pageUrl

    def get_count_then_get_page_url(self, url, data):

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
                res = self.get_page_url(url, data, page)
                pageUrl.extend(res)

        return pageUrl

        # END

    def start_requests(self):

        pageurl = list()

        # action + [ free to start , $0 - 4.99]

        url = 'https://u3b6gr4ua3-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=9a20c93440cf63cf1a7008d75f7438bf'
        url = 'https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=c4da8be7fd29f0f5bfa42920b0a99dc7'
 
        # Mature 376
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrb%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # every 10 + 911
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrb%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # teen <40 958

        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3AFree%20to%20start%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # teen > 40 64
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # everyone 995
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%245%20-%20%249.99%22%2C%22priceRange%3A%240%20-%20%244.99%22%2C%22priceRange%3AFree%20to%20start%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'

        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # everyone 472
        data = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=[page]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrb&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%2C%22priceRange%3A%2420%20-%20%2439.99%22%2C%22priceRange%3A%2440%2B%22%5D%2C%5B%22esrb%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
        _temp = self.get_count_then_get_page_url(url, data)
        pageurl.extend(_temp)

        # ---------------------------------------------------------------------------------------------------------------
        # print(len(pageurl))

        for url in pageurl:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
            yield scrapy.Request(url=url[0], callback=self.parse, headers=headers, meta={'interface': url[1]})

        # url = pageurl[0]
        # #
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'}
        # yield scrapy.Request(url=url[0], callback=self.parse, headers=headers, meta={'interface': url[1]})

    #

    def parse(self, response):

        item = response.meta['interface']

        sel = Selector(response)

        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')

        js = soup.find_all("script")

        for i in js:
            str = i.string
            if str:
                if 'window.game' in str:
                    # item['script'] = str
                    jsList = str.split(',')
                    for jsBean in jsList:
                        if jsBean.find("productCode") != -1:
                            item['code'] = jsBean.split(':')[1].replace("\"", "")
                            break

        item['developer'] = self.clean_value(sel.css('div .developer dd::text').extract())
        item['players'] = self.clean_value(sel.css('div .players dd::text').extract())
        item['fileSize'] = self.clean_value(sel.css('div .file-size dd::text').extract())
        item['genre'] = self.clean_value(sel.css('div .genre dd::text').extract())
        item['languages'] = self.clean_value(sel.css('div .supported-languages dd::text').extract())
        item['publisher'] = self.clean_value(sel.css('div .publisher dd::text').extract())
        item['playMode'] = self.clean_value(sel.css('div .playmode-image img::attr(alt)').extract())

        item['saveDataCloud'] = self.clean_value(sel.css('div .services-supported a::attr(aria-label)').extract())
        item['availability'] = self.clean_value(sel.css('div .availability::text').extract()).replace("\n", "").\
            replace("\t", "")
        item['icon'] = self.clean_value(sel.css('div .hero-only::attr(src)').extract())
        item['gallery'] = self.clean_value(sel.css('product-gallery-item::attr(src)').extract())

        print(json.dumps(item))


        datajson = json.dumps(item, ensure_ascii=False)
        headers = {'Content-Type': 'application/json',
                   'auth': 'eyJ0eXAiOiJKV1QiLCJhbG'
                           'ciOiJIUzI1NiJ9.eyJpc3MiOiJjdXRlYyIsImV4cCI6MTY0NTUxODcw'
                           'MCwiaWF0IjoxNjEzOTgyNzAwLCJ1c2VySWQiOiI3In0.Q_FoaN7rT1y9'
                           'wxr-NVUPaT9mxLBnWEUXChIKnzj23TE'}
        requests.post('http://140.143.211.59/game', headers=headers, data=datajson.encode())
        yield item
