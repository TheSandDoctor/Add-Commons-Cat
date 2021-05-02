import pywikibot
from pywikibot.data.api import APIError
from pywikibot.throttle import Throttle
import re
import mysql.connector
import json
import pickle
from redis import Redis
from datetime import date
from common import REDIS_KEY

site = pywikibot.Site('commons','commons')

site._throttle = Throttle(site, multiplydelay=False)

# Multi-workers are enough to cause problems, no need for internal
# locking to cause even more problems
site.lock_page = lambda *args, **kwargs: None  # noop
site.unlock_page = lambda *args, **kwargs: None  # noop

#search_generator = site.search('"El Paso Daily Times. (El Paso, Tex.), Vol"')
#igen = iter(search_generator)
#counter = 0
mydb = mysql.connector.connect(
  host="localhost",
  user="newuser",
  password="password",
  database="commons_task3_run"
)
mycursor = mydb.cursor()

search_sql = "SELECT title FROM runs WHERE title = '%s'"

def main():
    redis = Redis(host="localhost")
    while True:
        _, picklemsg = redis.blpop(REDIS_KEY)
        title = picklemsg.decode("utf-8")
        page = pywikibot.Page(site, title) #this could be the issue as page title isnt clean
        #print(page.title())
        #print(str(title))
        #print(type(title))

    #for page in igen:
        mycursor.execute(search_sql, page.title())
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            print("Already done")
            continue
        else:
            text = page.text
            search_result = re.search("Category:El Paso Daily Times", text)
            if search_result:
                print("Found in page")
                add_to_db(page)
                continue # already done, move on
        #if counter >4:
        #    print("Done")
        #    break
        #text = page.text
        if not call_home(site):
            raise ValueError("Kill switch on-wiki is false. Terminating program.")
        page.text = page.text + "\n[[Category:El Paso Daily Times]]"
        print("Editing")
        print(len(text))
        print(len(page.text))
        page.save(
                summary="Adding to [[:Category:El Paso Daily Times]]" +
                        " ([[Commons:Bots/Requests/TheSandBot 3|BRFA]])", minor=True,
                botflag=True, force=True)
        #counter += 1
        add_to_db(page)
        #val = (str(page.title()), date.today())
        #mycursor.execute(sql, val)
        #mydb.commit()
        #print(mycursor.rowcount, "record inserted")

def add_to_db(page):
    sql = "INSERT INTO runs (title, date_added) VALUES (%s, %s)"
    val = (str(page.title()), date.today())
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")

def call_home(site_obj):
    page = pywikibot.Page(site_obj, 'User:TheSandBot/status')
    text = page.text
    data = json.loads(text)["run"]["elpaso_daily_times"]
    return str(data) == str(True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
