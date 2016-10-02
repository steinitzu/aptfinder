# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .. import db

Apartment = db.models.Apartment


class AptscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLAlchemyPipeline(object):
    def open_spider(self, spider):
        db.init_db()

    def process_item(self, item, spider):
        s = db.Session()
        a = Apartment(**item)
        s.add(a)
        s.commit()
