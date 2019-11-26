import scrapy
from sex.items import SexItem


class KlubnichkaSpider(scrapy.Spider):
    name = 'klubnichka'
    allowed_domains = ['klubnichka.in.ua']
    start_urls = ['http://klubnichka.in.ua/']


    def parse(self, response):
        try:
            menu_blocks = response.xpath('//ol[@id="productMenu"]/li[@class="menuItem"]')
        except:
            return
        else:
            for block in menu_blocks:
                href = block.xpath('.//a[@class="menuItema "]/@href').get()
                if not href:
                    href = block.xpath('.//a/@href').get()

                href_2_list = block.xpath('.//a[@class="txtDefault "]/@href').getall()

                if len(href_2_list) == 0:
                    yield response.follow(url=response.urljoin(href),
                                          callback=self.parse_page_blocks,
                                          meta={'href': href, 'href_2': href})
                else:
                    for href_2 in href_2_list:
                        yield response.follow(url=response.urljoin(href_2),
                                              callback=self.parse_page_blocks,
                                              meta={'href': href, 'href_2': href_2})
                # break


    def parse_page_blocks(self, response):
        item = SexItem()
        href_1 = response.urljoin(response.meta['href'])
        href_2 = response.urljoin(response.meta['href_2'])
        meta_dict = {'href': href_1, 'href_2': href_2}

        blocks = response.xpath('//div[@id="content"]/table[@class="tblList"]/tr')

        for block in blocks:
            name_href_block = block.xpath('.//td[contains(@class, "colmntwo")]')

            if not name_href_block:
                continue

            item['href_1'] = href_1
            item['href_2'] = href_2
            item['name'] = name_href_block.xpath('.//a/text()').get()
            item['link'] = response.urljoin(name_href_block.xpath('.//a/@href').get())
            price_dict = self.get_prices(block)
            item['price'] = price_dict['price']
            item['old_price'] = price_dict['old_price']
            item['available'] = self.get_available(block)
            yield item

        next_link = self.get_next_link(response)
        if next_link:
            yield response.follow(url=next_link, callback=self.parse_page_blocks, meta=meta_dict)


    def get_available(self, block):
        available = block.xpath('.//td[contains(@class, "colmnfour")]//a[@class="buy_button"]')
        if available:
            return True
        else:
            return False


    def get_prices(self, block):
        result_dict = {'price': None, 'old_price': None}

        price_list = block.xpath('.//td[contains(@class, "colmnthree")]'
                                '//span[@property="price"]/text()').getall()
        if len(price_list) == 1:
            result_dict['price'] = self.clear_price(price_list[0])
        elif len(price_list) == 2:
            pr_1 = self.clear_price(price_list[0])
            pr_2 = self.clear_price(price_list[1])
            if pr_1 and pr_2:
                if pr_1 > pr_2:
                    result_dict['old_price'] = pr_1
                    result_dict['price'] = pr_2
                else:
                    result_dict['old_price'] = pr_2
                    result_dict['price'] = pr_1
        return result_dict


    def clear_price(self, price: str):
        price_1 = price.replace(' ', '')
        price_2 = price_1.replace('грн', '')
        price_3 = price_2.replace('.', '')
        price_4 = price_3.replace(',', '')
        price_str = price_4.strip()
        try:
            price_int = int(price_str)
        except:
            return None
        else:
            return price_int


        # next_link = self.get_next_link(response=response)
        # if next_link:
        #     print(next_link)
        #     yield response.follow(next_link, self.parse_page_blocks, meta=meta_dict)


    def get_next_link(self, response):
        next_links_list = response.xpath('//div[@id="content"]/p[@class="pagination"]/a[@class="txtLink"]')
        next_link = None

        for l in next_links_list:
            if l.xpath('.//text()').get() == '>':
                next_link = l.xpath('.//@href').get()
                break

        return next_link