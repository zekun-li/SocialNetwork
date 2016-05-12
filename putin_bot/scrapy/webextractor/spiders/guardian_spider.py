import scrapy
from webextractor.items import GuardianCommentItem

def generate_starturls(filename):
    list = []	
    with open(filename, "r") as f:
	for line in f:
        	list.append(line.strip())
    return list

class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    #start_urls = generate_starturls("guardian_urls.txt")
    start_urls = generate_starturls("guardian_new_url.txt")
    #start_urls =["http://www.theguardian.com/commentisfree/2015/aug/30/the-guardian-view-on-the-latest-ukraine-ceasefire-call-why-this-could-be-the-one-that-works"]

    '''def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)'''

    def parse(self, response):
        for href in response.xpath('//h2[@class="container__meta__title"]/a/@href'):
        	url = response.urljoin(href.extract())
            	yield scrapy.Request(url, callback=self.parse_comments_all_pages,dont_filter=True)


    def parse_comments_all_pages(self, response):
	page_number = int(response.xpath('//a[@class="button button--small button--tertiary pagination__action pagination__action--last js-discussion-change-page"]/text()').extract()[0])
	
	for i in range(1,page_number+1):
		if i == 1:
			url = response.url
			#yield scrapy.Request(url, callback=self.parse_comments_page,dont_filter=True)
		else:
			url = response.url + '?page=' + str(i)
		yield scrapy.Request(url, callback=self.parse_comments_page,dont_filter=True)


    def parse_comments_page(self, response):
	article = response.xpath('//h1[@class="content__headline"]/a/text()').extract()[0]
	article_url = response.xpath('//h1[@class="content__headline"]/a/@href').extract()[0]

	for sel in response.xpath('//ul[@class="d-thread d-thread--comments js-new-comments"]/li'):
		item = GuardianCommentItem()
		item['article'] = article
		item['article_url'] = article_url
    		
		item['comment_id'] = sel.xpath('@data-comment-id').extract()[0]
		item['author_name'] = sel.xpath('.//span[@itemprop="givenName"]/text()').extract()[0]
		item['author_id'] = sel.xpath('@data-comment-author-id').extract()[0]
		item['author_profile_url'] = sel.xpath('.//a[@itemprop="url"]/@href').extract()[0]	
		item['text'] = self.combine_text(sel.xpath('.//p/text()').extract())
		item['date'] = sel.xpath('.//time[@class="js-timestamp"]/text()').extract()[0]
		item['date_js_timestamp'] = sel.xpath('.//time[@class="js-timestamp"]/@data-timestamp').extract()[0]
		
		number_of_votes= sel.xpath('.//span[@class="d-comment__recommend-count--old"]/text()').extract()
		item['number_of_votes'] = number_of_votes[0] if number_of_votes else 0 

		reply_user_name = sel.xpath('.//span[@class="d-comment__reply-to-author"]/text()').extract()
		item['reply_user_name'] = reply_user_name[0] if reply_user_name else ''  
		
		reply_comment_id = sel.xpath('.//a[@class="js-discussion-author-link"]/@href').extract()
		
		item['reply_comment_id'] = reply_comment_id[0].split('-')[1] if reply_comment_id else '' 
		
		yield item

    def combine_text(self,list):
	text = ""
	for i in range(len(list)):
		text = text + list[i] + '\n'
	return text 

   
