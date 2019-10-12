import requests
import re
from bs4 import BeautifulSoup
from scrapy import Spider, Request
import logging

logger = logging.getLogger(__name__)


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

        url = response.request.url
        beer_name = response.xpath('//div/h1/text()').extract_first()

        # beer stats table
        soup = BeautifulSoup(response.text, 'lxml')
        stats = soup.findAll('dd', attrs={'class': 'beerstats'})

        stats0a = stats[0].findAll('a')
        if len(stats0a) == 2:
            style = stats0a[0].text
            style_ranking = stats0a[1].text
        elif len(stats0a) == 1:
            style = stats0a[0].text
            style_ranking = None
        else:
            style = None
            style_ranking = None

        stats1b = stats[1].findAll('b')
        if stats1b:
            abv = stats1b[0].text
        else:
            abv = None

        stats2b = stats[2].findAll('b')
        if stats2b:
            ba_score = stats2b[0].text
        else:
            ba_score = None

        stats2a = stats[2].findAll('a')
        if stats2a:
            overall_ranking = stats2a[0].text
        else:
            overall_ranking = None

        stats3span = stats[3].findAll('span')
        r_avg = stats3span[0].text
        pdev = stats3span[1].text

        stats4span = stats[4].findAll('span')
        if stats4span:
            n_reviews = stats4span[0].text
        else:
            n_reviews = None

        stats5span = stats[5].findAll('span')
        if stats5span:
            n_ratings = stats5span[0].text
        else:
            n_ratings = None

        stats6a = stats[6].findAll('a')
        if stats6a:
            brewery = stats6a[0].text
        else:
            brewery = None

        stats7a = stats[7].findAll('a')
        if len(stats7a) == 2:
            state = stats7a[0].text
            country = stats7a[1].text
        elif len(stats7a) == 1:
            state = None
            country = stats7a[0].text
        else:
            state = None
            country = None

        stats8span = stats[8].findAll('span')
        if stats8span:
            availability = stats8span[0].text
        else:
            availability = None

        stats9span = stats[9].findAll('span')
        if stats9span:
            n_wants = stats9span[0].text
        else:
            n_wants = None

        stats10span = stats[10].findAll('span')
        if stats10span:
            n_gots = stats10span[0].text
        else:
            n_gots = None

        div = soup.findAll('div', attrs={'id': 'rating_fullview_container'})
        for review in div:
            r1 = review.findAll('span', attrs={'class': 'BAscore_norm'})
            if r1:
                ba_score_norm = r1[0].text
            else:
                ba_score_norm = None

            r2 = review.findAll('span', attrs={'class': 'rAvg_norm'})
            if r2:
                r_avg_norm = r2[0].text
            else:
                r_avg_norm = None

            r3 = review.findAll('span', attrs={'style': re.compile(r'^color:#\d+')})
            if r3:
                r_dev_rating = r3[0].text
            else:
                r_dev_rating = None

            muted = review.findAll('span', attrs={'class': re.compile('muted')})
            if muted and '|' in muted[0].text:
                try:
                    ratings_bar = muted[0].text
                except IndexError:
                    ratings_bar = None

                try:
                    characters = muted[1].text
                except IndexError:
                    characters = None

                try:
                    username = muted[2].find('a').text
                except IndexError:
                    username = None

                try:
                    review_date = muted[2].findAll('a', attrs={'href': re.compile('#review')})[0].text
                except IndexError:
                    review_date = None
            else:
                ratings_bar = None
                characters = None
                username = None
                review_date = None

            try:
                all_text = str(review).split('<br/>')
                review_text = [x for x in all_text if '<' not in x]
                review_text = ''.join([x for x in review_text if x != ''])
            except IndexError:
                review_text = None

            results_dict = {
                            'url': url,
                            'beer_name': beer_name,
                            'style': style,
                            'style_ranking': style_ranking,
                            'abv': abv,
                            'ba_score': ba_score,
                            'overall_ranking': overall_ranking,
                            'r_avg': r_avg,
                            'pdev': pdev,
                            'n_reviews': n_reviews,
                            'n_ratings': n_ratings,
                            'brewery': brewery,
                            'state': state,
                            'country': country,
                            'availability': availability,
                            'n_wants': n_wants,
                            'n_gots': n_gots,
                            'BAscore_norm': ba_score_norm,
                            'rAvg_norm': r_avg_norm,
                            'r_dev_rating': r_dev_rating,
                            'ratings_bar': ratings_bar,
                            'characters': characters,
                            'username': username,
                            'review_date': review_date,
                            'review_text': review_text
                            }

            yield results_dict

        next_review = response.xpath('//div/span/*[contains(.,"next")]/@href').extract_first()
        if next_review:
            yield response.follow(next_review, self.parse_beer)
