import pywikibot
import re
import mysql.connector
import json
from datetime import date

site = pywikibot.Site('commons','commons')
search_generator = site.search('"El Paso Daily Times. (El Paso, Tex.), Vol"')
igen = iter(search_generator)
counter = 0
mydb = mysql.connector.connect(
  host="localhost",
  user="newuser",
  password="password",
  database="commons_task3_run"
)
mycursor = mydb.cursor()

search_sql = "SELECT title FROM runs WHERE title = '%s'"

def main():
    for page in igen:
        mycursor.execute(search_sql, page.title())
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            print("Already done")
            continue
        else:
            text = page.text
            search_result = re.search("Category:El Paso Daily Times", text)
            if search_result:
                add_to_db(page)
                continue # already done, move on
        #if counter >4:
        #    print("Done")
        #    break
        #text = page.text
        if not call_home(site):
            raise ValueError("Kill switch on-wiki is false. Terminating program.")
        page.text = page.text + "\n[[Category:El Paso Daily Times]]"
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
