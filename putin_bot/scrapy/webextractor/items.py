# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


'''class WebextractorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass'''

class GuardianCommentItem(scrapy.Item):
    article = scrapy.Field()
    article_url = scrapy.Field()
    comment_id = scrapy.Field()

    author_name = scrapy.Field()
    author_id = scrapy.Field()	
    author_profile_url = scrapy.Field()

    text = scrapy.Field()
    date = scrapy.Field()
    date_js_timestamp = scrapy.Field()
    number_of_votes = scrapy.Field()
 
    reply_user_name = scrapy.Field()
    reply_comment_id = scrapy.Field()


class GuardianPerUserCommentItem(scrapy.Item):
    article = scrapy.Field()
    article_url = scrapy.Field()
	
    comment_id = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()	

    text = scrapy.Field()
    date = scrapy.Field()
    date_js_timestamp = scrapy.Field()
    number_of_votes = scrapy.Field()
 

class NYTimesCommentItem(scrapy.Item):
    article = scrapy.Field()
    article_url = scrapy.Field()
    comment_id = scrapy.Field()

    author_name = scrapy.Field()
    author_id = scrapy.Field()	
    #author_profile_url = scrapy.Field()

    text = scrapy.Field()
    date = scrapy.Field()
    date_js_timestamp = scrapy.Field()
    number_of_votes = scrapy.Field()
 
    reply_user_name = scrapy.Field()
    reply_comment_id = scrapy.Field()

class NYTimesPerUserCommentItem(scrapy.Item):
    article = scrapy.Field()
    article_url = scrapy.Field()
    comment_id = scrapy.Field()

    author_name = scrapy.Field()
    author_id = scrapy.Field()	

    text = scrapy.Field()
    date = scrapy.Field()
    date_js_timestamp = scrapy.Field()
    number_of_votes = scrapy.Field()
 
