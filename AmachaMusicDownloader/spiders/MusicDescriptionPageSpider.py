import scrapy
from ..helpers.DatabaseManager import DatabaseManager


class MusicDescriptionPageSpider (scrapy.Spider):
    """This class parses all music description pages (for example http://amachamusic.chagasi.com/music_shoujorei.html) and updates each piece of music's:
    1. Name (Japanese and English).
    2. Release date.
    3. Length.
    4. File size.
    5. Instrument used (Japanese and English).
    6. Download URL.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "AmachaMusicDownloader.pipelines.MusicDescriptionPagePipeline.MusicDescriptionPagePipeline": 100
        }
    }

    name = "musicDescriptionPages"

    start_urls = []

    def start_requests(self):
        allMusicInformation = DatabaseManager.getInstance().getAllMusicInformation()

        for musicInformation in allMusicInformation:
            musicDescriptionPageURL = musicInformation["descriptionPageURL"]
            request = scrapy.Request(musicDescriptionPageURL, callback = self.parse, meta = {
                "musicID": musicInformation["musicID"]
            })
            yield request

    def parse(self, response):
        # 1. Music ID
        musicID = response.meta["musicID"]

        # 2. Music name
        musicName = response.xpath("//div[@class='download_box']/div[@class='download_title']/text()").extract()[0]    # Note: name has additional '\n's on both ends.
        # musicName = musicNameText.translate(dict.fromkeys({ord(c): None for c in '\n\t'}))
        musicName = musicName.translate({ord('\n'): None})    # Remove '\n's from music name.

        # 3. Music metadata
        fullMetadataArray = response.xpath("//div[@class='download_box']/div[@class='download_data']/text()").extract()

        # 3-1. Release date, length, file size
        firstMetadataLine = fullMetadataArray[0]
        firstMetadataLine = firstMetadataLine.translate({ord('\n'): None})    # Remove '\n's.

        splittedFirstMetadataLine = firstMetadataLine.split(" | ")

        releaseDate = splittedFirstMetadataLine[0]
        length = splittedFirstMetadataLine[-1].split("/")[0]
        fileSize = splittedFirstMetadataLine[-1].split("/")[1]

        # 3-2. Instruments used
        instrumentsUsed = fullMetadataArray[1]
        instrumentsUsed = instrumentsUsed.translate({ord('\n'): None})    # Remove '\n's.
        if (instrumentsUsed[0:5] == "使用楽器："):
            # Remove "使用楽器："
            instrumentsUsed = instrumentsUsed[5:]

        # 4. Download URL
        downloadURL = response.xpath("//div[@class='download_box']/div[@class='download_mp3']/a/@href").extract()[0]
        downloadURL = response.urljoin(downloadURL)

        yield {
            "musicID": musicID,
            "name": musicName,
            "releaseDate": releaseDate,
            "length": length,
            "fileSize": fileSize,
            "instrumentsUsed": instrumentsUsed,
            "downloadURL": downloadURL
        }
