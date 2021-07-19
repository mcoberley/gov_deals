from gov_deals.items import GovDealsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule



class HomepageSpider(CrawlSpider):
    name = 'homepage'
    allowed_domains = ['govdeals.com']
    start_urls = ['http://www.govdeals.com/index.cfm']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@id='cat_link']"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[text()='>>'])[2]"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='result_col_2']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = GovDealsItem()

        item['_id'] = GovDealsItem.generate_id(response)
        item['title'] = GovDealsItem.get_title(response)
        item['link'] = str(response.url)
        item['photo_url'] = GovDealsItem.get_photo_url(response)
        item['auction_end'] = GovDealsItem.get_auction_end_date(response)
        item['admin_fee'] = GovDealsItem.get_admin_fee(response)
        item['bids'] = GovDealsItem.get_number_of_bids(response)
        item['current_bid'] = GovDealsItem.get_current_bid(response)
        item['more_info'] = GovDealsItem.get_additional_info(response)

        yield item