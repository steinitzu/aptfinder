# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

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
        # Timestamp of first row added this session
        # Will delete any that are older
        self.first_date = None

    def process_item(self, item, spider):
        s = db.Session()
        apt = db.get_if_exists(s, Apartment, url=item['url'])
        if apt: # exists
            apt.touched_at = datetime.datetime.utcnow()
        else:
            apt = Apartment(**item)
        s.add(apt)
        s.commit()
        if not self.first_date:
            self.first_date = apt.touched_at

    def close_spider(self, spider):
        # DELETE inactive listings
        # TODO: handle in case of multiple spiders
        rs = db.engine.execute(
            'DELETE FROM apartment WHERE touched_at < %s',
            self.first_date)
        rs.close()
