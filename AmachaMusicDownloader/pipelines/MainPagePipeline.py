from scrapy.exceptions import DropItem
from ..helpers.DatabaseManager import DatabaseManager
from ..helpers.GoogleTranslationHelper import GoogleTranslationHelper


class MainPagePipeline (object):
    def __init__(self):
        self.genres = []
        self.images = []

    def open_spider(self, spider):
        print("Main page spider opened!")

    def process_item(self, item, spider):
        if ("genre_" in item["URL"]):
            self.genres.append(item)
        elif ("image_" in item["URL"]):
            self.images.append(item)
        else:
            print("MJ Error: cannot judge item kind from its URL.")
            raise DropItem

        return item

    def close_spider(self, spider):
        self.translateGenreOrImageNames()
        # print(self.genres)
        # print(self.images)
        if ((len(self.genres) != 0) and (len(self.images) != 0)):
            DatabaseManager.getInstance().deleteAllGenres()
            DatabaseManager.getInstance().deleteAllImages()
            DatabaseManager.getInstance().addGenres(self.genres)
            DatabaseManager.getInstance().addImages(self.images)

        print("Main page spider closed!")

    def translateGenreOrImageNames(self):
        """Translate `self.genres` and `self.images`.

        Before translation (each dictionary in either array):
            {
                "name": "明るい",
                "URL": "http://amachamusic.chagasi.com/image_akarui.html"
            }

        After translation (each dictionary in either array):
            {
                "name": "明るい",
                "URL": "http://amachamusic.chagasi.com/image_akarui.html",
                "englishName": "bright"
            }
        """

        namesToTranslate = []

        for aGenre in self.genres:
            namesToTranslate.append(aGenre["name"])

        for anImage in self.images:
            namesToTranslate.append(anImage["name"])

        translatedStrings = GoogleTranslationHelper.getInstance().translateStringsInTheSameLanguage(namesToTranslate)

        for aGenre in self.genres:
            aGenre["englishName"] = translatedStrings.pop(0)["translatedString"]

        for anImage in self.images:
            anImage["englishName"] = translatedStrings.pop(0)["translatedString"]