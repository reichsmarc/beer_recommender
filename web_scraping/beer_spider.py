import requests
import re
from bs4 import BeautifulSoup
import scrapy

class BeerAdvocateSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'beer_advocate'
        self.custom_settings = dict(CONCURRENT_REQUESTS_PER_DOMAIN=12, HTTPCACHE_ENABLED=True)
        self.style_dict = {}
        self.start_urls = []

    def getStartUrls(self):
        base_url = 'https://www.beeradvocate.com'
        start_href = '/beer/styles/'
        response = requests.get(base_url + start_href)
        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.findAll('a', attrs={'href': re.compile('^/beer/styles/[\\d]')})

        for tag in tags:
            beer_style = tag.text
            href = tag.get('href')
            self.style_dict[beer_style] = base_url + href

        self.start_urls = self.style_dict.keys()

    def parse(self, response):
        beers = response.xpath('//tr/td/a/@href').extract()[6::3]

        for href in beers:
            yield response.follow(href, self.parse_beer)

            next_beer = response.xpath('//tr/td/span//*[contains(.,"next")]/@href').extract_first()
            beercount = int(next_beer.split('start=')[1]) # URL beercount on next button
            if (beercount < 150):
                yield response.follow(next_beer, self.parse)
            else:
                next

    def parse_beer(self, response):
        beer_name = response.xpath('//div/h1/text()').extract_first()
        brewery = response.xpath('//h1/span/text()').extract_first()
        style = response.xpath('//div[@class="break"]/a[contains(@href,"style")]/b/text()').extract_first()
        abv = response.xpath('//div[@class="break"]/b[4]/following-sibling::text()').extract_first()
        avg_review_score = response.xpath('//div[@id="item_stats"]/dl/dd[3]/span/text()').extract_first()

        for review in response.xpath('//div[@id="rating_fullview_container"]'):
            review_score = review.xpath('*//span[@class="BAscore_norm"]/text()').extract_first()
            review_deviation = review.xpath('*//span[@style="color:#006600;"]/text()').extract_first()
            username = review.xpath('*//span[@class="muted"]/a[@class="username"]/text()').extract_first()
            date = review.xpath('*//span[@class="muted"]/a[2]/text()').extract_first()
            review_text = review.xpath('*[@id="rating_fullview_content_2"]/text()').extract()

            muted = review.xpath('*//span[@class="muted"]/text()').extract_first()
            try:
                muted = muted.split('|')
                look = muted[0]
                smell = muted[1]
                taste = muted[2]
                feel = muted[3]
                overall = muted[4]
            except:
                look = None
                smell = None
                taste = None
                feel = None
                overall = None

        yield {
            'beername': beer_name,
            'brewery': brewery,
            'style': style,
            'abv': abv,
            'avgreviewscore': avg_review_score,
            'reviewscore': review_score,
            'reviewdeviation': review_deviation,
            'reviewtext': review_text,
            'username': username,
            'date': date,
            'look': look,
            'smell': smell,
            'tase': taste,
            'feel': feel,
            'overall': overall
            }

        next_review = response.xpath('//div/span/*[contains(.,"next")]/@href').extract_first()
        reviewcount = int(next_review.split('start=')[1]) # URL reviewcount on next button
        if (reviewcount < 500): # when next button >= max, next page is not returned
            yield response.follow(next_review, self.parse_beer)
        else:
            next