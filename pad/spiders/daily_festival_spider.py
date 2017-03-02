import scrapy
import re
import redis
from datetime import datetime, timedelta

class DailyFestivalSpider(scrapy.Spider):
    name = "dailyfest"
    padx = 'http://puzzledragonx.com/'
    time_delta_br = 3
    cache = redis.StrictRedis(host = 'localhost', port = 2468, db = 0)

    def start_requests(self):
        urls = [
            self.padx,
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):

        events = response.css('div#metal1a #event')[0].css('tr')
        total_of_events = (len(events) - 1) / 2

        for row in range(1, (len(events) - 1), 2):

            events_by_group = events[row].css('a')
            events_hour = events[row + 1].css('td.metaltime').xpath('text()')

            for i in range(0, len(events_by_group), 1):
                partialHref = re.sub("\D", "", events_by_group[i].xpath('@href').extract()[0])
                href = self.padx + 'en/mission.asp?m=' + partialHref
                hour = self.parse_hour(events_hour[i].extract())
                hour = hour + timedelta(hours = self.time_delta_br)

                if self.cache.get(href) is None:
                    new_response = scrapy.Request(url = href, callback = self.parse_dg_title)
                    print new_response
                    # print new_response.xpath('//*[@id="tablestat"]/tbody/tr[2]/td').extract()
                    # self.cache.set(href, new_response.)
                #
                # new_res = self.cache.get(partialHref)
                #
                # print "\n"
                # print new_res
                # print "\n"

    def parse_hour(self, timezone):
        time = timezone[-2:]
        splited_hour = timezone.split(':')

        if len(splited_hour) == 1:
            hour = re.sub("\D", "", timezone)
            timezone = hour + ':00 ' + time

        return datetime.strptime(timezone, '%I:%M %p')

    def parse_dg_title(self, response):
        print '------------------------\n'
        # print response
        print '------------------------\n'
        return 'qwoejqwoei'

class DailyEvent (object):
    def __init__(self):
        self.name = ''
        self.link = ''
        self.title = ''
        self.schedule = ''

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_link(self):
        return self.link

    def set_link(self, link):
        self.link = link

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_schedule(self):
        return self.schedule

    def set_schedule(self, schedule):
        self.schedule = schedule
