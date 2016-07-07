# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from edunepal.items import EdunepalItem
import re
import html2text
import unicodedata


class EduSpider(scrapy.Spider):
    name = "edu1"
    allowed_domains = ["edusanjal.com"]
    start_urls = [
"http://edusanjal.com/college",
    ]

    def parse(self, response):
        # response = response.body


        next_url = response.xpath("//a[rel=''next]/@href").extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), self.parse)

        print()















