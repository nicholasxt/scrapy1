# -*- coding: utf-8 -*-
import scrapy
from scrapy1.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    offset = 0
    baseURL = "https://hr.tencent.com/position.php?&start="
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
            item = TencentItem()
            item['name'] = node.xpath("./td[1]/a/text()").extract()
            item['link'] = node.xpath("./td[1]/a/@href").extract()
            if len(node.xpath("./td[2]/text()")):
                item['type'] = node.xpath("./td[2]/text()").extract()
            else:
                item['type'] = "NULL"
            item['number'] = node.xpath("./td[3]/text()").extract()
            item['location'] = node.xpath("./td[4]/text()").extract()
            item['time'] = node.xpath("./td[5]/text()").extract()

            yield item

        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url, callback=self.parse)


