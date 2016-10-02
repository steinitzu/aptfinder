# -*- coding: utf-8 -*-
import re
from decimal import Decimal

import scrapy
from dateutil.parser import parse as dateparse

from .util import yes_no_bool


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["kijiji.ca"]
    start_urls = (('http://www.kijiji.ca'
                   '/b-apartments-condos'
                   '/gta-greater-toronto-area'
                   '/c37l1700272?ad=offering&pet-friendly=1/'),)

    def parse(self, response):
        for title in response.css('.search-item'):
            href = title.css('div::attr("data-vip-url")').extract_first()
            self.logger.info('Going to href %s', href)
            yield scrapy.Request(
                response.urljoin(href), callback=self.parse_ad)

        pagination = response.css('.pagination')
        next_page = pagination.css('a[title=Next]::attr("href")')
        next_page = next_page.extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse)

    def parse_ad(self, response):
        table = response.css('.ad-attributes')
        rows = table.xpath('//tr')
        result = {}
        result['url'] = response.url
        for row in rows:
            try:
                heading, data = row.xpath('./th|./td')
            except ValueError:
                # Non data row most likely
                continue
            heading = heading.xpath('text()').extract_first()

            heading = heading.strip().lower()
            heading = re.sub(r'[^\w\s]', '', heading)
            heading = heading.strip()
            heading = heading.replace(' ', '_')
            if heading == 'price':
                data = data.css('[itemprop="price"]')
                data = data.xpath('./strong/text()').extract_first()
                data = data.replace(',', '')
                data = Decimal(data[1:])
            else:
                data = data.xpath('text()').extract_first()
            if isinstance(data, str):
                data = data.strip()
            if isinstance(data, Decimal):
                pass
            elif heading == 'date_listed':
                data = dateparse(data)
            elif heading == 'bathrooms':
                data = int(data[0])
            elif data.lower() in ('yes', 'no'):
                data = yes_no_bool(data)
            result[heading] = data
        return result
