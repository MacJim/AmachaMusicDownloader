import scrapy


class MainPageSpider (scrapy.Spider):
    """This class parses the main page URL http://amachamusic.chagasi.com/.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "AmachaMusicDownloader.pipelines.MainPagePipeline.MainPagePipeline": 100
        }
    }

    name = "mainPage"

    start_urls = ["http://amachamusic.chagasi.com/"]

    def parse(self, response):
        namesAndURLs = response.xpath("//ul[@class='menu']//a/text() | //ul[@class='menu']//a/@href").extract()

        if (len(namesAndURLs) % 2 == 0):    # If `namesAndURLs` has an even amount of elements (which is normal).
            namesAndURLsTuplesCount = int(len(namesAndURLs) / 2)
            for i in range(namesAndURLsTuplesCount):
                url = namesAndURLs[i * 2]
                name = namesAndURLs[i * 2 + 1]
                if ((not url.startswith("image_")) and (not url.startswith("genre_"))):    # Ignore useless links
                    continue
                else:
                    # url = "http://amachamusic.chagasi.com/" + url    # URLs in the website are relative rather than absolute.
                    # The `urljoin` method constructs an absolute url by combining the Response’s url with a possible relative url (URLs in the website are relative rather than absolute).
                    url = response.urljoin(url)

                    yield {
                    "URL": url,
                    "name": name
                }

        else:    # If `namesAndURLs` has an odd amount of elements (which is definitely abnormal).
            print("MJ Error: `namesAndURLs` has an odd amount (", len(namesAndURLs), ") of elements!")


    # def parse(self, response):
    #     """OLD IMPLEMENTATION!!!

    #     This legacy implementation may be released in a later snapshot."""
    #     imageOrGenreNames = []
    #     imageOrGenreURLs = []

    #     for imageOrGenreName in response.xpath("//ul[@class='menu']//a/text()"):
    #         # print(imageOrGenreName.extract())
    #         imageOrGenreNames.append(imageOrGenreName)

    #     for imageOrGenreURL in response.xpath("//ul[@class='menu']//a/@href"):
    #         # print(imageOrGenreURL.extract())
    #         imageOrGenreURLs.append(imageOrGenreURL)

    #     if (imageOrGenreNames.count() = imageOrGenreURLs.count()):
    #         for i in range(imageOrGenreNames.count()):
    #             imageOrGenreName
    #     else:
    #         print("MJ Error: `imageOrGenreNames` count (", imageOrGenreNames.count(), ") and `imageOrGenreURLs` count (", imageOrGenreURLs.count(), ") mismatch!", sep="")