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

class EdunepalPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvPipeline(object):
    def __init__(self):
        self.all_colleges_list_csvwriter= csv.writer(open("{}all_private-hs-and-college_list.csv".format(csv_path),'wb'))
        self.highschool_csvwriter = csv.writer(codecs.open("{}private-high-school-list.csv".format(csv_path),'wb'))
        self.collegeanduni_csvwriter = csv.writer(open("{}private-college-and-university-list.csv".format(csv_path),'wb'))

        self.all_colleges_list_csvwriter.writerow(['OrganizationName','EducationBoard','ContactNo',
                                                   'Email','Website','StreetAddress',
                                                   'District','Zone','ContactAddress',
                                                   'Courses','HighSchoolCourses','CollegeAndUniCourses',
                                                   'Link','Funding','FacebookLink','GooglePlusLink',
                                                   'TwitterLink','YoutubeLink','OtherLinks'
                                                   ])

        self.highschool_csvwriter.writerow(['OrganizationName','EducationBoard','ContactNo',
                                                   'Email','Website','StreetAddress',
                                                   'District','Zone','ContactAddress',
                                                   'HighSchoolCourses','Link','Funding',
                                                   'FacebookLink','GooglePlusLink','TwitterLink',
                                                   'YoutubeLink','OtherLinks'
                                                   ])

        self.collegeanduni_csvwriter.writerow(['OrganizationName','EducationBoard','ContactNo',
                                                   'Email','Website','StreetAddress',
                                                   'District','Zone','ContactAddress',
                                                   'CollegeAndUniCourses','Link','Funding',
                                                   'FacebookLink','GooglePlusLink','TwitterLink',
                                                   'YoutubeLink','OtherLinks'
                                                   ])


    def process_item(self, item, spider):
        education_board = item['EducationBoard'].split(",")
        high_school = "HSEB"
        college_and_uni = []

        for board in education_board:
            if "HSEB" == board:
             high_school = "HSEB"
            else:
                college_and_uni.append(board)
        college_and_uni = ",".join(college_and_uni)

        if item['HighSchoolCourses'] and item['Funding'] == 'Private':
            self.highschool_csvwriter.writerow([item['OrganizationName'],high_school,item['ContactNo'],
                                                 item['Email'],item['Website'],item['StreetAddress'],
                                                 item['District'],item['Zone'],item['ContactAddress'],
                                                 item['HighSchoolCourses'],item['Link'],item['Funding'],
                                                 item['FacebookLink'],item['GooglePlusLink'],item['TwitterLink'],
                                                 item['YoutubeLink'],item['OtherLinks']

            ])
        if item['CollegeAndUniCourses'] and item['Funding'] == 'Private':

            self.collegeanduni_csvwriter.writerow([item['OrganizationName'],college_and_uni,item['ContactNo'],
                                                     item['Email'],item['Website'],item['StreetAddress'],
                                                     item['District'],item['Zone'],item['ContactAddress'],
                                                     item['CollegeAndUniCourses'],item['Link'],item['Funding'],
                                                     item['FacebookLink'],item['GooglePlusLink'],item['TwitterLink'],
                                                     item['YoutubeLink'],item['OtherLinks']

                ])


        self.all_colleges_list_csvwriter.writerow([item['OrganizationName'],item['EducationBoard'],item['ContactNo'],
                                                 item['Email'],item['Website'],item['StreetAddress'],
                                                 item['District'],item['Zone'],item['ContactAddress'],
                                                 item['Courses'],item['HighSchoolCourses'],item['CollegeAndUniCourses'],
                                                 item['Link'],item['Funding'],
                                                 item['FacebookLink'],item['GooglePlusLink'],item['TwitterLink'],
                                                 item['YoutubeLink'],item['OtherLinks']

            ])


        return item

class JsonPipeline(object):
    def process_item(self, item, spider):
        return item



