import scrapy


class SexItem(scrapy.Item):
    href_1 = scrapy.Field()
    href_2 = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    available = scrapy.Field()
