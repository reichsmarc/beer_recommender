import scrapy
from myproject.items import MyItem


class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)


class beerSpider(scrapy.Spider):
    name = 'beeradvocate2'

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 12,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://www.beeradvocate.com/beer/style/128/',
                  'https://www.beeradvocate.com/beer/style/19/',
                  'https://www.beeradvocate.com/beer/style/175/',
                  'https://www.beeradvocate.com/beer/style/99/',
                  'https://www.beeradvocate.com/beer/style/73/',
                  'https://www.beeradvocate.com/beer/style/94/',
                  'https://www.beeradvocate.com/beer/style/140/',
                  'https://www.beeradvocate.com/beer/style/157/',
                  'https://www.beeradvocate.com/beer/style/116/',
                  'https://www.beeradvocate.com/beer/style/97/',
                  'https://www.beeradvocate.com/beer/style/93/',
                  'https://www.beeradvocate.com/beer/style/159/',
                  'https://www.beeradvocate.com/beer/style/158/',
                  'https://www.beeradvocate.com/beer/style/78/',
                  'https://www.beeradvocate.com/beer/style/171/',
                  'https://www.beeradvocate.com/beer/style/130/',
                  'https://www.beeradvocate.com/beer/style/163/',
                  'https://www.beeradvocate.com/beer/style/6/',
                  'https://www.beeradvocate.com/beer/style/72/',
                  'https://www.beeradvocate.com/beer/style/12/',
                  'https://www.beeradvocate.com/beer/style/60/',
                  'https://www.beeradvocate.com/beer/style/119/',
                  'https://www.beeradvocate.com/beer/style/174/',
                  'https://www.beeradvocate.com/beer/style/54/',
                  'https://www.beeradvocate.com/beer/style/56/',
                  'https://www.beeradvocate.com/beer/style/55/',
                  'https://www.beeradvocate.com/beer/style/141/',
                  'https://www.beeradvocate.com/beer/style/127/',
                  'https://www.beeradvocate.com/beer/style/57/',
                  'https://www.beeradvocate.com/beer/style/15/',
                  'https://www.beeradvocate.com/beer/style/52/',
                  'https://www.beeradvocate.com/beer/style/53/',
                  'https://www.beeradvocate.com/beer/style/14/',
                  'https://www.beeradvocate.com/beer/style/10/',
                  'https://www.beeradvocate.com/beer/style/50/',
                  'https://www.beeradvocate.com/beer/style/142/',
                  'https://www.beeradvocate.com/beer/style/129/',
                  'https://www.beeradvocate.com/beer/style/58/',
                  'https://www.beeradvocate.com/beer/style/48/',
                  'https://www.beeradvocate.com/beer/style/80/',
                  'https://www.beeradvocate.com/beer/style/114/',
                  'https://www.beeradvocate.com/beer/style/152/',
                  'https://www.beeradvocate.com/beer/style/98/',
                  'https://www.beeradvocate.com/beer/style/74/',
                  'https://www.beeradvocate.com/beer/style/75/',
                  'https://www.beeradvocate.com/beer/style/150/',
                  'https://www.beeradvocate.com/beer/style/154/',
                  'https://www.beeradvocate.com/beer/style/76/',
                  'https://www.beeradvocate.com/beer/style/101/',
                  'https://www.beeradvocate.com/beer/style/13/',
                  'https://www.beeradvocate.com/beer/style/165/',
                  'https://www.beeradvocate.com/beer/style/66/',
                  'https://www.beeradvocate.com/beer/style/95/',
                  'https://www.beeradvocate.com/beer/style/82/',
                  'https://www.beeradvocate.com/beer/style/69/',
                  'https://www.beeradvocate.com/beer/style/79/',
                  'https://www.beeradvocate.com/beer/style/84/',
                  'https://www.beeradvocate.com/beer/style/47/',
                  'https://www.beeradvocate.com/beer/style/148/',
                  'https://www.beeradvocate.com/beer/style/86/',
                  'https://www.beeradvocate.com/beer/style/87/',
                  'https://www.beeradvocate.com/beer/style/91/',
                  'https://www.beeradvocate.com/beer/style/16/',
                  'https://www.beeradvocate.com/beer/style/89/',
                  'https://www.beeradvocate.com/beer/style/85/',
                  'https://www.beeradvocate.com/beer/style/90/',
                  'https://www.beeradvocate.com/beer/style/18/',
                  'https://www.beeradvocate.com/beer/style/92/',
                  'https://www.beeradvocate.com/beer/style/162/',
                  'https://www.beeradvocate.com/beer/style/161/',
                  'https://www.beeradvocate.com/beer/style/173/',
                  'https://www.beeradvocate.com/beer/style/77/',
                  'https://www.beeradvocate.com/beer/style/68/',
                  'https://www.beeradvocate.com/beer/style/70/',
                  'https://www.beeradvocate.com/beer/style/38/',
                  'https://www.beeradvocate.com/beer/style/147/',
                  'https://www.beeradvocate.com/beer/style/164/',
                  'https://www.beeradvocate.com/beer/style/42/',
                  'https://www.beeradvocate.com/beer/style/155/',
                  'https://www.beeradvocate.com/beer/style/132/',
                  'https://www.beeradvocate.com/beer/style/39/',
                  'https://www.beeradvocate.com/beer/style/5/',
                  'https://www.beeradvocate.com/beer/style/40/',
                  'https://www.beeradvocate.com/beer/style/149/',
                  'https://www.beeradvocate.com/beer/style/37/',
                  'https://www.beeradvocate.com/beer/style/43/',
                  'https://www.beeradvocate.com/beer/style/32/',
                  'https://www.beeradvocate.com/beer/style/35/',
                  'https://www.beeradvocate.com/beer/style/20/',
                  'https://www.beeradvocate.com/beer/style/36/',
                  'https://www.beeradvocate.com/beer/style/41/',
                  'https://www.beeradvocate.com/beer/style/131/',
                  'https://www.beeradvocate.com/beer/style/33/',
                  'https://www.beeradvocate.com/beer/style/29/',
                  'https://www.beeradvocate.com/beer/style/46/',
                  'https://www.beeradvocate.com/beer/style/21/',
                  'https://www.beeradvocate.com/beer/style/7/',
                  'https://www.beeradvocate.com/beer/style/31/',
                  'https://www.beeradvocate.com/beer/style/30/',
                  'https://www.beeradvocate.com/beer/style/168/',
                  'https://www.beeradvocate.com/beer/style/169/',
                  'https://www.beeradvocate.com/beer/style/9/',
                  'https://www.beeradvocate.com/beer/style/8/',
                  'https://www.beeradvocate.com/beer/style/11/']

    def parse(self, response):
        beers = response.xpath('//tr/td/a/@href').extract()[6::3]

        for href in beers:
            yield response.follow(href, self.parse_beer)

            next_beer = response.xpath('//tr/td/span//*[contains(.,"next")]/@href').extract_first()
            beercount = int(next_beer.split('start=')[1])  # URL beercount on next button
            if (beercount < 150):
                yield response.follow(next_beer, self.parse)
            else:
                next

    def parse_beer(self, response):
        # check if we can yield this into a different file
        # if not, just do open('filename') etc.. and save as JSON
        beer_name = response.xpath('//div/h1/text()').extract_first()
        brewery = response.xpath('//h1/span/text()').extract_first()
        style = response.xpath('//div[@class="break"]/a[contains(@href,"style")]/b/text()').extract_first()
        abv = response.xpath('//div[@class="break"]/b[4]/following-sibling::text()').extract_first()
        avg_review_score = response.xpath('//div[@id="item_stats"]/dl/dd[3]/span/text()').extract_first()

        for review in response.xpath('//div[@id="rating_fullview_container"]'):
            review_score = review.xpath('*//span[@class="BAscore_norm"]/text()').extract_first()
            review_deviation = review.xpath('*//span[@style="color:#006600;"]/text()').extract_first()
            username = review.xpath('*//span[@class="muted"]/a[@class="username"]/text()').extract_first()
            date = review.xpath(
                '*//span[@class="muted"]/a[2]/text()').extract_first()  # use div container as well to ensure it gets the proper one
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
        reviewcount = int(next_review.split('start=')[1])  # URL reviewcount on next button
        if (reviewcount < 500):  # when next button >= max, next page is not returned
            yield response.follow(next_review, self.parse_beer)
        else:
            next