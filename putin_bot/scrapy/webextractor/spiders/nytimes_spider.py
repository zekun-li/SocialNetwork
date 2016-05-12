import scrapy
from requests.utils import quote,unquote
import json
from webextractor.items import NYTimesCommentItem
import datetime 

def generate_API_url(url,APIkey):
    encoded_url = quote(url.strip(), safe='')
    return "http://api.nytimes.com/svc/community/v3/user-content/url.json?api-key="+ APIkey + "&url=" + encoded_url

def generate_starturls(filename):
    list = []	
    with open(filename, "r") as f:
	for line in f:
        	list.append(line.strip())
    return list

class NYTimesSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["api.nytimes.com"]

    start_urls = generate_starturls("nytimes_new_url.txt")
    #start_urls = generate_starturls("nytimes_urls.txt")
    #start_urls =[
#'http://www.nytimes.com/2015/09/29/world/middleeast/obama-and-putin-clash-at-un-over-syria-crisis.html'
   #]

    def parse(self, response):
	article_url = response.url 
	if article_url[-5:] == '?_r=0':
		article_url = article_url[:-5]

	article = response.xpath('//title/text()').extract()[0]
	APIkey = '9ad1450c5a9f230ae5db72e287338b09:19:73093276'
	api_url = generate_API_url(article_url,APIkey)
	yield scrapy.Request(api_url, callback=self.parse_comments,dont_filter=True,meta = {'article_url': article_url,'article':article})

    def parse_comments(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

	pages = int(jsonresponse['results']['totalParentCommentsFound']) 
	original_url = response.url

	for i in range(0,pages,25):
		url = original_url + '&offset='	+ str(i)
		yield scrapy.Request(url, callback=self.parse_page_comments,dont_filter=True,meta = {'article_url': response.meta['article_url'],'article':response.meta['article']})
		
    def parse_page_comments(self, response):
	jsonresponse = json.loads(response.body_as_unicode())
	article_url = response.meta['article_url']
	article = response.meta['article']

	for i in range(len(jsonresponse['results']['comments'])):
		item = NYTimesCommentItem()
		item['article'] = article
		item['article_url'] = article_url
		
		comment = jsonresponse['results']['comments'][i]
		item['comment_id'] = comment['commentID'] 
		item['author_name'] = comment['userDisplayName']
		item['author_id'] = comment['userID']

		item['text'] = comment['commentBody']
    		item['date_js_timestamp']= comment['createDate']
		dt = datetime.datetime.fromtimestamp(int(comment['createDate']))

		item['date'] = dt.strftime('%d %b %Y %H:%M')
		item['number_of_votes'] = comment['recommendations']
		
		item['reply_user_name'] =''
		item['reply_comment_id'] =''
		
		yield item

		for j in range(len(comment['replies'])):
			reply_item = NYTimesCommentItem()
			reply_item['article'] = article
			reply_item['article_url'] = article_url
		
			reply_comment = comment['replies'][j]
			reply_item['comment_id'] = reply_comment['commentID'] 
			reply_item['author_name'] = reply_comment['userDisplayName']
			reply_item['author_id'] = reply_comment['userID']

			reply_item['text'] = reply_comment['commentBody']
	    		reply_item['date_js_timestamp']= reply_comment['createDate']
			dt = datetime.datetime.fromtimestamp(int(reply_comment['createDate']))

			reply_item['date'] = dt.strftime('%d %b %Y %H:%M')
			reply_item['number_of_votes'] = reply_comment['recommendations']
		
			reply_item['reply_user_name'] =reply_comment['parentUserDisplayName']
			reply_item['reply_comment_id'] =reply_comment['parentID']
	
			yield reply_item
