# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Category(scrapy.Item):
    category = scrapy.Field()
    games_list = scrapy.Field()

class Game(scrapy.Item):
    category = scrapy.Field()
    title_en = scrapy.Field()
    title_he = scrapy.Field()
    category = scrapy.Field()
    os = scrapy.Field()
    admin_rating = scrapy.Field()
    users_rating = scrapy.Field()
    num_of_players = scrapy.Field()
    size = scrapy.Field()
    release_year = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    review = scrapy.Field()
    keywords = scrapy.Field()
    more_in_series = scrapy.Field()
    similar_games = scrapy.Field()
    
