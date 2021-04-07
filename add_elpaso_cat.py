import pywikibot
import re
site = pywikibot.Site('commons','commons')
search_generator = site.search('"El Paso Daily Times. (El Paso, Tex.), Vol"')
igen = iter(search_generator)
for i in igen:
    try:
        page = next(temp)
    except StopIteration:
        pass

    text = page.text
    search_result = re.search("Category:El Paso Daily Times", text)
    if search_result:
        continue # already done, move on
    page.text = page.text += "[[Category:El Paso Daily Times]]"
    page.save(
        summary="Adding to [[:Category:El Paso Daily Times]]" +
                " ([[Wikipedia:Bots/Requests for approval/" + self.brfa + "|BRFA]])", minor=True,
        botflag=True, force=True)
