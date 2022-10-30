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
    print(start_urls)
    marcas = list()

    def parse(self, response):
        for name in response.css('.rankingName'):
            brand = name.css('::text').get()
            self.marcas.append({'name': brand})
            yield {'name': brand}

        for href in response.css('.brandLine a::attr(href)'):
            yield response.follow(href, self.parse_dir_contents)

    def parse_dir_contents(self, response):
        print(response.url)
    #   for sel in response.xpath('//ul/li'):
    #      item['title'] = sel.xpath('a/text()').extract()
    #      item['link'] = sel.xpath('a/@href').extract()
    #      item['desc'] = sel.xpath('text()').extract()
    #      yield item        

    def close(self, reason):
        write_results_file(self.marcas)
