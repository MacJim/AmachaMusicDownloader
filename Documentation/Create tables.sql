-- CREATE DATABASE AmachaMusicDownloader CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- USE AmachaMusicDownloader;


-- ATTACH DATABASE 'AmachaMusicDownloader.db' as 'AmachaMusicDownloader';


CREATE TABLE Genres (
    genreID INTEGER,

    japaneseName VARCHAR(20) UNIQUE NOT NULL,

    englishName VARCHAR(40) UNIQUE NOT NULL,

    url VARCHAR(255) UNIQUE NOT NULL,


    PRIMARY KEY (genreID)
);


CREATE TABLE Images (
    imageID INTEGER,

    japaneseName VARCHAR(20) UNIQUE NOT NULL,

    englishName VARCHAR(40) UNIQUE NOT NULL,

    url VARCHAR(255) UNIQUE NOT NULL,


    PRIMARY KEY (imageID)
);


CREATE TABLE Music (
    musicID INTEGER,

    japaneseName VARCHAR(255) UNIQUE,

    englishName VARCHAR(255),

    /**
     Examples: "2018.03" / "2018.03.12"
     */
    releaseDate VARCHAR(10),

    genre1ID INTEGER,

    genre2ID INTEGER,

    image1ID INTEGER,

    image2ID INTEGER,

    /**
     Example: 2分10秒
     */
    length VARCHAR(10),

    /**
     Example: 10.23 MB
     */
    fileSize VARCHAR(10),

    instrumentsUsedJapanese TEXT,

    instrumentsUsedEnglish TEXT,

    downloadURL VARCHAR(255) UNIQUE,

    descriptionPageURL VARCHAR(255) UNIQUE NOT NULL,

    /**
     My "love level" on this piece of music.

     0 = lowest (hate); 4 = highest (love).
     */
    loveLevel TINYINT,

    /**
     My (or your) comments on this piece of music.
     */
    comments TEXT,

    /**
     ポケモンソムリエ 😂😂😂.

     Currently NOT USED.

     This is a bitwise column. 1 (true) / 0 (false).

     Bits (from lowest to highest):
     0. Whether this piece of music is suitable for game BGM.
     1. Whether this piece of music is "soothing".
     */
    -- suitability TINYINT,


    PRIMARY KEY (musicID),
    /*
     For some reasons `ON DELETE SET NULL` does not work. Is this an SQLite restriction?
     */
    FOREIGN KEY (genre1ID) REFERENCES Genres(genreID) ON DELETE SET NULL,
    FOREIGN KEY (genre2ID) REFERENCES Genres(genreID) ON DELETE SET NULL,
    FOREIGN KEY (image1ID) REFERENCES Images(imageID) ON DELETE SET NULL,
    FOREIGN KEY (image2ID) REFERENCES Images(imageID) ON DELETE SET NULL
);