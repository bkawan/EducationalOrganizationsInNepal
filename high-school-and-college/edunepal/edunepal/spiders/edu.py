# -*- coding: utf-8 -*-
import scrapy
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
            elif "Public" in short_info:
                funding = "Public"

            request = scrapy.Request(response.urljoin(college_link), self.parse_each_edu_org)
            request.meta['funding'] = funding
            request.meta['category'] = category
            yield request


        next_url = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url),self.parse)



    def parse_each_edu_org(self,response):


        print("********* Name  of Organization *************")
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
        highschool_board = ""
        college_board = []
        if education_board:
            for board in education_board:
                if board.strip() == "HSEB":
                    highschool_board = board.strip()
                else:
                    college_board.append(board.strip())

        print(education_board)
        print(highschool_board)
        print(college_board)


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
                if district:
                    try:
                        zone = district_zone_elements[1]
                    except:
                        zone = None
            except:
                district = None
        print (district,zone)


        print("********* Full Address *************")
        full_address = response.xpath("normalize-space(//ul[@class='DetailsList']/li/span)").extract_first()
        full_address = unicodedata.normalize("NFKD", full_address)

        print("********* Stree Address *************")
        street_address = re.sub(r'\b' + district + r'\b', ' ', full_address)
        street_address = re.sub(r'\b' + zone + r'\b', ' ', street_address)

        print(street_address)


        print("********* courses *************")
        course_elements = response.xpath("//ul[@class='list_link']/li")
        hseb_dict_list = []
        college_and_uni_dict_list =[]
        for course in course_elements:
            course = course.xpath('normalize-space()').extract_first()
            if "Ten Plus Two" in course:
                course_items = [x for x in course.split(";") if x.strip()]
                course_detail = {
                    "Title": self.get_index(course_items, 0),
                    "Capacity": self.get_index(course_items, 1),
                    "Fee": self.get_index(course_items, 2)
                }
                hseb_dict_list.append(course_detail)

            else:
                course_items = [x for x in course.split(";") if x.strip()]
                course_detail = {
                    "Title": self.get_index(course_items, 0),
                    "Capacity": self.get_index(course_items, 1),
                    "Fee": self.get_index(course_items, 2)
                }
                college_and_uni_dict_list.append(course_detail)




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
        info_elements = response.xpath("normalize-space(//div[@class='normalContentWrapp'])").extract_first()

        print("***************** Established ********************************")

        all_dates = re.findall(
            r'(([Ee]stablished in)?([Ff]ounded in)?([Ee]stablishment)? ((20|1\d)\d\d)\s?([adADbsBS.]{2,4})?)',info_elements)
        estb = []

        if all_dates:
            for date in all_dates:
                item = ['established in', 'founded in', 'establishment']
                for r in range(len(item)):
                    if item[r] in date[0].lower():
                        d = re.sub(r'[eE]stablished in|[fF]ounded in|[Ee]stablishment', "", date[0])
                        estb.append(d.strip())
        else:
            estb.append("")


        print("*************** Prefered Contact Address********************************")
        contact_address = re.findall(r'Contact Address(.*)',info_elements)
        if contact_address:
            contact_address = contact_address[0]
        else:
            contact_address = full_address

        print(contact_address)


        print("********* link *********************")
        link = response.url


        ## instantiate  EdunepalItem
        item = EdunepalItem()

        ## creating Dictionary item
        item['OrganizationOverview'] = {
            "Organization Name": self.strip(org_name),
            "Established": ",".join(estb),
            "Education Board": {
                "High School": highschool_board,
                "Higher Education Board": college_board
            },
            "Contact Number": self.strip(contact_no),
            "Email Address": self.strip(email),
            "Website": self.strip(org_website),
            "Detail Link": self.strip(link),
            "Street Address": self.strip(street_address),
            "District": self.strip(district),
            "Zone": self.strip(zone),
            "Prefered Contact Address": self.strip(contact_address),
            "Courses": {
                "HSEB": hseb_dict_list,
                "CollegeAndUni": college_and_uni_dict_list
            },
            "Funding": funding,
            "Social Links": {
                "Facebook": self.strip(facebook_link),
                "Google": self.strip(googleplus_link),
                "Twitter": self.strip(twitter_link),
                "Youtube": self.strip(youtube_link),

            },
            "Other Links": others_link,
            "Category":category

        }

        yield item



    def get_index(self,item_list, index):
        try:
            value = item_list[index]
            try:
                value = value.strip()
            except:
                value = value
        except:
            value = ""
        return value

    def strip(self,string):
        try:
            value = string.strip()
        except:
            value = string
        return value


