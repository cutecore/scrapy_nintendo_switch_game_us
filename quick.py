import requests
import json

def clean_value(raw):
    
    if raw is None:
        return ''
    if type(raw) == int:
        return str(raw)
    if type(raw) == float:
        return str(raw)
    if type(raw) == str:
        return raw
    if type(raw) == list:
        if len(raw) == 0:
            return ''
        elif len(raw) == 1:
            return raw[0]
        else:
            return ",".join(raw)



def build_url(url, data):
    data = template_data.replace('[page=1]','page=1')

    response = requests.post(url, data, timeout=30)
    if response.status_code != 200:
        print("HTTP STATUS CODE :", response.status_code)
        return -1
    ddata = json.loads(response.content)
    resultsList = ddata.get('results', {})[0]
    total = resultsList.get('nbHits', 0)
    nbPages = resultsList.get('nbPages', 0)
    print(total, nbPages)
    for i in range(0, nbPages):
        data = template_data.replace('[page=1]','page=' + str(i))
        response = requests.post(url, data, timeout=30)
        if response.status_code != 200:
            print("HTTP STATUS CODE :", response.status_code)
            return -1
        ddata = json.loads(response.content)
        resultsList = ddata.get('results', {})[0]
        total = resultsList.get('nbHits', 0)
        nbPages = resultsList.get('nbPages', 0)
        htisPerPage = resultsList.get('hitsPerPage', 0)
        game_list = resultsList.get('hits', {})
        print("#",i,total, nbPages, htisPerPage, len(game_list))
        for game in game_list:
            info = dict()
            for k,v in  game.items():
                info[k] = clean_value(v)
            print(info['title'])
            datajson = json.dumps(info, ensure_ascii=False)
            headers = {'Content-Type': 'application/json',
                    'auth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjdXRlYyIsImV4cCI6MTYxNzc5MzUyMiwiaWF0IjoxNjE3Nzg2MzIyLCJ1c2VySWQiOiI0In0.AUGxQA3QJ8DgYOnFF5utJ0XBE2I-jUXXkG7Gz_f8kQw'}
            requests.post('http://127.0.0.1/manager/game', headers=headers, data=datajson.encode())

    
if __name__ == "__main__":
    
    url = 'https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id=U3B6GR4UA3&x-algolia-api-key=c4da8be7fd29f0f5bfa42920b0a99dc7'
    # template_data_list = list()
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data) 
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3AStrategy%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3AStrategy%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3AStrategy%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3ASports%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3ASports%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3ASports%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3ASimulation%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3ARole-Playing%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3ARole-Playing%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3ARole-Playing%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3ARacing%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3ARacing%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3ARacing%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3AParty%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3AParty%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3AParty%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3AMusic%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3AMusic%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3AMusic%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&[page=1]&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22genres%3AEducation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22genres%3AEducation%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22genres%3AEducation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)

    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAction%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AEveryone%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AEveryone%2010%2B%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'   
    build_url(url, template_data)
    template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3ATeen%22%5D%2C%5B%22genres%3AAdventure%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'   
    build_url(url, template_data)

    # template_data = '{"requests":[{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=168&maxValuesPerFacet=30&page=0&analytics=false&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22genres%22%2C%22howToShop%22%2C%22virtualConsole%22%2C%22franchises%22%2C%22priceRange%22%2C%22esrbRating%22%2C%22playerFilters%22%5D&tagFilters=&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=esrbRating&facetFilters=%5B%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=playerFilters&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=priceRange&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=genres&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=availability&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22platform%3ANintendo%20Switch%22%5D%5D"},{"indexName":"ncom_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page=0&analytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=platform&facetFilters=%5B%5B%22esrbRating%3AMature%22%5D%2C%5B%22playerFilters%3A1%2B%22%5D%2C%5B%22priceRange%3A%2410%20-%20%2419.99%22%5D%2C%5B%22genres%3AAdventure%22%2C%22genres%3ASimulation%22%5D%2C%5B%22availability%3AAvailable%20now%22%5D%5D"}]}'
    # build_url(url, template_data)
       