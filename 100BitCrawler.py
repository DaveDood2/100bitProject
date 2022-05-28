# Using Selenium to run a browser's javascript code with javaa referenced from: https://stackoverflow.com/questions/63965653/how-do-i-run-command-from-web-browser-console-in-python
# and also: https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
# and also also: https://stackoverflow.com/questions/48666620/python-selenium-webdriver-stuck-at-get-in-a-loop
# And: https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-the-background

### --- Configuration settings --- ###
#Which No. the code should start/end with. Note: the No. MUST be in the history page, i.e., it should end in .html like: https://dan-ball.jp/en/javagame/bit/1.html
#STARTING_NO = 1 # Should be no smaller than 1
#ENDING_NO = 583 # At the time of writing, should be no larger than 582 (though over time as new No. are created, this will change)
#Where the code should output the crawled 100bit data
#OUTPUT_FILE = "100bitdump.xlsx"



from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import xlsxwriter
import pandas as pd
import sys

#The maximum characters that can be written in one cell of a .xlsx file
MAX_CELL_SIZE = 32767

def toGrid(grid):
    output = ""
    for i, x in enumerate(grid):
        if ((i % 256) == 0):
            output += "\n"
        if (x == 1):
            #output += u"▯"
            output += "1"
        else:
            #output += u"▮"
            output += "0"
    return output

def listToString(list, typeOfData = "default"):
    output = ""
    first = True
    previousItem = 0
    for x in list:
        # Some of the data types have leftover junk data, so I use switch case to lop it off.
        if typeOfData == "users":
            if (x == ""):
                return output
        elif typeOfData == "dotPlacements":
            if (x is None):
                return output
        elif typeOfData == "dotOwner":
            if ((x == 0) and previousItem != 0):
                return output 
        if first:
            output += str(x)
            first = False
        else:
            output += "," + str(x)
        previousItem = x
    return output

def doWBWrite(wb, row, col, data):
    if (type(data) == int):
        wb.write(row, col, data)
        return
    dataSize = len(data)
    nextRow = row
    dataWritten = 0
    while (dataSize > dataWritten):
        wb.write(nextRow, col, data[dataWritten:(dataWritten+MAX_CELL_SIZE)])
        nextRow += 1
        dataWritten += MAX_CELL_SIZE
    return

def doCrawl(OUTPUT_FILE, STARTING_NO, ENDING_NO):
    print("Crawling from", STARTING_NO, "to", ENDING_NO,"and outputting to", OUTPUT_FILE)
    '''
    NoObject = {
        "NoNumber" : 0, # What number this No. represents
        "NoDots" : 0, # x, how many dots total exist in this No.
        "users" : [], # u 
        "startingGrid": [0] * 49152, # g
        "dotPlacements" : [0] * 100100, # p 
        "dotOwner" : [0] * 100100 # aa
    }'''
    # Open the URL you want to execute JS
    currentNo = STARTING_NO
    try:
        # Writing to .xlsx files referenced from: https://stackoverflow.com/questions/25883017/xlsxwriter-and-xlwt-writing-a-list-of-strings-to-a-cell
        workbook = xlsxwriter.Workbook(OUTPUT_FILE)
        #writer = csv.writer(f)
        #writer = csv.DictWriter(f, fieldnames=header)
        # write the header
        #writer.writerow(header)
        #writer.writeheader()
        # write multiple rows
        while (currentNo <= ENDING_NO):
            print("Scanning: No. " + str(currentNo) + " (out of " + str(ENDING_NO) + ")")
            worksheet = workbook.add_worksheet("No." + str(currentNo))
            URL = 'https://dan-ball.jp/en/javagame/bit/' + str(currentNo) + '.html'
            #driver = webdriver.Chrome(chromedriver)
            ChromeOptions = webdriver.ChromeOptions()
            ChromeOptions.add_argument('--disable-browser-side-navigation')
            ChromeOptions.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=ChromeOptions)
            driver.get(URL)
            sleep(3)
            NoObject = {}
            NoObject["NoNumber"] = currentNo
            driver.execute_script("x = 30000")
            NoObject["NoDots"] = driver.execute_script("return x")
            NoObject["users"] = driver.execute_script("return u")
            NoObject["startingGrid"] = driver.execute_script("return g")
            NoObject["dotPlacements"] = driver.execute_script("return p")
            NoObject["dotOwner"] = driver.execute_script("return aa")
            #writer.writerow(data)
            #writer.writerow(NoObject)
            #worksheet.write(NoObject["NoNumber"], NoObject["NoDots"], NoObject["users"], NoObject["startingGrid"], NoObject["dotPlacements"], NoObject["dotOwner"])
            # Add header, referenced from: https://stackoverflow.com/questions/55797151/formatting-only-headers-with-data-using-xlsxwriter
            for col, data in enumerate(["No", "Dot Count", "Users", "Starting Grid", "Dot Placements", "Dot Owner"]):
                worksheet.write(0, col, data)
            doWBWrite(wb=worksheet, row=1, col=0, data=NoObject["NoNumber"])
            doWBWrite(wb=worksheet, row=1, col=1, data=NoObject["NoDots"])
            doWBWrite(wb=worksheet, row=1, col=2, data=listToString(NoObject["users"], "users"))
            doWBWrite(wb=worksheet, row=1, col=3, data=listToString(NoObject["startingGrid"], "startingGrid"))
            doWBWrite(wb=worksheet, row=1, col=4, data=listToString(NoObject["dotPlacements"], "dotPlacements"))
            doWBWrite(wb=worksheet, row=1, col=5, data=listToString(NoObject["dotOwner"], "dotOwner"))
            currentNo += 1
            driver.quit()
            
            #json.dump(NoObject, temp)
    finally:
        driver.quit()
        workbook.close()
        print("Done writing data!")


def main(args):
    OUTPUT_FILE = "newNos.xlsx"
    startNo = 584
    endNo = 585
    #wb = pd.read_excel(INPUT_FILE, sheet_name=None, header=None, names=["No", "Dot Count", "Users", "Starting Grid", "Dot Placements", "Dot Owner"])
    if len(args) >= 1:
        OUTPUT_FILE = args[0]
    if len(args) >= 2:
        startNo = int(args[1])
        endNo = int(args[1])
    if len(args) >= 3:
        endNo = int(args[2])
    doCrawl(OUTPUT_FILE, startNo, endNo)

if __name__ == "__main__":
  main(sys.argv[1:])