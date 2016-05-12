import scrapy
from webextractor.items import GuardianPerUserCommentItem
import datetime 
import json
from BeautifulSoup import  BeautifulSoup
import pickle

name_id_dict = pickle.load(open('guardian_name_id_dict.p', 'rb'))

def generate_starturls():
    list = []	
    global name_id_dict
    for name in name_id_dict:
	id_list = name_id_dict[name]

	for id in id_list:
		url = 'https://api.nextgen.guardianapps.co.uk/discussion/profile/'+ str(id) +'/discussions.json'
		if url not in list:
			list.append(url)

    return list


def generateitems(comment,user_id,user_name):
	article = comment.find('div',{'class':'activity-item__title'}).find('a').text
	article_url = comment.find('div',{'class':'activity-item__title'}).find('a')['href']
	item_list = []	

	comments =  comment.findAll('div',{'class':'activity-item__content '})
	for eachcomment in comments:
		item = generateitem(eachcomment,user_id,user_name,article,article_url)
		item_list.append(item)

	comments =  comment.findAll('div',{'class':'activity-item__content activity-item__content--no-border'})
	for eachcomment in comments:
		item = generateitem(eachcomment,user_id,user_name,article,article_url)
		item_list.append(item)
	return item_list

def generateitem(comment,user_id,user_name,article,article_url):
	item = GuardianPerUserCommentItem()
	article = article
	article_url = article_url
	item['article'] = article
	item['article_url'] = article_url
	
	date = comment.find('time',{'class':'disc-comment__date-published'}).find('a').text
	date_js_timestamp = comment.find('time',{'class':'disc-comment__date-published'})['data-timestamp']
	item['date'] = date
	item['date_js_timestamp'] = date_js_timestamp
	
	comment_id = comment.find('a',{'class':'disc-comment__view-discussion js-comment-permalink'})['data-comment-id']
	item['comment_id'] = comment_id

	number_of_votes = comment.find('div',{'class':'disc-comment__recommend-count js-disc-recommend-count'}).text
	item['number_of_votes'] = number_of_votes
	text = ''	
	for p in comment.findAll('p'):
		text = text + p.text + '\n'
	item['text'] = text

	item['author_id'] = user_id
	item['author_name'] = user_name

	return item

class GuardianPeruserSpider(scrapy.Spider):
    name = "guardian_peruser"
    allowed_domains = ["api.nextgen.guardianapps.co.uk"]

    start_urls = generate_starturls()
    #start_urls = ['https://api.nextgen.guardianapps.co.uk/discussion/profile/13230742/discussions.json'] 

    def parse(self, response):
	origin_url = response.url
	global name_id_dict

	user_id = int(origin_url.split('/')[-2])
	user_name = ''
	for name in name_id_dict:
		if user_id in name_id_dict[name]:
			user_name = name

	for i in range(1,15,1):
		url = origin_url + '?page=' + str(i)
		yield scrapy.Request(url, callback=self.parse_page_comments,dont_filter=True,meta = {'user_id': user_id,'user_name':user_name})
  
    def parse_page_comments(self, response):
	user_id = response.meta['user_id']
	user_name = response.meta['user_name']

	jsonresponse = json.loads(response.body_as_unicode())
	html = jsonresponse['html']
	soup = BeautifulSoup(html)
	
	comments =  soup.findAll('div',{'class':'activity-stream__item activity-item activity-item--first'})
	for comment in comments:
		item_list = generateitems(comment,user_id,user_name)
		for item in item_list:
			yield item

	comments =  soup.findAll('div',{'class':'activity-stream__item activity-item '})
	for comment in comments:
		item_list = generateitems(comment,user_id,user_name)
		for item in item_list:
			yield item
	
