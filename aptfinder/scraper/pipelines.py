# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import googlemaps

from .. import db
from ..db.models import Apartment
from ..config import GOOGLE_MAPS_API_KEY
from .. import log


class AptscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLAlchemyPipeline(object):
    def open_spider(self, spider):
        db.init_db()

    def process_item(self, item, spider):
        s = db.Session()
        apt = db.get_if_exists(s, Apartment, url=item['url'])
        if apt:
            log.info('Apartment url: "{}" already exists'.format(
                apt.url))
            return  # already exists, done
        apt = Apartment(**item)
        s.add(apt)
        s.commit()
