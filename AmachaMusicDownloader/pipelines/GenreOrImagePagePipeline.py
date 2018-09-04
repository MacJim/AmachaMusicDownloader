# Please note that pipelines are not shared between multiple spiders in the same process and each spider gets its own pipeline instance.

from ..helpers.DatabaseManager import DatabaseManager


class GenreOrImagePagePipeline (object):
    def __init__(self):
        self.musicInformationArray = []    # A list of dictionary containing each piece of music's description page URL, genre ID or imageID.

    def open_spider(self, spider):
        print("Genre or image page spider opened!")

    def process_item(self, item, spider):
        self.musicInformationArray.append(item)
        return item

    def close_spider(self, spider):
        DatabaseManager.getInstance().updateMusicGenreOrImageInformation(self.musicInformationArray)
        print("Genre or image page spider closed!")