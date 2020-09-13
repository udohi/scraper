import scrapy


class UkhotelsItem(scrapy.Item):
    # define the fields for your item here like:
    hotel_name = scrapy.Field()
    city = scrapy.Field()
    hotel_overview=scrapy.Field()
    imageUrl = scrapy.Field()
    overall_rating = scrapy.Field()
    value = scrapy.Field()
    cleanliness = scrapy.Field()
    service = scrapy.Field()
    location = scrapy.Field()
    hotel_class = scrapy.Field()
    hotel_style = scrapy.Field()
    number_reviews = scrapy.Field()
    free_parking = scrapy.Field()
    breakfast = scrapy.Field()
    pool = scrapy.Field()
    taxi_service = scrapy.Field()
    restaurant = scrapy.Field()
    free_wifi = scrapy.Field()
    air_conditioning = scrapy.Field()
    private_balcony = scrapy.Field()
    room_service = scrapy.Field()
    iron = scrapy.Field()
    refrigerator = scrapy.Field()
    tv = scrapy.Field()
    house_keeping = scrapy.Field()
    excellent_ratings = scrapy.Field()
    pass
