import scrapy
from requests.utils import quote,unquote
import json
from webextractor.items import NYTimesPerUserCommentItem
import datetime 
import pickle

name_id_dict = pickle.load(open('nytimes_name_id_dict.p', 'rb'))

def generate_starturls():
    list = []	
    global name_id_dict
    for name in name_id_dict:
	id_list = name_id_dict[name]

	for id in id_list:
		url = 'http://api.nytimes.com/svc/community/v3/user-content/user.json?userID='+ str(id) +'&api-key=9ad1450c5a9f230ae5db72e287338b09:19:73093276'
		if url not in list:
			list.append(url)

    return list

class NYTimesPeruserSpider(scrapy.Spider):
    name = "nytimes_peruser"
    allowed_domains = ["api.nytimes.com"]


    start_urls = generate_starturls()
    #start_urls = [
#'http://api.nytimes.com/svc/community/v3/user-content/user.json?userID=1023951&api-key=9ad1450c5a9f230ae5db72e287338b09:19:73093276'
#] 


    def parse(self, response):
	jsonresponse = json.loads(response.body_as_unicode())
	
	global name_id_dict
	name = jsonresponse['results']['comments'][0]['userSubmittedDisplayName']
	if name in name_id_dict:
		pages = int(jsonresponse['results']['totalCommentsFound']) 
		#if pages > 500:
		#	pages = 500
		original_url = response.url

		for i in range(0,pages,25):
			url = original_url + '&offset='	+ str(i)
			yield scrapy.Request(url, callback=self.parse_page_comments,dont_filter=True)


    def parse_page_comments(self, response):
	jsonresponse = json.loads(response.body_as_unicode())

	for i in range(len(jsonresponse['results']['comments'])):
		item = NYTimesPerUserCommentItem()
		comment = jsonresponse['results']['comments'][i]

		item['article'] = comment['asset']['assetURL'] if 'assetURL' in comment['asset'] else 'null'
		item['article_url'] = comment['asset']['taxonomy'] if 'taxonomy' in comment['asset'] else 'null'
		
		item['comment_id'] = comment['commentID'] 
		item['author_name'] = comment['userSubmittedDisplayName']
		item['author_id'] = comment['userID']

		item['text'] = comment['commentBody']
    		item['date_js_timestamp']= comment['createDate']
		dt = datetime.datetime.fromtimestamp(int(comment['createDate']))

		item['date'] = dt.strftime('%d %b %Y %H:%M')
		item['number_of_votes'] = comment['recommendations']

		yield item
