import scrapy
import html
import os
import re

startYear = 1986
endYear = 1995

# startCase = 13
# endCase = -5

headnoteCount = 0
writPetitionCount = 0
civilAppellateJurisdictionCount = 0
criminalAppellateJurisdictionCount = 0
originalJurisdictionCount = 0

HEADNOTE = r'HEADNOTE\s*:|HEADNOTE\s*\.'
WRIT_PETITION = r'WRIT\s*PETITION\s*:|WRIT\s*PETITION\s*\.'
CIVIL_APPELLATE_JURISDICTION = r'CIVIL\s*APPELLATE\s*JURISDICTION\s*:|CIVIL\s*APPELLATE\s*JURISDICTION\s*\.'
CRIMINAL_APPELLATE_JURISDICTION = r'CRIMINAL\s*APPELLATE\s*JURISDICTION\s*:|CRIMINAL\s*APPELLATE\s*JURISDICTION\s*\.'
ORIGINAL_JURISDICTION = r'ORIGINAL\s*JURISDICTION\s*:|ORIGINAL\s*JURISDICTION\s*\.'


class Practise(scrapy.Spider):
    name = "liiofindia"

    start_urls = [
        'http://www.liiofindia.org/in/cases/cen/INSC'
    ]

    def parse(self, response):
        # Parse the Home Page

        # Creating a directory for the data to be extracted
        try:
            os.mkdir('/home/rakshith/Academic/BTP/scrapy/extractedData')
        except OSError as error:
            print(error)

        for year in range(startYear, (endYear+1)):
            dirPath = '/home/rakshith/Academic/BTP/scrapy/extractedData/' + \
                str(year)
            try:
                os.mkdir(dirPath)
            except OSError as error:
                print(error)
            # Append the year to the URL
            yearPageURL = self.start_urls[0] + '/' + str(year)
            yield scrapy.Request(yearPageURL, callback=self.parseYear, meta={'year': year})

        print("Printing the values!")
        print(f"headnoteCount: {headnoteCount}")
        print(f"writPetitionCount: {writPetitionCount}")
        print(
            f"civilAppellateJurisdictionCount: {civilAppellateJurisdictionCount}")
        print(
            f"criminalAppellateJurisdictionCount: {criminalAppellateJurisdictionCount}")
        print(f"originalJurisdiction: {originalJurisdictionCount}")

    def parseYear(self, response):
        # Parse the page of each year
        # Response of each year
        aList = response.css('a.make-database::attr(href)').getall()

        aListSize = len(aList)
        startCase = 13
        endCase = aListSize-5

        for caseNumber in range(startCase, (endCase+1)):

            # Path of each case directory
            dirPath = '/home/rakshith/Academic/BTP/scrapy/extractedData/' + \
                str(response.meta['year']) + '/' + str((caseNumber-12))
            try:
                os.mkdir(dirPath)
            except OSError as error:
                print(error)

            # Append the case number to the URL
            casePageURL = self.start_urls[0] + '/' + \
                str(response.meta['year']) + '/' + aList[caseNumber]
            yield scrapy.Request(casePageURL, callback=self.parseCase, meta={'year': response.meta['year'], 'caseNumber': (caseNumber-12)})

    def parseCase(self, response):
        # Parse the page of each case
        responseBody = str(response.body.decode())

        # # Finding the indices to copy the text
        # headnoteIndex = responseBody.find(HEADNOTE)
        # wirtPetitionIndex = responseBody.find(WRIT_PETITION)
        # civilAppellateJurisdictionIndex = responseBody.find(
        #     CIVIL_APPELLATE_JURISDICTION)
        # criminalAppellateJurisdictionIndex = responseBody.find(
        #     CRIMINAL_APPELLATE_JURISDICTION)

        # (list(re.finditer(WRIT_PETITION, responseBody, re.IGNORECASE))[0]).start()
        headnoteIndex = -1
        wirtPetitionIndex = -1
        civilAppellateJurisdictionIndex = -1
        criminalAppellateJurisdictionIndex = -1
        originalJurisdictionIndex = -1

        # if re.finditer(HEADNOTE, responseBody, re.IGNORECASE):
        try:
            headnoteIndex = (
                list(re.finditer(HEADNOTE, responseBody, re.IGNORECASE))[0]).start()
        except:
            print("HEADNOTE not found")

        # if re.finditer(WRIT_PETITION, responseBody, re.IGNORECASE):
        try:
            wirtPetitionIndex = (
                list(re.finditer(WRIT_PETITION, responseBody, re.IGNORECASE))[0]).start()
        except:
            print("WRIT NOTE not found")

        # if re.finditer(CIVIL_APPELLATE_JURISDICTION, responseBody, re.IGNORECASE):
        try:
            civilAppellateJurisdictionIndex = (
                list(re.finditer(CIVIL_APPELLATE_JURISDICTION, responseBody, re.IGNORECASE))[0]).start()
        except:
            print("CIVIL APPELLATE JURISDICTION not found")

        # if re.finditer(CRIMINAL_APPELLATE_JURISDICTION, responseBody, re.IGNORECASE):
        try:
            criminalAppellateJurisdictionIndex = (
                list(re.finditer(CRIMINAL_APPELLATE_JURISDICTION, responseBody, re.IGNORECASE))[0]).start()
        except:
            print("CRIMINAL APPELLATE JURISDICTION not found")

        try:
            originalJurisdictionIndex = (
                list(re.finditer(ORIGINAL_JURISDICTION, responseBody, re.IGNORECASE))[0]).start()
        except:
            print("ORIGINAL JURISDICTION not found")

        endIndex = responseBody.find('LIIofIndia:')

        # Finding paths to create files to add the text into
        fileDirPath = '/home/rakshith/Academic/BTP/scrapy/extractedData/' + \
            str(response.meta['year']) + '/' + str(response.meta['caseNumber']) + '/' + str(
                response.meta['year']) + '_' + str(response.meta['caseNumber']) + '_'
        headnoteFile = fileDirPath + 'HEADNOTE'
        wirtPetitionFile = fileDirPath + 'WRIT_PETITION'
        civilAppellateJurisdictionFile = fileDirPath + 'CIVIL_APPELLATE_JURISDICTION'
        criminalAppellateJurisdictionFile = fileDirPath + \
            'CRIMINAL_APPELLATE_JURISDICTION'
        originalJurisdictionFile = fileDirPath + 'ORIGINAL_JURISDICTION'

        # Writing into seperate files
        if (headnoteIndex != -1):
            global headnoteCount
            headnoteCount += 1
            # Push the HEADNOTE into a file
            f = open(headnoteFile, 'w')
            i = headnoteIndex
            if civilAppellateJurisdictionIndex != -1:
                endIndex = civilAppellateJurisdictionIndex
            else:
                if criminalAppellateJurisdictionIndex != -1:
                    endIndex = criminalAppellateJurisdictionIndex
                else:
                    if originalJurisdictionIndex != -1:
                        endIndex = originalJurisdictionIndex
            while i < endIndex:
                # Removing html tags
                while responseBody[i] == '<':
                    while responseBody[i] != '>':
                        i += 1
                    i += 1
                f.write(responseBody[i])
                i += 1
            f.close()

        if (wirtPetitionIndex != -1):
            global writPetitionCount
            writPetitionCount += 1
            # Push the wirtPetition into a file
            f = open(wirtPetitionFile, 'w')
            i = wirtPetitionIndex
            if civilAppellateJurisdictionIndex != -1:
                endIndex = civilAppellateJurisdictionIndex
            else:
                if criminalAppellateJurisdictionIndex != -1:
                    endIndex = criminalAppellateJurisdictionIndex
            while i < endIndex:
                # Removing html tags
                while responseBody[i] == '<':
                    while responseBody[i] != '>':
                        i += 1
                    i += 1
                f.write(responseBody[i])
                i += 1
            f.close()

        if (civilAppellateJurisdictionIndex != -1):
            global civilAppellateJurisdictionCount
            civilAppellateJurisdictionCount += 1
            # Push the CIVIL APPELLATE JURISDICTION into a file
            f = open(civilAppellateJurisdictionFile, 'w')
            i = civilAppellateJurisdictionIndex
            endIndex = responseBody.find('LIIofIndia:')
            while i < endIndex:
                # Removing html tags
                while responseBody[i] == '<':
                    while responseBody[i] != '>':
                        i += 1
                    i += 1
                f.write(responseBody[i])
                i += 1
            f.close()

        if (criminalAppellateJurisdictionIndex != -1):
            global criminalAppellateJurisdictionCount
            criminalAppellateJurisdictionCount += 1
            # Push the CIVIL APPELLATE JURISDICTION into a file
            f = open(criminalAppellateJurisdictionFile, 'w')
            i = criminalAppellateJurisdictionIndex
            endIndex = responseBody.find('LIIofIndia:')
            while i < endIndex:
                # Removing html tags
                while responseBody[i] == '<':
                    while responseBody[i] != '>':
                        i += 1
                    i += 1
                f.write(responseBody[i])
                i += 1
            f.close()

        if (originalJurisdictionIndex != -1):
            global originalJurisdictionCount
            originalJurisdictionCount += 1
            # Push the CIVIL APPELLATE JURISDICTION into a file
            f = open(originalJurisdictionFile, 'w')
            i = originalJurisdictionIndex
            endIndex = responseBody.find('LIIofIndia:')
            while i < endIndex:
                # Removing html tags
                while responseBody[i] == '<':
                    while responseBody[i] != '>':
                        i += 1
                    i += 1
                f.write(responseBody[i])
                i += 1
            f.close()
