import os
# from shutil import get_terminal_size

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import scrapy.settings

from AmachaMusicDownloader.spiders.MainPageSpider import MainPageSpider
from AmachaMusicDownloader.spiders.GenreOrImagePageSpider import GenreOrImagePageSpider
from AmachaMusicDownloader.spiders.MusicDescriptionPageSpider import MusicDescriptionPageSpider

from AmachaMusicDownloader.helpers.DatabaseManager import DatabaseManager
import AmachaMusicDownloader.helpers.DownloadAllMusic
import AmachaMusicDownloader.helpers.getch
import AmachaMusicDownloader.helpers.FileLauncher


# runner = CrawlerRunner(get_project_settings())

# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(MainPageSpider)
#     yield runner.crawl(GenreOrImagePageSpider)
#     yield runner.crawl(MusicDescriptionPageSpider)
#     reactor.stop()

# crawl()
# reactor.run() # the script will block here until the last crawl call is finished



# from scrapy.crawler import CrawlerProcess
# process = CrawlerProcess(get_project_settings())

# process.crawl(MainPageSpider)
# process.start()    # The script will block here until the crawling is finished.
# process.crawl(GenreOrImagePageSpider)
# process.start()
# process.crawl(MusicDescriptionPageSpider)
# process.start()


# TODO: Remove
# print(scrapy.settings.default_settings, sep = "\n")
# print("Project settings:", get_project_settings().__dict__, sep = "\n")
# AmachaMusicDownloader.helpers.getch.getch()


# MARK: Script helper functions.
def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def printALineOfSeparator():
    print("------------------------------------")

def printAllGenresInformation():
    print("Genres:")
    allGenres = DatabaseManager.getInstance().getAllGenresInformation()
    for aGenre in allGenres:
        print(aGenre["genreID"], ". ", aGenre["japaneseName"], " ", aGenre["englishName"], sep = "")

def printAllImagesInformation():
    print("Images:")
    allImages = DatabaseManager.getInstance().getAllImagesInformation()
    for anImage in allImages:
        print(anImage["imageID"], ". ", anImage["japaneseName"], " ", anImage["englishName"])

def printMusicInformation(musicInformation):
    """Prints a single piece of music's **full** information.
    """
    print("Music ID:", musicInformation["musicID"])
    print("Japanese name:", musicInformation["japaneseName"])
    print("English name:", musicInformation["englishName"])
    print("Release date:", musicInformation["releaseDate"])

    genre1ID = musicInformation["genre1ID"]
    genre2ID = musicInformation["genre2ID"]
    image1ID = musicInformation["image1ID"]
    image2ID = musicInformation["image2ID"]
    if (genre1ID is not None):
        genre1Information = DatabaseManager.getInstance().searchForGenreWithGenreID(genre1ID)
        print("Genre 1:", genre1Information["japaneseName"], genre1Information["englishName"])
    if (genre2ID is not None):
        genre2Information = DatabaseManager.getInstance().searchForGenreWithGenreID(genre2ID)
        print("Genre 2:", genre2Information["japaneseName"], genre2Information["englishName"])
    if (image1ID is not None):
        image1Information = DatabaseManager.getInstance().searchForGenreWithGenreID(image1ID)
        print("Image 1:", image1Information["japaneseName"], image1Information["englishName"])
    if (image2ID is not None):
        image2Information = DatabaseManager.getInstance().searchForGenreWithGenreID(image2ID)
        print("Image 2:", image2Information["japaneseName"], image2Information["englishName"])

    print("Length:", musicInformation["length"])
    print("File size:", musicInformation["fileSize"])
    print("Instruments used (Japanese):", musicInformation["instrumentsUsedJapanese"])
    print("Instruments used (English):", musicInformation["instrumentsUsedEnglish"])

    loveLevel = musicInformation["loveLevel"]
    loveLevelText = ""
    if (loveLevel == 0):
        loveLevelText = "Hate"
    elif (loveLevel == 1):
        loveLevelText = "Dislike"
    elif (loveLevel == 2):
        loveLevelText = "Mediocre"
    elif (loveLevel == 3):
        loveLevelText = "Like"
    elif (loveLevel == 4):
        loveLevelText = "Love"
    else:
        loveLevelText = "Unspecified"
    print("Love level:", loveLevelText)

    print("Comments:", musicInformation["comments"])

    # suitability = musicInformation["suitability"]
    # if (suitability is None):
    #     print("Suitability: Unspecified")
    # else:
    #     suitabilityTexts = []
    #     if ((suitability & 1) == 1):
    #         suitabilityTexts.append("Game BGM")
    #     if ((suitability & 2) == 2):
    #         suitabilityTexts.append("Soothing")

    #     if (len(suitabilityTexts) == 0):
    #         print("Suitability: None")
    #     else:
    #         print("Suitability: ", end = "")
    #         for i in range(len(suitabilityTexts)):
    #             if (i != 0):
    #                 print(", ", end = "")
    #             print(suitabilityTexts[i], end = "")

def printAnArrayOfMusicInformation(musicInformationArray):
    musicCount = len(musicInformationArray)
    if (musicCount <= 0):
        return    # Print nothing.
    
    print(musicCount, "pieces of music in total.")

    for musicInformation in musicInformationArray:
        printALineOfSeparator()
        printMusicInformation(musicInformation)

    printALineOfSeparator()
    
    # TODO: Sort music by love level.
    # print("Sorting form love to hate:")
    # TODO: Use pydoc.pager

def openMusicFileNamed(fileName):
    if (fileName[-4:] != ".mp3"):
            fileName += ".mp3"
    filePath = os.path.join(os.getcwd(), "music", fileName)
    AmachaMusicDownloader.helpers.FileLauncher.openAFile(filePath)


# MARK: Script menus.
def enterScraperAndDownloaderMenu():
    while (True):
        clearTerminal()

        print("Scrape or download music from the Amacha website.")
        print("1. Scrap and update all music's information and download them to disk.")
        print("2. Run main page spider.")
        print("3. Run Genre & Image pages spider.")
        print("4. Run music description pages spider.")
        print("5. Download all music.")
        print("0. Return to main menu.")
        print("Press 1 if you're unsure.")

        # TODO:
        userInput = AmachaMusicDownloader.helpers.getch.getch()

        if (userInput == "0"):
            break

        elif (userInput == "5"):
            clearTerminal()
            AmachaMusicDownloader.helpers.DownloadAllMusic.downloadAllMusic()
            AmachaMusicDownloader.helpers.getch.pressAnyKeyToContinue()

def enterFindMusicMenu():
    while (True):
        clearTerminal()

        print("Find music in local database.")
        print("1. Find music by internal ID.")
        print("2. Find music by Japanese name.")
        print("3. Find music by file name.")
        print("4. Find music by genre and / or image.")
        print("5. Find music by description.")
        print("0. Return to main menu.")

        userInput = AmachaMusicDownloader.helpers.getch.getch()

        if (userInput == "0"):
            # Return to main menu.
            break

        if (userInput == "1"):
            # Find music by ID.
            musicID = input("Music ID: ")
            musicInformation = DatabaseManager.getInstance().searchForMusicWithMusicID(musicID)

            if (musicInformation is None):
                print("Music not found!")
            else:
                printMusicInformation(musicInformation)

        elif (userInput == "2"):
            # Find music by Japanese name.
            japaneseName = input("Music Japanese name: ")
            musicInformation = DatabaseManager.getInstance().searchForMusicWithJapaneseName(japaneseName)

            if (musicInformation is None):
                print("Music not found!")
            else:
                printMusicInformation(musicInformation)

        elif (userInput == "3"):
            # Find music by file name.
            fileName = input("Music file name: ")
            musicInformation = DatabaseManager.getInstance().searchForMusicWithFileName(fileName)

            if (musicInformation is None):
                print("Music not found!")
            else:
                printMusicInformation(musicInformation)

        elif (userInput == "4"):
            # Find music by genre and / or image.
            printALineOfSeparator()
            printAllGenresInformation()
            printALineOfSeparator()
            printAllImagesInformation()
            printALineOfSeparator()

            genreID = input("Genre ID (type nothing for wildcard): ")
            imageID = input("Image ID (type nothing for wildcard): ")

            printALineOfSeparator()

            musicFound = DatabaseManager.getInstance().searchForMusicWithGenreIDAndImageID(genreID, imageID)

            if (len(musicFound) == 0):
                print("No music found!")
            else:
                printAnArrayOfMusicInformation(musicFound)

        elif (userInput == "5"):
            commentsSnippet = input("Comments snippet: ")

            printALineOfSeparator()

            musicFound = DatabaseManager.getInstance().searchForMusicWithCommentsSnippet(commentsSnippet)

            if (len(musicFound) == 0):
                print("No music found!")
            else:
                printAnArrayOfMusicInformation(musicFound)

        AmachaMusicDownloader.helpers.getch.pressAnyKeyToContinue()

def enterAppraiseMusicMenu():
    while (True):
        clearTerminal()

        print("Appraise music in local database.")
        print("1. Appraise a random piece of unassessed music.")
        print("2. Appraise a random piece of unassessed music from a specific genre and / or image.")
        print("3. Appraise a specific piece of music.")
        print("4. Update music love level, comments and suitability manually.")
        print("0. Return to main menu.")

        userInput = AmachaMusicDownloader.helpers.getch.getch()

        if (userInput == "0"):
            # Return to main menu.
            break

        musicInformation = None
        musicFileName = None

        if (userInput == "1"):
            musicInformation = DatabaseManager.getInstance().getRandomUnassessedMusic(None, None)

        elif (userInput == "2"):
            printALineOfSeparator()
            printAllGenresInformation()
            printALineOfSeparator()
            printAllImagesInformation()
            printALineOfSeparator()

            genreID = input("Genre ID (type nothing for wildcard): ")
            imageID = input("Image ID (type nothing for wildcard): ")

            printALineOfSeparator()

            musicInformation = DatabaseManager.getInstance().getRandomUnassessedMusic(genreID, imageID)

        elif ((userInput == "3") or (userInput == "4")):
            musicFileName = None

            musicIDOrFileName = input("Music ID or file name: ")
            if (musicIDOrFileName.isdigit()):
                musicID = int(musicIDOrFileName)
                musicInformation = DatabaseManager.getInstance().searchForMusicWithMusicID(musicID)
            else:
                musicFileName = musicIDOrFileName
                musicInformation = DatabaseManager.getInstance().searchForMusicWithFileName(musicFileName)

        else:    # Invalid input handling.
            continue

        if (musicInformation is None):
            print("Music not found!")
        else:
            # print("Current love level: ", end = "")
            if (musicFileName is None):
                musicFileName = DatabaseManager.getInstance().extractMusicFileNameFromDownloadURL(musicInformation["downloadURL"])

            if (userInput != "4"):
                openMusicFileNamed(musicFileName)

            printMusicInformation(musicInformation)

            newLoveLevel = input("New love level (0 ~ 4, 0 = hate, 4 = love): ")
            newComments = input("Comments: ")

            if (newLoveLevel != ""):
                DatabaseManager.getInstance().updateMusicLoveLevel(musicInformation["musicID"], newLoveLevel)
            if (newComments != ""):
                DatabaseManager.getInstance().updateMusicComments(musicInformation["musicID"], newComments)

        AmachaMusicDownloader.helpers.getch.pressAnyKeyToContinue()


# MARK: Main program.
# 1. Switch to project directory.
mainFilePath = os.path.dirname(os.path.abspath(__file__))
os.chdir(mainFilePath)

# 2. Create "AmachaMusicDownloader.db" if it does not exist.
if (not os.path.isfile(os.path.join(os.getcwd(), "AmachaMusicDownloader.db"))):
    print("Welcome to Amacha Music Downloader by MacJim!")
    print("Scraping the whole Amacha website may take a long time. You may consider running this script in a \"screen\" session.")
    print("This seems to be the first time you run this script. Would you like to create the database file in the project folder? (Yes/No) ")

    userInput = input()

    if ((userInput == "Yes") or (userInput == "yes") or (userInput == "Y") or (userInput == "y")):
        # 2-1. Execute "Documentation/Create tables.sql" file.
        DatabaseManager.getInstance().createTables()
    else:
        # 2-2. Prompt and exit.
        print("You have chosen NOT to create the database file. You may create it manually using the following command:\nsqlite3 AmachaMusicDownloader.db < Documentation/Create\\ tables.sql")
        exit()

# 3. Script main menu.
while True:
    clearTerminal()

    print("Amacha music downloader by MacJim")
    print("1. Scrape and / or download music from the Amacha website.")
    print("2. Find music in local database.")
    print("3. Appraise music in local database.")
    print("0. Exit.")

    # NO confirmation here. No need to press ENTER 😝.
    userInput = AmachaMusicDownloader.helpers.getch.getch()

    if (userInput == "0"):
        exit()

    elif (userInput == "1"):
        enterScraperAndDownloaderMenu()

    elif (userInput == "2"):
        enterFindMusicMenu()

    elif (userInput == "3"):
        enterAppraiseMusicMenu()
