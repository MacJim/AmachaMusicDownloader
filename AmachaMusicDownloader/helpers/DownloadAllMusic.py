import urllib.request
import time
import os
import sys
from .DatabaseManager import DatabaseManager


def downloadAllMusic():
    print("Starting music download!")

    musicDownloadURLs = DatabaseManager.getInstance().getAllMusicDownloadURLs()

    existingMusicOnDisk = []    # Existing music on disk.
    successfullyDownloadMusic = []
    failedToDownloadMusic = []    # Failed-to-download music.

    musicStorageDirectory = os.path.join(os.getcwd(), "music")    # Directory path without the final '/' (Unix) or '\' (Windows).
    # musicStorageDirectory = "~/Desktop/MJPlayground/Python/AmachaMusicDownloader/music"

    for downloadURL in musicDownloadURLs:
        print("\nStart downloading ", downloadURL, sep = "")

        fileName = downloadURL.split("/")[-1]
        fileStoragePath = os.path.join(musicStorageDirectory, fileName)

        # See if a file or path exists at `fileStoragePath`
        if (os.path.isdir(fileStoragePath)):
            # (Unexpected) A folder exists on disk instead of a file.
            failedToDownloadMusic.append(downloadURL)
            print("A folder exists! Failed to download: ", downloadURL, sep = "")
        elif (os.path.isfile(fileStoragePath)):
            # (Skip this piece of music) A file exists on disk.
            existingMusicOnDisk.append(downloadURL)
            print("Skipped: ", downloadURL, sep = "")
        else:
            # Download this piece of music.
            try:
                urllib.request.urlretrieve(downloadURL, fileStoragePath)
            # except urllib.request.ContentTooShortError:
            except:
                failedToDownloadMusic.append(downloadURL)
                print("Failed to download: ", downloadURL, sep = "")
            else:
                successfullyDownloadMusic.append(downloadURL)
                print("Successfully downloaded: ", downloadURL, sep = "")

            # Wait for a short period before downloading the next file. This is to reduce pressure on the target server.
            print("Waiting for 6 seconds before downloading the next file......6", end="")
            sys.stdout.flush()    # Without the flush function the print functions will be blocked by the sleep function below.
            time.sleep(1)
            print("5", end="")
            sys.stdout.flush()
            time.sleep(1)
            print("4", end="")
            sys.stdout.flush()
            time.sleep(1)
            print("3", end="")
            sys.stdout.flush()
            time.sleep(1)
            print("2", end="")
            sys.stdout.flush()
            time.sleep(1)
            print("1", end="")
            sys.stdout.flush()
            time.sleep(1)
            print("\n", end="")

    # Print download summary
    print("Music download complete!")

    if (len(existingMusicOnDisk) > 0):
        print("Existing music on disk:")
        for i in range(len(existingMusicOnDisk)):
            print(i, ". ", existingMusicOnDisk[i], sep = "")

    if (len(successfullyDownloadMusic) > 0):
        print("Successfully downloaded music:")
        for i in range(len(successfullyDownloadMusic)):
            print(i, ". ", successfullyDownloadMusic[i], sep = "")

    if (len(failedToDownloadMusic) > 0):
        print("Failed-to-download music:")
        for i in range(len(failedToDownloadMusic)):
            print(i, ". ", failedToDownloadMusic[i], sep = "")