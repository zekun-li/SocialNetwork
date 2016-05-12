import scrapy
import w3lib.url

def generate_starturls(url,pages):
	list = []
	list.append(url)
	for i in range(1,pages):
		list.append(url+'&start='+str(i*10))
	return list

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    url = "https://www.google.com/search?q=Putin+Russia+Ukraine+site:theguardian.com"
    pages = 52
    #url = "https://www.google.com/search?q=Putin+OR+Russia+site:nytimes.com"
    #pages = 67
    start_urls = generate_starturls(url,pages)

    def parse(self, response):
	 for href in response.xpath('//h3[@class="r"]/a/@href').extract():
		print w3lib.url.url_query_parameter(href, "q")



