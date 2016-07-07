# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EdunepalItem(scrapy.Item):
    # define the fields for your item here like:

    OrganizationName = scrapy.Field()
    EducationBoard = scrapy.Field()
    ContactNo = scrapy.Field()
    Email = scrapy.Field()
    Website = scrapy.Field()
    StreetAddress = scrapy.Field()
    District = scrapy.Field()
    Zone = scrapy.Field()
    ContactAddress = scrapy.Field()
    Courses = scrapy.Field()
    HighSchoolCourses = scrapy.Field()
    CollegeAndUniCourses = scrapy.Field()
    Link = scrapy.Field()
    Funding = scrapy.Field()

    FacebookLink= scrapy.Field()
    GooglePlusLink= scrapy.Field()
    TwitterLink= scrapy.Field()
    YoutubeLink= scrapy.Field()
    OtherLinks = scrapy.Field()



