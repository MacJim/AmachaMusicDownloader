from ..helpers.DatabaseManager import DatabaseManager
from ..helpers.GoogleTranslationHelper import GoogleTranslationHelper
from ..helpers.DownloadAllMusic import downloadAllMusic
import os
import urllib.request
import time


class MusicDescriptionPagePipeline (object):
    def __init__(self):
        self.music = []

    def open_spider(self, spider):
        print("Music description page spider opened!")

    def process_item(self, item, spider):
        self.music.append(item)
        return item

    def close_spider(self, spider):
        self.translateMusicNamesAndInstruments()

        if (len(self.music) != 0):
            DatabaseManager.getInstance().updateMusicGeneralInformation(self.music)
            downloadAllMusic()

        print("Music description page spider closed!")

    def translateMusicNamesAndInstruments(self):
        stringsToTranslate = []    # [name1, instruments1, name2, instruments2, ...]

        for aPieceOfMusic in self.music:
            stringsToTranslate.append(aPieceOfMusic["name"])
            stringsToTranslate.append(aPieceOfMusic["instrumentsUsed"])

        translatedStrings = GoogleTranslationHelper.getInstance().translateStringsInTheSameLanguage(stringsToTranslate)

        for aPieceOfMusic in self.music:
            aPieceOfMusic["englishName"] = translatedStrings.pop(0)["translatedString"]
            aPieceOfMusic["instrumentsUsedEnglish"] = translatedStrings.pop(0)["translatedString"]

    # def downloadAllMusic(self):
    #     print("Starting music download!")

    #     self.existingMusicOnDisk = []    # Existing music on disk.
    #     self.successfullyDownloadMusic = []
    #     self.failedToDownloadMusic = []    # Failed-to-download music.

    #     musicStorageDirectory = os.path.join(os.getcwd(), "music")    # Directory path without the final '/' (Unix) or '\' (Windows).

    #     for aPieceOfMusic in self.music:
    #         downloadURL = aPieceOfMusic["downloadURL"]
    #         fileName = downloadURL.split("/")[-1]
    #         fileStoragePath = os.path.join(musicStorageDirectory, fileName)

    #         # See if a file or path exists at `fileStoragePath`
    #         if (os.path.isdir(fileStoragePath)):
    #             # (Unexpected) A folder exists on disk instead of a file.
    #             self.failedToDownloadMusic.append(aPieceOfMusic)
    #             print("A folder exists! Failed to download: ", downloadURL, sep = "")
    #         elif (os.path.isfile(fileStoragePath)):
    #             # (Skip this piece of music) A file exists on disk.
    #             self.existingMusicOnDisk.append(aPieceOfMusic)
    #             print("Skipped: ", downloadURL, sep = "")
    #         else:
    #             # Download this piece of music.
    #             try:
    #                 urllib.request.urlretrieve(downloadURL, fileStoragePath)
    #             # except urllib.request.ContentTooShortError:
    #             except:
    #                 self.failedToDownloadMusic.append(aPieceOfMusic)
    #                 print("Failed to download: ", downloadURL, sep = "")
    #             else:
    #                 self.successfullyDownloadMusic.append(aPieceOfMusic)
    #                 print("Successfully downloaded: ", downloadURL, sep = "")

    #             # Wait for a short period before downloading the next file. This is to reduce pressure on the target server.
    #             print("Waiting for 6 seconds before downloading the next file......6", end="")
    #             time.sleep(1)
    #             print("5", end="")
    #             time.sleep(1)
    #             print("4", end="")
    #             time.sleep(1)
    #             print("3", end="")
    #             time.sleep(1)
    #             print("2", end="")
    #             time.sleep(1)
    #             print("1", end="")
    #             time.sleep(1)

    #     # Print download summary
    #     print("Music download complete!")

    #     print("Existing music on disk:")
    #     for i in range(len(self.existingMusicOnDisk)):
    #         print(i, ". ", self.existingMusicOnDisk[i]["downloadURL"], sep = "")

    #     print("Successfully downloaded music:")
    #     for i in range(len(self.successfullyDownloadMusic)):
    #         print(i, ". ", self.successfullyDownloadMusic[i]["downloadURL"], sep = "")

    #     print("Failed-to-download music:")
    #     for i in range(len(self.failedToDownloadMusic)):
    #         print(i, ". ", self.failedToDownloadMusic[i]["downloadURL"], sep = "")
