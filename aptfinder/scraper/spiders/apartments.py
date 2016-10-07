# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from math import radians

import scrapy
from dateutil.parser import parse as dateparse

from .util import yes_no_bool


class ApartmentsSpider(scrapy.Spider):
    name = "apartments"
    allowed_domains = ["kijiji.ca"]

    # TODO: get bedroom number from url
    start_urls = [
        'http://www.kijiji.ca/b-2-bedroom-apartments-condos/gta-greater-toronto-area/c214l1700272?ad=offering',
        'http://www.kijiji.ca/b-1-bedroom-apartments-condos/gta-greater-toronto-area/c212l1700272?ad=offering',
        'http://www.kijiji.ca/b-1-bedroom-den-apartments-condos/gta-greater-toronto-area/c213l1700272?ad=offering',
        'http://www.kijiji.ca/b-bachelor-studio-apartments-condos/gta-greater-toronto-area/c211l1700272?ad=offering',
        'http://www.kijiji.ca/b-3-bedroom-apartments-condos/gta-greater-toronto-area/c215l1700272?ad=offering',
        'http://www.kijiji.ca/b-4-plus-bedroom-apartments-condos/gta-greater-toronto-area/c216l1700272?ad=offering']

    bed_map = {
        '2-bedroom-apartments-condos': '2 bedroom',
        '1-bedroom-apartments-condos': '1 bedroom',
        '3-bedroom-apartments-condos': '3 bedroom',
        '4-plus-bedroom-apartments-condos': '4 bedroom',
        'bachelor-studio-apartments-condos': 'studio',
        '1-bedroom-den-apartments-condos': '1 bedroom'
    }

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

        name = response.css('[itemprop="name"]').css('h1')
        name = name.xpath('text()').extract_first()

        lat = response.css(
            '[property="og:latitude"]::attr("content")').extract_first()
        lng = response.css(
            '[property="og:longitude"]::attr("content")').extract_first()

        result['latitude'] = radians(float(lat))
        result['longitude'] = radians(float(lng))
        result['geocode_source'] = 'kijiji'

        result['title'] = name

        url = response.url
        result['url'] = url
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
                try:
                    data = Decimal(data[1:])
                except:
                    data = None
            else:
                data = data.xpath('text()').extract_first()
            if isinstance(data, str):
                data = data.strip()
            if isinstance(data, Decimal) or data is None:
                pass
            elif heading == 'date_listed':
                data = dateparse(data)
            elif heading == 'bathrooms':
                data = int(data[0])
            elif data.lower() in ('yes', 'no'):
                data = yes_no_bool(data)
            result[heading] = data

        for key, value in self.bed_map.items():
            if key in result['url']:
                result['bedrooms'] = value
                break
        return result
