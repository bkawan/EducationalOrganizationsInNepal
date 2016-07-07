# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from edunepal.items import EdunepalItem
import re
import sys
import  codecs
import locale
import unicodedata

class EduSpider(scrapy.Spider):
    name = "edu"
    allowed_domains = ["edusanjal.com"]
    start_urls = [
        'http://edusanjal.com/college/',
    ]

    def __init__(self):
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse(self, response):


        list_details_elements = response.xpath("//div[@class='listDetails']")
        for item in list_details_elements:
            short_info = item.xpath('normalize-space(.//div[@class="shortInfo"])').extract_first()
            college_link = item.xpath(".//div[@class='detlsTitle']/a/@href").extract_first()
            categories = item.xpath(".//div[@class='categoriesIcons']")[0]
            category =",".join(categories.xpath("a/text()").extract())
            funding = "Others"
            if "Private" in short_info:
                funding = "Private"

                # print("Private")
            elif "Public" in short_info:
                funding = "Public"
                # print("Public")

            request = scrapy.Request(response.urljoin(college_link), self.parse_each_edu_org)
            request.meta['funding'] = funding
            request.meta['category'] = category
            yield request

        # "<a href="?page=2" rel="next">Next</a>"

        next_url = response.xpath("//a[@rel='next']/@href").extract_first()


        if next_url:
            yield scrapy.Request(response.urljoin(next_url),self.parse)



    def parse_each_edu_org(self,response):
        # print(response.url)


        print("********* Name *************")
        org_name = response.xpath('normalize-space(//h1[@class="mainHeading"])').extract_first()
        print (org_name)

        print("********* Funding *************")
        funding = response.meta['funding']
        print(funding)

        print("********* category *************")
        category = response.meta['category']
        print(category)

        print("********* Education Board *************")
        education_board = response.xpath("//ul[@class='DetailsList']/li[2]/a/text()").extract()
        education_board = ",".join(education_board)
        print(education_board)

        print("********* Contact Number *************")
        contact_no = response.xpath('normalize-space(//ul[@class="DetailsList"]/li[3])').extract_first()
        print(contact_no)

        print("********* district  and Zone *************")
        district_zone_elements = response.xpath("//ul[@class='DetailsList']/li[1]/span/a/text()").extract()
        district=""
        zone=""
        if district_zone_elements:
            try:
                district =district_zone_elements[0]
                print(district)
                if district:
                    try:
                        zone = district_zone_elements[1]
                    except:
                        zone = "Null"
            except:
                district = "Null"


        print("********* Full Address *************")
        full_address = response.xpath("normalize-space(//ul[@class='DetailsList']/li/span)").extract_first()
        full_address = unicodedata.normalize("NFKD", full_address)

        print("********* Stree Address *************")
        # street_address = full_address.strip(zone)
        street_address = re.sub(r'\b' + district + r'\b', ' ', full_address)
        street_address = re.sub(r'\b' + zone + r'\b', ' ', street_address)

        print(street_address)

        print("********* courses *************")
        course_elements = response.xpath("//ul[@class='list_link']/li")
        course_list = []
        high_school_course_list = []
        college_and_uni_course_list = []
        for course in course_elements:
            c = course.xpath('normalize-space()').extract_first()
            course_list.append(c)
            if "Ten Plus Two" in c:
                high_school_course_list.append(c)
            else:
                college_and_uni_course_list.append(c)

        print("********* All Courses List *************")
        print(",\n".join(course_list))
        courses = ",".join(course_list)

        print("********* High School Courses *************")
        print(high_school_course_list)

        print("********* Colleges Courses *************")
        print(college_and_uni_course_list)


        print("********* Websites,links,email *************")
        detail_list = response.xpath("//ul[@class='DetailsList']").extract_first()
        web_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        website_group = web_regex.findall(detail_list)
        facebook_link = ""
        googleplus_link = ""
        youtube_link = ""
        twitter_link = ""
        org_website = ""
        others_link = []
        for i in range(len(website_group)):
            if "facebook.com" in website_group[i]:
                facebook_link = website_group[i]
            elif "google.com" in website_group[i]:
                googleplus_link = website_group[i]
            elif "youtube.com" in website_group[i]:
                youtube_link = website_group[i]
            elif "twitter.com" in website_group[i]:
                twitter_link = website_group[i]
            elif website_group.count(website_group[i]) == 2:
                org_website = website_group[i]
            else:
                others_link.append(website_group[i])

        print(facebook_link,twitter_link,googleplus_link,youtube_link,org_website,others_link)

        print("********* Email *************")
        email_regex = re.compile(r'[a-zA-Z0-9_.+]+@[a-zA-Z0-9_.+]+')
        email_group = email_regex.findall(detail_list)
        email=""
        if email_group:
            email = email_group[0]
        print(email)

        print("********* Prefered Contact Address *************")

        contact_address_elements = response.xpath("normalize-space(//div[@class='normalContentWrapp'])").extract_first()
        if "Contact Address" in contact_address_elements:
            contact_address = contact_address_elements.split("Contact Address")
            print (contact_address[-1])
            contact_address = contact_address[-1]
        else:
            contact_address = full_address

        print("********* link *************")
        link = response.url


        item = EdunepalItem()
        item['OrganizationName'] = org_name
        item['EducationBoard'] = education_board
        print(item['EducationBoard'].split(","))

        item['ContactNo'] = contact_no
        item['Email'] = email
        item['Website'] = org_website
        item['StreetAddress'] = street_address
        item['District'] = district
        item['Zone'] = zone
        item['ContactAddress'] = contact_address
        item['Courses'] = courses
        item['HighSchoolCourses'] = ",".join(high_school_course_list)
        item['CollegeAndUniCourses'] = ",".join(college_and_uni_course_list)

        item['Link'] = link
        item['Funding'] = funding

        item['FacebookLink'] = facebook_link
        item['GooglePlusLink'] = googleplus_link
        item['TwitterLink'] = twitter_link
        item['YoutubeLink'] = youtube_link
        item['OtherLinks'] = ",".join(others_link)


        yield item






