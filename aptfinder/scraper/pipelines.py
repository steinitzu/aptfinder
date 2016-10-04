# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from math import radians

import googlemaps

from .. import db
from ..db.models import Apartment
from ..config import GOOGLE_MAPS_API_KEY


class AptscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLAlchemyPipeline(object):
    def open_spider(self, spider):
        self.gmaps = googlemaps.Client(
            key=GOOGLE_MAPS_API_KEY)
        db.init_db()

    def process_item(self, item, spider):
        # loc = self.gmaps.geocode(item['address'])[0]
        # lat = radians(loc['geometry']['location']['lat'])
        # lng = radians(loc['geometry']['location']['lng'])
        # item['latitude'] = lat
        # item['longitude'] = lng
        s = db.Session()
        a = Apartment(**item)
        s.add(a)
        s.commit()
