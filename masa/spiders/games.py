import json
import scrapy
from ..items import Category, Game


class GamesSpider(scrapy.Spider):
    name = 'games'
    start_urls = ['https://www.old-games.org/categories']
    base_url = 'https://www.old-games.org'

    def parse(self, response):
        categories = response.xpath("//div[@class='cat_slideshow']/descendant::node()/a")

        for category in categories:
            cat_name = category.xpath(".//text()").get()
            url = self.base_url + category.xpath(".//@href").get()    
            
            cat = Category()
            cat['category'] = cat_name
            
            yield response.follow(url=url, callback=self.parse_category, meta={ 'category': cat })

    def parse_category(self, response):
        games_url_list = response.xpath('//table[@id="table_games_id"]/descendant::node()/td[2]/a/@href').getall()

        cat = response.meta['category']
        url = self.base_url + games_url_list.pop()
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        
        if next_page:
            next_page = self.base_url + response.xpath('//a[@rel="next"]/@href').get()

        yield response.follow(url=url, callback=self.parse_game, meta={'category': cat, 'games_url_list': games_url_list, 'next_page': next_page})
            
    def parse_game(self, response):
        cat = response.meta['category']
        game = Game()

        try:
            cat['games_list']
        except:
            cat['games_list'] = []
        
        game_info = response.xpath('//td[@class="game_specs"]')
        
        game['category'] = cat['category']
        game['title_en'] = response.xpath('//h1[@class="game_title"]/a/text()').get()
        game['title_he'] = response.xpath('//h2[@class="game_title"]/a/text()').get()
        game['os'], game['num_of_players'] = (game_info.xpath('.//a/text()').getall())[1:3]
        game['admin_rating'] = game_info[2].xpath('.//text()').get()
        game['users_rating'] = game_info[3].xpath('.//text()').get()
        game['size'] = game_info[5].xpath('.//text()').get()
        
        pub_info = response.xpath('//div[@id="game_dev_and_pub"]/descendant::node()/dd')
        game['release_year'] = '' if pub_info[0].xpath('.//a/text()').get() is None else pub_info[0].xpath('.//a/text()').get()
        game['developer'] = '' if pub_info[1].xpath('.//a/text()').get() is None else pub_info[1].xpath('.//a/text()').get()
        game['publisher'] = '' if pub_info[2].xpath('.//a/text()').get() is None else pub_info[2].xpath('.//a/text()').get()
        
        # game['review'] = ''.join(response.xpath('//div[@id="game_review"]/p/text()').getall())
        review = ''
        for val in response.xpath('//div[@id="game_review"]/p'):
            review += val.xpath('normalize-space(./text())').get()
        
        game['review'] = review
        game['keywords'] = response.xpath('//li[contains(text(), "מפתח")]/a/text()').getall()
        game['more_in_series'] = response.xpath('//li[contains(text(), "משחקים נוספים ב")]/descendant::node()[contains(@href, "games")]/text()').getall()
        game['similar_games'] = response.xpath('//li[contains(text(), "משחקים דומים")]/a[contains(@href, "games")]/text()').getall()
 
        cat['games_list'].append(game)

        games_url_list = response.meta['games_url_list']
        next_page = response.meta['next_page']
        if games_url_list: 
            url = self.base_url + games_url_list.pop()
            yield response.follow(url=url, callback=self.parse_game, meta={'category': cat, 'games_url_list': games_url_list, 'next_page': next_page})

        else:
            if next_page:
                yield response.follow(url=next_page, callback=self.parse_category, meta={'category': cat})
            else:
                yield cat