# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from hashlib import sha256

# GovDealsItem class
# 
# All of the xpaths are good as of 2021-07-19
# 
class GovDealsItem(scrapy.Item):

    _id = scrapy.Field()
    photo_url = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    auction_end = scrapy.Field()
    admin_fee = scrapy.Field()
    bids = scrapy.Field()
    current_bid = scrapy.Field()
    more_info = scrapy.Field()

    def clean_self(self):
        for key in self:
            if self[key] == '':
                self[key] = 'N/A'

    @classmethod
    def generate_id(self, response):
        return sha256(str(response.url).encode('utf-8')).hexdigest()

    @classmethod
    def get_photo_url(self, response):
        photo_url_xpath = "//a[@id='thumb1']/img/@src"
        return response.urljoin(response.xpath(photo_url_xpath).get())

    @classmethod
    def get_title(self, response):
        title_xpath = "//td[@id='asset_short_desc_id']/text()"
        return response.xpath(title_xpath).get()

    @classmethod
    def get_auction_end_date(self, response):
        auction_end_xpath = "//td[text()='Auction Ends']/following-sibling::td/b/text()"
        return response.xpath(auction_end_xpath).get()

    @classmethod
    def get_admin_fee(self, response):
        admin_fee_xpath = "normalize-space(//td[starts-with(normalize-space(text()),'Admin Fee:')]/following-sibling::td/text())"
        return response.xpath(admin_fee_xpath).get().replace("\u00A0", "").strip()

    @classmethod
    def get_number_of_bids(self, response):
        bids_xpath = "normalize-space(//a[@id='viewBidHistory']/text())"
        num_of_bids = int(response.xpath(bids_xpath).get().replace("\u00A0", "").strip())
        return num_of_bids

    @classmethod
    def get_current_bid(self, response):
        current_bid_xpath = "normalize-space(//td[text()='Current Bid']/following-sibling::td/text())"
        current_bid = response.xpath(current_bid_xpath).get().replace("\u00A0", "").replace("C", "").replace("$", "").strip()
        return current_bid

    @classmethod
    def get_additional_info(self, response):
        table1_dict = {}

        x = response.xpath("//table[@id='make_model_tbl_id']")

        for table in x:
            table_rows = table.xpath("./tr")

            row1 = table_rows[0].xpath("./td")
            row2 = table_rows[1].xpath("./td")

            for i in range(0,len(row1)):
                label = row1[i].xpath("normalize-space(./b/text())").get()
                label = label.replace(" ", "_").replace("/", "_").lower()

                if label == "category":
                    value = row2[i].xpath("normalize-space(./a/text())").get()
                else:    
                    value = row2[i].xpath("normalize-space(./text())").get()

                table1_dict[label] = value

        return table1_dict