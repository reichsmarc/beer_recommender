import requests
import re
from bs4 import BeautifulSoup
from scrapy import Spider, Request


class BeerAdvocateSpider(Spider):
    name = 'beer_advocate'
    custom_settings = dict(CONCURRENT_REQUESTS_PER_DOMAIN=12, HTTPCACHE_ENABLED=True)

    def start_requests(self):
        base_url = 'https://www.beeradvocate.com'
        start_href = '/beer/styles/'
        start_response = requests.get(base_url + start_href)
        soup = BeautifulSoup(start_response.content, 'lxml')
        tags = soup.findAll('a', attrs={'href': re.compile('^/beer/styles/[\\d]')})

        style_dict = dict()
        for tag in tags:
            beer_style = tag.text
            href = tag.get('href')
            style_dict[beer_style] = base_url + href

        # styles = style_dict.keys()
        urls = style_dict.values()

        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        # beer style page(s) have table of beer, brewery, abv, # ratings, and avg. rating
        raw = response.text
        soup = BeautifulSoup(raw, 'lxml')

        table = soup.find('table')
        rows = table.findAll('tr')

        beer_dict = {}
        for row in rows:
            cols = row.findAll('td')
            if len(cols) == 6:
                beer = cols[0].find('a')
                beer_name = beer.text
                beer_href = beer.get('href')

                # brewery = cols[1].find('a')
                # brewery_name = brewery.text
                # brewery_href = brewery.get('href')

                # abv = cols[2].text
                # n_ratings = cols[3].text
                # avg_rating = cols[4].text

                beer_dict[beer_name] = beer_href

        for _, href in beer_dict.items():

            yield response.follow(href, self.parse_beer)

            # next button
            next_beer_page_href = response.xpath('//tr/td/span//*[contains(.,"next")]/@href').extract_first()

            if next_beer_page_href:
                yield response.follow(next_beer_page_href, self.parse)

    def parse_beer(self, response):

        beer_name = response.xpath('//div/h1/text()').extract_first()
        soup = BeautifulSoup(response.text, 'lxml')
        stats = soup.findAll('dd', attrs={'class': 'beerstats'})

        stats0a = stats[0].findAll('a')
        if len(stats0a) == 2:
            style = stats0a[0].text
            style_ranking = stats0a[1].text
        if len(stats0a) == 1:
            style = stats0a[0].text
            style_ranking = None

        stats1b = stats[1].findAll('b')
        abv = stats1b[0].text

        stats2b = stats[2].findAll('b')
        ba_score = stats2b[0].text

        stats2a = stats[2].findAll('a')
        overall_ranking = stats2a[0].text

        stats3span = stats[3].findAll('span')
        r_avg = stats3span[0].text
        r_dev = stats3span[1].text

        stats4span = stats[4].findAll('span')
        n_reviews = stats4span[0].text

        stats5span = stats[5].findAll('span')
        n_ratings = stats5span[0].text

        stats6a = stats[6].findAll('a')
        brewery = stats6a[0].text

        stats7a = stats[7].findAll('a')
        if len(stats7a) == 2:
            state = stats7a[0].text
            country = stats7a[1].text
        if len(stats7a) == 1:
            state = None
            country = stats7a[0].text

        stats8span = stats[8].findAll('span')
        availability = stats8span[0].text

        stats9span = stats[9].findAll('span')
        n_wants = stats9span[0].text

        stats10span = stats[10].findAll('span')
        n_gots = stats10span[0].text

        results_dict = {
                        'beer_name': beer_name,
                        'style': style,
                        'style_ranking': style_ranking,
                        'abv': abv,
                        'ba_score': ba_score,
                        'overall_ranking': overall_ranking,
                        'r_avg': r_avg,
                        'r_dev': r_dev,
                        'n_reviews': n_reviews,
                        'n_ratings': n_ratings,
                        'brewery': brewery,
                        'state': state,
                        'country': country,
                        'availability': availability,
                        'n_wants': n_wants,
                        'n_gots': n_gots
                        }

        yield results_dict

        # for review in response.xpath('//div[@id="rating_fullview_container"]'):
        #     review_score = review.xpath('*//span[@class="BAscore_norm"]/text()').extract_first()
        #     review_deviation = review.xpath('*//span[@style="color:#006600;"]/text()').extract_first()
        #     username = review.xpath('*//span[@class="muted"]/a[@class="username"]/text()').extract_first()
        #     date = review.xpath('*//span[@class="muted"]/a[2]/text()').extract_first()
        #     review_text = review.xpath('*[@id="rating_fullview_content_2"]/text()').extract()
        #
        #     muted = review.xpath('*//span[@class="muted"]/text()').extract_first()
        #     try:
        #         muted = muted.split('|')
        #         look = muted[0]
        #         smell = muted[1]
        #         taste = muted[2]
        #         feel = muted[3]
        #         overall = muted[4]
        #     except:
        #         look = None
        #         smell = None
        #         taste = None
        #         feel = None
        #         overall = None
        #
        # yield {
        #     'beername': beer_name,
        #     'brewery': brewery,
        #     'style': style,
        #     'abv': abv,
        #     'avgreviewscore': avg_review_score,
        #     'reviewscore': review_score,
        #     'reviewdeviation': review_deviation,
        #     'reviewtext': review_text,
        #     'username': username,
        #     'date': date,
        #     'look': look,
        #     'smell': smell,
        #     'tase': taste,
        #     'feel': feel,
        #     'overall': overall
        #     'overall': overall
        #     }

        next_review = response.xpath('//div/span/*[contains(.,"next")]/@href').extract_first()
        if next_review:
            yield response.follow(next_review, self.parse_beer)
