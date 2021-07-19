# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymongo


class GovDealsPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    items = []

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.write(json.dumps(self.items))
        self.file.close()

    def process_item(self, item, spider):
        item.clean_self()
        self.items.append(ItemAdapter(item).asdict())
        return item


class MongoPipeline:

    collection_name = 'uncategorized'

    def __init__(self, mongo_uri, mongo_db): 
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item.clean_self()

        try:
            collection_name = item['more_info']['category'].lower().replace("-", "").replace("/", "_and_").replace(" ", "_").replace(",", "")
        except:
            collection_name = 'uncategorized'
            
        self.db[collection_name].replace_one({'_id': item['_id']}, ItemAdapter(item).asdict(), upsert=True)
        return item