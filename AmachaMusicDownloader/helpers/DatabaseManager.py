import sqlite3


class DatabaseManager:
# MARK: Database setting
    databaseName = "AmachaMusicDownloader"
    databaseFilename = "AmachaMusicDownloader.db"

    genresTableName = "Genres"
    imagesTableName = "Images"
    musicTableName = "Music"


# MARK: Singleton stuff
    _sharedInstance = None

    @staticmethod
    def getInstance():
        if (DatabaseManager._sharedInstance is None):
            _sharedInstance = DatabaseManager()

        return _sharedInstance


# MARK: Constructors and destructors
    def __init__(self):
        self.databaseConnection = sqlite3.connect(DatabaseManager.databaseFilename)
        self.databaseConnection.row_factory = sqlite3.Row
        self.databaseConnection.execute("PRAGMA foreign_keys = ON")
        self.databaseCursor = self.databaseConnection.cursor()

    def __del__(self):
        # super.__del__(self)
        if (hasattr(self, "databaseCursor")):
            self.databaseCursor.close()

        if (hasattr(self, "databaseConnection")):
            self.databaseConnection.commit()
            self.databaseConnection.close()


# MARK: Create tables
    def createTables(self):
        createTablesSQLFileContent = open('Documentation/Create tables.sql', 'r').read()
        self.databaseCursor.executescript(createTablesSQLFileContent)
        self.databaseConnection.commit()


# MARK: Genres and Images tables
    def searchForGenreWithGenreID(self, genreID):
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.genresTableName + " WHERE genreID=?", (genreID,))
        return self.databaseCursor.fetchone()

    def getAllGenresInformation(self):
        """
        Returns:
            list: A list of lists containing genres' information. The order of each list is the same as the table's structure (defined in /Documentation/Create Tables.sql).
        """
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.genresTableName)
        return self.databaseCursor.fetchall()

    def deleteAllGenres(self):
        """Deletes all genres.
        """
        self.databaseCursor.execute("DELETE FROM " + DatabaseManager.genresTableName)
        self.databaseConnection.commit()

    def addGenres(self, genresInformationToAdd):
        """Adds genre information.

        Args:
            genresInformationToAdd (list): A list of dictionaries. This method searches for the following keys in each dictionary:
                1. name: The genre's Japanese name.
                2. englishName: The genre's English name.
                3. URL: The genre's main page URL.

        Returns:
            bool: `True` if the update succeeded; `False` if not.
        """

        if ((genresInformationToAdd is None) or (len(genresInformationToAdd) == 0)):
            print("MJ Error: latestGenresInformation count is 0!")
            return False

        for genreInformation in genresInformationToAdd:
            japaneseName = genreInformation["name"]
            englishName = genreInformation["englishName"]
            url = genreInformation["URL"]

            self.databaseCursor.execute("INSERT INTO " + DatabaseManager.genresTableName + " VALUES(NULL, ?, ?, ?)", (japaneseName, englishName, url))

        self.databaseConnection.commit()

    def searchForImageWithImageID(self, imageID):
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.imagesTableName + " WHERE imageID=?", (imageID,))
        return self.databaseCursor.fetchone()

    def getAllImagesInformation(self):
        """
        Returns:
            list: A list of lists containing images' information. The order of each list is the same as the table's structure (defined in /Documentation/Create Tables.sql).
        """
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.imagesTableName)
        return self.databaseCursor.fetchall()

    def deleteAllImages(self):
        """Deletes all images.
        """
        self.databaseCursor.execute("DELETE FROM " + DatabaseManager.imagesTableName)
        self.databaseConnection.commit()

    def addImages(self, imagesInformationToAdd):
        """(Similar to `addGenres`)

        Args:
            imagesInformationToAdd (list)

        Returns:
            bool: `true` if the update succeeded; `false` if not.
        """
        if ((imagesInformationToAdd is None) or (len(imagesInformationToAdd) == 0)):
            print("MJ Error: imagesInformationToAdd count is 0!")
            return False

        for imageInformation in imagesInformationToAdd:
            japaneseName = imageInformation["name"]
            englishName = imageInformation["englishName"]
            url = imageInformation["URL"]

            self.databaseCursor.execute("INSERT INTO " + DatabaseManager.imagesTableName + " VALUES(NULL, ?, ?, ?)", (japaneseName, englishName, url))

        self.databaseConnection.commit()


# MARK: Music table
    def searchForMusicWithMusicID(self, musicID):
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE musicID=?", (musicID,))
        return self.databaseCursor.fetchone()    # Returns only the first result since music IDs are unique.

    def searchForMusicWithDescriptionPageURL(self, url):
        """Search for music information in database with the given URL.

        Returns `None` if none exists.
        """
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE descriptionPageURL=?", (url,))
        return self.databaseCursor.fetchone()    # Returns only the first result since URLs are unique.

    def searchForMusicWithJapaneseName(self, japaneseName):
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE japaneseName=?", (japaneseName,))
        return self.databaseCursor.fetchone()

    def searchForMusicWithFileName(self, fileName):
        """File names are stored in the database as part of the download URL.

        File extension ".mp3" can be omitted.
        """
        if (fileName[-4:] != ".mp3"):
            fileName += ".mp3"

        # self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE downloadURL LIKE '%?'", (fileName,))    # This does not work 😭...
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE downloadURL LIKE '%" + fileName + "'")    # Although prone to injections, this works...
        return self.databaseCursor.fetchone()    # Returns only the first result since file names are unique.

    def searchForMusicWithGenreIDAndImageID(self, genreID, imageID):
        if (((genreID is None) or (genreID == "")) and ((imageID is None) or (imageID == ""))):
            return []

        if (((genreID is not None) and (genreID != "")) and ((imageID is None) or (imageID == ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE genre1ID=? OR genre2ID=?", (genreID, genreID))
        elif (((genreID is None) or (genreID == "")) and ((imageID is not None) and (imageID != ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE image1ID=? OR image2ID=?", (imageID, imageID))
        elif (((genreID is not None) and (genreID != "")) and ((imageID is not None) and (imageID != ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE (genre1ID=? OR genre2ID=?) AND (image1ID=? OR image2ID=?)", (genreID, genreID, imageID, imageID))

        return self.databaseCursor.fetchall()

    def searchForMusicWithCommentsSnippet(self, commentsSnippet):
        if (commentsSnippet is None):
            return []

        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE comments LIKE '%" + commentsSnippet + "%'")
        return self.databaseCursor.fetchall()

    def getRandomUnassessedMusic(self, genreID, imageID):
        """Get a random piece of unassessed music.

        Unassessed music have its `loveLevel` column set to `NULL`.
        """
        # TODO:
        if (((genreID is None) or (genreID == "")) and ((imageID is None) or (imageID == ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE loveLevel IS NULL ORDER BY RANDOM() LIMIT 1")
        elif (((genreID is not None) and (genreID != "")) and ((imageID is None) or (imageID == ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE (loveLevel IS NULL) AND (genre1ID=? OR genre2ID=?) ORDER BY RANDOM() LIMIT 1", (genreID, genreID))
        elif (((genreID is None) or (genreID == "")) and ((imageID is not None) and (imageID != ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE (loveLevel IS NULL) AND (image1ID=? OR image2ID=?) ORDER BY RANDOM() LIMIT 1", (imageID, imageID))
        elif (((genreID is not None) and (genreID != "")) and ((imageID is not None) and (imageID != ""))):
            self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName + " WHERE (loveLevel IS NULL) AND (genre1ID=? OR genre2ID=?) AND (image1ID=? OR image2ID=?) ORDER BY RANDOM() LIMIT 1", (genreID, genreID, imageID, imageID))

        return self.databaseCursor.fetchone()

    def getAllMusicInformation(self):
        """
        Returns:
            list: A list of lists containing genres' information. The order of each list is the same as the table's structure (defined in /Documentation/Create Tables.sql).
        """
        self.databaseCursor.execute("SELECT * FROM " + DatabaseManager.musicTableName)
        return self.databaseCursor.fetchall()

    def getAllMusicDownloadURLs(self):
        """
        Returns:
            list: A list of downloadable URLs (not tuples).
        """
        self.databaseCursor.execute("SELECT downloadURL FROM " + DatabaseManager.musicTableName)
        return [aResult["downloadURL"] for aResult in self.databaseCursor.fetchall()]

    # def clearMusicGenreOrImageInformation(self):
    #     """Set all music's `genre1ID`, `genre2ID`, `image1ID`, `image2ID` fields to NULL.
    #     """

    def updateMusicGenreOrImageInformation(self, musicInformationArray):
        """Adds or updates a group of music's information to database.

        This method only updates the `genre1ID`, `genre2ID`, `image1ID`, `image2ID` and `descriptionPageURL` columns of the `Music` table. No other columns are affected.

        Args:
            musicInformationArray (list): A list of dictionary containing each piece of music's URL, genre ID or imageID.
        """
        for musicInformation in musicInformationArray:
            # 1. Retrieve current music information.
            descriptionPageURL = musicInformation["descriptionPageURL"]
            genreOrImageType = musicInformation["type"]
            if (genreOrImageType == "genre"):
                genreID = musicInformation["genreID"]
            elif (genreOrImageType == "image"):
                imageID = musicInformation["imageID"]

            # 2. Create music entry in database if it does not exist.
            musicInformationInDatabase = self.searchForMusicWithDescriptionPageURL(descriptionPageURL)
            if (musicInformationInDatabase is None):
                # Create music
                self.databaseCursor.execute("INSERT INTO " + DatabaseManager.musicTableName + " VALUES(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, ?, NULL, NULL)", (descriptionPageURL,))
                musicInformationInDatabase = self.searchForMusicWithDescriptionPageURL(descriptionPageURL)

            # 3. Update music genre or image type.
            musicID = musicInformationInDatabase[0]
            if (genreOrImageType == "genre"):
                # 3-1. Update music genre ID.
                musicGenre1IDInDatabase = musicInformationInDatabase[4]    # `genre1ID` value in database.
                musicGenre2IDInDatabase = musicInformationInDatabase[5]    # `genre2ID` value in database.
                if (musicGenre1IDInDatabase is None):
                    self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET genre1ID=? WHERE musicID=?", (genreID, musicID))
                elif (musicGenre2IDInDatabase is None):
                    self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET genre2ID=? WHERE musicID=?", (genreID, musicID))
            elif (genreOrImageType == "image"):
                # 3-2. Update music image ID.
                musicImage1IDInDatabase = musicInformationInDatabase[6]    # `image1ID` value in database.
                musicImage2IDInDatabase = musicInformationInDatabase[7]    # `image2ID` value in database.
                if (musicImage1IDInDatabase is None):
                    self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET image1ID=? WHERE musicID=?", (imageID, musicID))
                elif (musicImage2IDInDatabase is None):
                    self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET image2ID=? WHERE musicID=?", (imageID, musicID))

        self.databaseConnection.commit()

    def updateMusicGeneralInformation(self, musicInformationArray):
        """Updates the `japaneseName`, `englishName`, `releaseDate`, `length`, `fileSize`, `instrumentsUsedJapanese`, `instrumentsUsedEnglish`, `downloadURL` columns of the `Music` table. No other columns are affected.
        """
        for musicInformation in musicInformationArray:
            self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET japaneseName=?, englishName=?, releaseDate=?, length=?, fileSize=?, instrumentsUsedJapanese=?, instrumentsUsedEnglish=?, downloadURL=? WHERE musicID=?", (musicInformation["name"], musicInformation["englishName"], musicInformation["releaseDate"], musicInformation["length"], musicInformation["fileSize"], musicInformation["instrumentsUsed"], musicInformation["instrumentsUsedEnglish"], musicInformation["downloadURL"], musicInformation["musicID"]))

        self.databaseConnection.commit()

    def updateMusicLoveLevel(self, musicID, loveLevel):
        # musicInformation = self.searchForMusicWithFileName(fileName)
        # if (musicInformation is not None):
        #     musicID = musicInformation[0]
        self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET loveLevel=? WHERE musicID=?", (loveLevel, musicID))
        self.databaseConnection.commit()

    def updateMusicComments(self, musicID, comments):
        self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET comments=? WHERE musicID=?", (comments, musicID))
        self.databaseConnection.commit()

    # def updateMusicSuitability(self, musicID, gameBGM, soothing):
    #     suitability = gameBGM + soothing * 2
    #     self.databaseCursor.execute("UPDATE " + DatabaseManager.musicTableName + " SET suitability=? WHERE musicID=?", (suitability, musicID))

    def extractMusicFileNameFromDownloadURL(self, url):
        return url.split("/")[-1]

    def getMusicStatistics(self):
        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName)
        totalMusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel IS NOT NULL")
        assessedMusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel=4")
        loveLevel4MusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel=3")
        loveLevel3MusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel=2")
        loveLevel2MusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel=1")
        loveLevel1MusicCount = self.databaseCursor.fetchone()[0]

        self.databaseCursor.execute("SELECT count(*) FROM " + DatabaseManager.musicTableName + " WHERE loveLevel=0")
        loveLevel0MusicCount = self.databaseCursor.fetchone()[0]

        return {
            "totalMusicCount": totalMusicCount,
            "assessedMusicCount": assessedMusicCount,
            "loveLevel4MusicCount": loveLevel4MusicCount,
            "loveLevel3MusicCount": loveLevel3MusicCount,
            "loveLevel2MusicCount": loveLevel2MusicCount,
            "loveLevel1MusicCount": loveLevel1MusicCount,
            "loveLevel0MusicCount": loveLevel0MusicCount
        }



# MARK: For testing only.
# print(DatabaseManager.getInstance().searchForMusicWithURL("???"))    # An empty list.
# print(DatabaseManager.getInstance().searchForMusicWithURL("http://amachamusic.chagasi.com/genre_hollywood.html"))
# print(DatabaseManager.getInstance().searchForMusicWithDescriptionPageURL("http://www.example.com/")[4])

# DatabaseManager.getInstance().addMusic([{
#     "descriptionPageURL": "https://www.example.com",
#     "type": "genre",
#     "genreID": 2
# }])
# DatabaseManager.getInstance().addMusic([{
#     "descriptionPageURL": "https://www.example.com",
#     "type": "image",
#     "imageID": 3
# }])
# DatabaseManager.getInstance().addMusic([{
#     "descriptionPageURL": "https://www.example.com",
#     "type": "genre",
#     "genreID": 4
# }])
# DatabaseManager.getInstance().addMusic([{
#     "descriptionPageURL": "https://www.example.com",
#     "type": "image",
#     "imageID": 5
# }])

# print(DatabaseManager.getInstance().searchForMusicWithFileName("1950danosekkin.mp3"))
# print(DatabaseManager.getInstance().searchForMusicWithFileName("akinonowoiku"))

# print(DatabaseManager.getInstance().getAllMusicDownloadURLs())

# for aRowObject in DatabaseManager.getInstance().searchForMusicWithGenreIDAndImageID(9, 7):
#     for member in aRowObject:
#         print(member)

# print(DatabaseManager.getInstance().searchForMusicWithMusicID("adfs"))    # None

# for member in DatabaseManager.getInstance().getRandomUnassessedMusic(None, None):
#     print(member)
# for member in DatabaseManager.getInstance().getRandomUnassessedMusic(1, None):
#     print(member)
# for member in DatabaseManager.getInstance().getRandomUnassessedMusic(None, 1):
#     print(member)
# for member in DatabaseManager.getInstance().getRandomUnassessedMusic(2, 2):
#     print(member)