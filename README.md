# gov_deals
Scraper for GovDeals.com site

The only spider in the project is called homepage. It crawls all the links on the home page of [GovDeals](https://www.govdeals.com/index.cfm) 
## Run
```bash
scrapy crawl homepage
```

## Pipelines
Two item pipelines are included. The first, JsonWriterPipeline, outputs items to a JSON file, items.json, as they are scraped. The other, MongoPipeline, puts them into a mongodb database. The name of the database is defined in settings.py MONGO_DATABASE and the uri is MONGO_URI. The collection that any given item is upserted to is determined by (and named after) the category field. If no category field is found, the item is put into a collectio named 'uncategorized'.

## Middlewares
No middlewares are used, but the boilerplate code is left in for extensibility.