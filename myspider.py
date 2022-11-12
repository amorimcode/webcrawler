from urllib.parse import urljoin
import scrapy
import json


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
        
        self.marcas.append({'name': brand, 'gbin': gbin, 'site': site})
    
        write_results_file(self.marcas)

    def close(self, reason):
        print('Acabou, meu patrão!')
