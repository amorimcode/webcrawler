from urllib.parse import urljoin
import scrapy
import json
import base64
import requests


def write_results_file(marcas):
    marcas_ordenadas = sorted(marcas, key=lambda d: d['name'])
    jsonstring = json.dumps(marcas_ordenadas)
    jsonfile = open('marcas.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    base_url = 'https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter='
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVXWYZ'
    urls = list()
    for l in alfabeto:
        urls.append(base_url + l)
    return urls


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = urls_brands()
    marcas = list()

    def parse(self, response):
        for href in response.css('.brandLine a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)

    def parse_dir_contents(self, response):
        brand = response.css('.brandName span::text').get()
        gbin = response.css('.brandInfoText span::text').get()
        site = response.css('.brandInfoText a::text').get()
        imgUrl = 'https://www.rankingthebrands.com/' + response.css('.brandLogo img::attr(src)').get()
        base64Img = str(base64.b64encode(requests.get(imgUrl).content))
        country = response.css('.brandInfoText span::text')[2].get()
        rtbScore = response.css('.brandInfoText span::text')[1].get()
        
        self.marcas.append({'name': brand, 'gbin': gbin, 'site': site, 'imgBase64': base64Img, 'country': country, 'rtbScore': rtbScore})
    
        write_results_file(self.marcas)

    def close(self, reason):
        print('Acabou, meu patrão!')
