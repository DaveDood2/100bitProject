import pandas as pd
import sys
import iterFunctions as iter
import numpy as np
import graphFunctions as graph
import codecs #used to print unicode characters, referenced from: https://stackoverflow.com/questions/10569438/how-to-print-unicode-character-in-python

def getPixelsByPopularity(wb, start, end, userFilter=[]):
    data = []
    firstOccurence = -1 #If using a user filter, track when the first and last No. was where the user edited in
    lastOccurence = -1
    for num in range(start, end+1):
        dotPlacements = stringToList(getNoData(wb, num, "Dot Placements"))
        if (len(userFilter) > 0):
            filteredDotPlacements = []
            users = getNoData(wb, num, "Users")
            users = [i for i in map(str, users.split(","))]
            dotOwner = stringToList(getNoData(wb, num, "Dot Owner"))
            for user in userFilter:
                if user in users:
                    for userPosition in iter.findInList(user, users):
                        print("Found", user, "in No.", num, "Position:", userPosition)
                        if (firstOccurence == -1):
                            firstOccurence = num
                        lastOccurence = num
                        try:
                            dotPosition = dotOwner.index(userPosition)
                        except ValueError:
                            #Note: there is a rare case where someone can upload to 100bit WITHOUT drawing anything.
                            #This 'continue' will trigger if that happens, and the upload without any dots drawn will be skipped.
                            continue
                        ownerNumber = dotOwner[dotPosition]
                        #ownerNumber = dotOwner[userPosition]
                        #print("Owner Num:", ownerNumber)
                        currentPos = dotPosition
                        while ((currentPos < len(dotOwner)) and (dotOwner[currentPos] == ownerNumber)):
                            #print(" Got: ", dotPlacements[currentPos], end="")
                            filteredDotPlacements.append(dotPlacements[currentPos])
                            currentPos += 1
            dotPlacements = filteredDotPlacements
            #for pixel in filteredDotPlacements:
            #    print('\tx{:<5d} y{:<5d}'.format(pixel % 256, pixel // 256))
        data += dotPlacements
        #print(df)
    if (len(data) == 0):
        sys.exit("No edits were made between No."+ str(start) + " and No." + str(end) + " with the specified user filter: " + ', '.join(userFilter))
    #print(data[0:100])
    #data = iter.flatMapSequential(data, iter.splitCommaList)
    pixel_keyvalues = iter.mapSequential(data, iter.makeKeyValue)
    #print("Pixel key", pixel_keyvalues[0:100])
    pixel_counts = iter.reduceByKeySequential(pixel_keyvalues, iter.addValues)
    #print("Pixel values: ", pixel_counts[0:100])
    pixel_counts_sorted = sorted(pixel_counts, key=lambda x: x[1], reverse=True)
    pixel_counts2D = np.zeros(shape=(192,256))
    #print(pixel_counts)
    totalCount = 0
    for pixel, count in pixel_counts:
        if (pixel == -1):
            continue
        totalCount += count
        pixel_counts2D[pixel // 256][pixel % 256] = count
    if (len(userFilter) == 0):
        graph.plotHeatMap(pixel_counts2D, title="100Bit pixels edited from No." + str(start) + " to No." + str(end))
    else:
        graph.plotHeatMap(pixel_counts2D, title="100Bit pixels edited from No." + str(firstOccurence) + " to No." + str(lastOccurence) + " for user(s): " + ', '.join(userFilter))
    print("Total pixels edited:", totalCount)
    print("Mean edits per pixel:", totalCount / (192* 256))
    print("Pixels sorted by # of times edited:")
    for pixel, count in pixel_counts_sorted[0:10]:
        if (pixel == -1):
            continue
        print('x{:<5d} y{:<5d}: {:>6d}'.format(pixel % 256, pixel // 256, count))

def getUserEditCount(wb, start, end):
    userDotCount = {}
    for num in range(start, end+1):
        #print("On no:", num)
        users = getNoData(wb, num, "Users")
        users = [i for i in map(str, users.split(","))]
        dotOwner = stringToList(getNoData(wb, num, "Dot Owner"))
        dotCountsPerUser = iter.mapSequential(dotOwner, iter.makeKeyValue)
        dotCountsPerUser = iter.reduceByKeySequential(dotCountsPerUser, iter.addValues)
        #print(dotCountsPerUser[0:100])
        for count in dotCountsPerUser:
            currentUser = users[count[0]]
            if currentUser in userDotCount:
                userDotCount[currentUser] += count[1]
            else:
                userDotCount[currentUser] = count[1]
    editCountSorted = sorted(userDotCount, key=lambda x: userDotCount[x], reverse=True)
    print("Users sorted by most edits:")
    for user in editCountSorted:
        print('{:>6d} edits from {:<30s}'.format(userDotCount[user], user))
    return

def getRatio(grid):
    #Returns a number from 0 to 1, where 0 is a completely white board, 1 is completely black.
    #data = iter.flatMapSequential(grid, iter.splitCommaList)
    data = [i for i in map(int, grid.split(','))]
    print("grid ratio:", len(data))
    return data

def editGrid(grid, edits):
    #Returns grid after pixels in edits have been toggled
    #print(edits)
    for e in edits:
        #print(e, ",", end = "")
        if (grid[e] == 1):
            grid[e] = 0
        else:
            grid[e] = 1
    return grid

def printGrid(grid):
    toPrint = ""
    for i, pixel in enumerate(grid):
        if ((i % 256) == 0):
            toPrint += "\n"
        if (pixel == 1):
            toPrint += str(1)
        elif (pixel == 0):
            toPrint += str(0)
        else:
            toPrint += "?"
    print(toPrint)

def showBlackWhiteRatio(wb, start, ending):
    data = []
    startingGrid = getNoData(wb, start, "Starting Grid")
    startingGrid = stringToList(startingGrid)
    #startingGrid = getRatio(startingGrid)
    edits = getNoData(wb, start, "Dot Placements")
    edits = stringToList(edits)
    startingGrid = editGrid(startingGrid, edits)
    nextGrid = getNoData(wb, start+1, "Starting Grid")
    nextGrid = stringToList(nextGrid)
    if(startingGrid != nextGrid):
        print("Grids aren't equal")
    else:
        print("Grids are equal!")

    #printGrid(nextGrid)
    #nextGrid = getRatio(nextGrid)

def getNoData(wb, No, col):
    #wb = The workbook object
    #No = an int representing the No. to read from (e.g., 1 for No. 1)
    #col = a string that represents which column to read from (e.g., "Dot Placements")
    #Returns a string which represents all non-empty cells under the specified column.
    NoData = wb["No." + str(No)]
    currentRow = 0
    data = ""
    #Keep reading data from a column until an empty cell is encountered
    for value in NoData[col].values:
        if ((type(value) != type("string")) and (np.isnan(value))):
            break
        data += str(value)
        currentRow += 1
    return data

def stringToList(stringThing, delimiter = ","):
    #stringThing = A string object that is separated by some delimiter (commas by default)
    #delimiter = What separates each item in the stringThing list
    data = [i for i in map(int, stringThing.split(delimiter))]
    return data

def main(args):
    startNo = 1
    endNo = 583
    INPUT_FILE = "100bitdump.xlsx"
    #wb = pd.read_excel(INPUT_FILE, sheet_name=None, header=None, names=["No", "Dot Count", "Users", "Starting Grid", "Dot Placements", "Dot Owner"])
    wb = pd.read_excel(INPUT_FILE, sheet_name=None)
    if len(args) >= 1:
        startNo = int(args[0])
        endNo = int(args[0])
    if len(args) >= 2:
        endNo = int(args[1])
    #getPixelsByPopularity(wb, startNo, endNo, ["Dave dood", "XisN"]) #
    #getPixelsByPopularity(wb, startNo, endNo, ["Dragon Archives", "dragon-master", "dragon-slayer"])
    getPixelsByPopularity(wb, startNo, endNo, ["jpicklestone"])
    #getPixelsByPopularity(wb, startNo, endNo)
    #print("arg length", len(args), "start/end:", startNo, endNo)
    #showBlackWhiteRatio(wb, startNo, endNo)
    #getUserEditCount(wb, startNo, endNo)

if __name__ == "__main__":
  main(sys.argv[1:])