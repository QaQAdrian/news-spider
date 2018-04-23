from redis_util.redis_queue_dao import RedisQueueDao
from redis_util.redis_url_pusher import RedisUrlPusher

class UrlPushPipeline(object):

    def __init__(self, redis_uri, redis_password, redis_port = 6379, redis_queue_key = "queue"):
        self.__redis_uri = redis_uri
        self.__redis_password = redis_password
        self.__redis_port = redis_port
        self.__redis_queue_key = redis_queue_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_uri = crawler.settings.get('REDIS_URI'),
            redis_password = crawler.settings.get('REDIS_PASSWORD'),
            redis_port = int(crawler.settings.get('REDIS_PORT')),
            redis_queue_key = crawler.settings.get('REDIS_QUEUE_KEY')
        )

    def open_spider(self, spider):
        rqd = RedisQueueDao(host = self.__redis_uri,
                            password = self.__redis_password,
                            port = self.__redis_port,
                            queue_key = self.__redis_queue_key)
        self.__rup = RedisUrlPusher(rqd)

    def close_spider(self, spider):
        del self.__rup

    def process_item(self, item, spider):
        self.__rup.url_push(item)
        return item