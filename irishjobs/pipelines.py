# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re


class IrishjobsPipeline(object):
    """
    Cleans job_description of non-breaking space and newlines.
    Also removes the "Updated" string from date_updated.
    """

    def __init__(self):
        self.spaces = re.compile(r"\s+")

    def process_item(self, item, spider):
        if item['job_description']:
            item['job_description'] = self.spaces.sub(" ", item['job_description']).strip()
        if item['date_updated']:
            item['date_updated'] = item['date_updated'].replace("Updated ", "")
        return item
