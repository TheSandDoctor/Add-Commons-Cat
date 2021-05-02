from redis import Redis
import pickle
import pywikibot
from common import REDIS_KEY

site = pywikibot.Site(user="TheSandBot")
redis = Redis(host="localhost")
search_generator = site.search('"El Paso Daily Times. (El Paso, Tex.), Vol" -incategory:"El Paso Daily Times"')
igen = iter(search_generator)
for page in igen:
    #pickled_page = pickle.dumps(page)
    redis.rpush(REDIS_KEY, str(page.title()))
