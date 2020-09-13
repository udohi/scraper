import scrapy
from ukhotels.items import UkhotelsItem
from datetime import datetime
import re


class Scraper(scrapy.Spider):
    name = "ukhotels"

    # First Start Url
    start_urls = [
        "https://www.tripadvisor.co.uk/Hotels-g186338-London_England-Hotels.html"]

    # number of pages to scrape
    npages = 130

    # number of hotels in a page
    nbItemsOnPage = 30

    # This mimics getting the pages using the pagination
    i = 0
    for i in range(30, npages*30, nbItemsOnPage):
        start_urls.append("https://www.tripadvisor.co.uk/Hotels-g186338-oa" +
                          str(i)+"-London_England-Hotels.html#BODYCON")

    # parsing each page
    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'listing_title')]/a[1]//@href"):
            url = "https://www.tripadvisor.co.uk" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    # parse each hotel page
    def parse_dir_contents(self, response):

        item = UkhotelsItem()

        # Getting Hotel Name
        item['hotel_name'] = response.xpath(
            "//h1[contains(@id, 'HEADING')]/descendant::text()").extract()[0].strip()

        # Getting overall_rating
        item['overall_rating'] = response.xpath(
            "//span[contains(@class,'_3cjYfwwQ')]/descendant::text()").extract()[0].strip()

        # Getting hotel_overview
        item['hotel_overview'] = response.xpath(
            "//div[contains(@id, 'ABOUT_TAB')]//div[contains(@class,'cPQsENeY')]/descendant::text()").extract()[0].strip()

        # Getting imageUrl
        item['imageUrl'] = response.xpath(
            "//div[contains(@class,'carousel')]/ul/li/div/img[1]/@src").extract()[0].strip()

        # Getting city
        item['city'] = response.xpath(
            "//div[contains(@id,'ABOUT_TAB')]//div[contains(@class, 'ui_column')]/span/descendant::text()").extract()[0].split(" in ")[-1].strip()

        # ratings
        rattings = response.xpath(
            "//div[contains(@class, '_1krg1t5y')]/span[contains(@class, 'ui_bubble_rating')]/@class").extract()

        item['location'] = int(rattings[0].strip()[-2:])/10
        item['cleanliness'] = int(rattings[1].strip()[-2:])/10
        item['service'] = int(rattings[2].strip()[-2:])/10
        item['value'] = int(rattings[3].strip()[-2:])/10

        # Getting number_reviews
        item['number_reviews'] = response.xpath(
            "//span[contains(@class, 'test-target-tab-Reviews')]//span[contains(@data-test-target, 'CC_TAB_Reviews_LABEL')]/span/span/descendant::text()").extract()[0].strip()

        # Getting excellent_ratings
        item['excellent_ratings'] = response.xpath(
            "//div[contains(@data-test-target, 'reviews-tab')]/div/div/div/ul/li/span/descendant::text()").extract()[0].strip()

        # Getting hotel_class
        item['hotel_class'] = response.xpath(
            "//div[contains(@id, 'ABOUT_TAB')]/div[contains(@class, 'ui_column')]//div[contains(@class, 'ui_columns')]/div[1]/div[2]/span/span/@title").extract()[0].strip()[0:3]

        # Getting hotel_style
        styles = response.xpath(
            "//div[contains(@id, 'ABOUT_TAB')]/div[contains(@class, 'ui_column')]//div[contains(@class, 'ui_columns')]/div[1]//div/descendant::text()").extract()
        item['hotel_style'] = ','.join(map(str, styles[2:])).strip()

        # properties
        properties = response.xpath(
            "//div[contains(@id, 'ABOUT_TAB')]/div[contains(@class, 'ui_column')]/div/div[1]/div[2]/div/descendant::text()").extract()

        # features
        features = response.xpath(
            "//div[contains(@id, 'ABOUT_TAB')]/div[contains(@class, 'ui_column')]/div/div[1]/div[5]/div/descendant::text()").extract()

        # fill with no but check after
        item['free_parking'] = "No"
        item['free_wifi'] = "No"
        item['breakfast'] = "No"
        item['taxi_service'] = "No"
        item['pool'] = "No"
        item['restaurant'] = "No"
        item['air_conditioning'] = "No"
        item['private_balcony'] = "No"
        item['room_service'] = "No"
        item['iron'] = "No"
        item['refrigerator'] = "No"
        item['house_keeping'] = "No"
        item['tv'] = "No"

        # check properties
        for prop in properties:
            if "Free High Speed Internet (WiFi)" in prop.strip():
                item['free_wifi'] = "YES"

            if "Free parking" in prop.strip():
                item['free_parking'] = "YES"

            if "Free breakfast" in prop.strip():
                item['breakfast'] = "YES"

            if "Pool" in prop.strip():
                item['pool'] = "YES"

            if "Free shuttle or taxi services" in prop.strip():
                item['taxi_service'] = "YES"

            if "Restaurant" in prop.strip():
                item['restaurant'] = "YES"

        # check features
        for prop in features:

            if "Air conditioning" in prop.strip():
                item['air_conditioning'] = "YES"

            if "Flatscreen TV" in prop.strip():
                item['tv'] = "YES"

            if "Room service" in prop.strip():
                item['room_service'] = "YES"

            if "Iron" in prop.strip():
                item['iron'] = "YES"

            if "Housekeeping" in prop.strip().strip():
                item['house_keeping'] = "YES"

            if "Refrigerator" in prop.strip():
                item['refrigerator'] = "YES"

            if "Private balcony" in prop.strip():
                item['private_balcony'] = "YES"

        yield item
