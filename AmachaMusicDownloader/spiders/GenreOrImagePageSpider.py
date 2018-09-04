import scrapy
from ..helpers.DatabaseManager import DatabaseManager


class GenreOrImagePageSpider (scrapy.Spider):
    """This class parses all genres and images pages (for example http://amachamusic.chagasi.com/image_akarui.html) and stores:
    1. Each piece of music's description page URL.
    2. Each piece of music's genre and image (these information might be updated in case the description page URL already exists in the database).
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "AmachaMusicDownloader.pipelines.GenreOrImagePagePipeline.GenreOrImagePagePipeline": 100
        }
    }

    name = "genreOrImagePages"

    # def __init__(self):
    #     self.type = ""    # "genre" for a genre; "image" for an image; any other value is undefined.
    #     self.genreID = 0    # Genre ID in database. 0 for N/A.
    #     self.imageID = 0    # Image ID in database. 0 for N/A.

    def start_requests(self):
        # MARK: This is just a placeholder method. Subclasses must implement this method to read genres' or images' URLs from database.
        # with open("urls.txt", "rb") as urls:
        #     for url in urls:
        #         yield scrapy.Request(url, self.parse)
        # The `meta` dictionary contains information about the request URL, such as type (genre or image), genre ID, image ID.
        allGenresInformation = DatabaseManager.getInstance().getAllGenresInformation()
        allImagesInformation = DatabaseManager.getInstance().getAllImagesInformation()

        for genreInformation in allGenresInformation:
            genreURL = genreInformation["url"]
            request = scrapy.Request(genreURL, callback = self.parse, meta = {
                "type": "genre",
                "genreID": genreInformation["genreID"]
            })
            yield request

        for imageInformation in allImagesInformation:
            imageURL = imageInformation["url"]
            request = scrapy.Request(imageURL, callback = self.parse, meta = {
                "type": "image",
                "imageID": imageInformation["imageID"]
            })
            yield request

    def parse(self, response):
        pageType = response.meta["type"]    # "genre" or "image"
        genreID = None
        imageID = None
        if (pageType == "genre"):
            genreID = response.meta["genreID"]
        elif (pageType == "image"):
            imageID = response.meta["imageID"]
        else:
            print("MJ Error: unsupported page type", pageType)

        musicDescriptionPageURLs = response.xpath("//div[@class='download']//a/@href").extract()

        for url in musicDescriptionPageURLs:
            joinedURL = response.urljoin(url)
            if ((genreID is not None) and (imageID is None)):
                yield {
                    "descriptionPageURL": joinedURL,
                    "type": pageType,
                    "genreID": genreID
                }
            elif ((genreID is None) and (imageID is not None)):
                yield {
                    "descriptionPageURL": joinedURL,
                    "type": pageType,
                    "imageID": imageID
                }

        currentPageIndex = response.xpath("//ul[@class='pager']//strong/text()").extract()[0]    # Note: This is a string (not int)!

        otherPagesIndexes = response.xpath("//ul[@class='pager']//a/text()").extract()    # Note: These are strings (not integers)!
        otherPagesURLs = response.xpath("//ul[@class='pager']//a/@href").extract()
        otherPagesDictionary = dict(zip(otherPagesIndexes, otherPagesURLs))    # index: URL

        nextPageIndex = str(int(currentPageIndex) + 1)    # Note: This is a string (not int)!
        if (nextPageIndex in otherPagesIndexes):
            nextPageURL = response.urljoin(otherPagesDictionary[nextPageIndex])
            yield scrapy.Request(nextPageURL, callback = self.parse, meta = response.meta)