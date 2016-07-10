# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import csv
import codecs

json_path = "data/json/"
csv_path = "data/csv/"

class JsonPipeline(object):
    def __init__(self):
        self.college_jsonfile = codecs.open('{}all-private-college-and-uni-list.json'.format(json_path), 'wb', encoding='utf-8')
        self.highschool_jsonfile = codecs.open('{}all-private-highschool-list.json'.format(json_path), 'wb', encoding='utf-8')
        self.all_edu_jsonfile = codecs.open('{}all-private-highschool-and-college-and-uni-list.json'.format(json_path), 'wb', encoding='utf-8')
        self.allfile = codecs.open('{}all-private-and-public-highschool-and-college-and-uni-list.json'.format(json_path), 'wb', encoding='utf-8')
    #
    def process_item(self, item, spider):
        funding = item['OrganizationOverview']['Funding']
        college_course = item['OrganizationOverview']['Courses']['CollegeAndUni']
        hs_course = item['OrganizationOverview']['Courses']['HSEB']
        hseb_board = item['OrganizationOverview']['Education Board']['High School']
        college_board = item['OrganizationOverview']['Education Board']['Higher Education Board']

        items = []
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.allfile.write(line)
        items.append(item)

        if funding =='Private':
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.all_edu_jsonfile.write(line)
            items.append(item)
            if college_course:
                item['OrganizationOverview']['Courses'] = college_course
                item['OrganizationOverview']['Education Board']  = college_board
                line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                self.college_jsonfile.write(line)
                items.append(item)

            if hs_course:
                item['OrganizationOverview']['Courses'] = hs_course
                item['OrganizationOverview']['Education Board']  = hseb_board
                line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                self.highschool_jsonfile.write(line)
                items.append(item)



        return tuple(items)









