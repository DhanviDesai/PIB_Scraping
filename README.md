# PIB_Scraping

Scrape PIB website of all documents on given date , month and year. These are given as command line arguments . Uses selenium and chrome headless browser. Chrome should be installed and also the executable file of chrome headless browser should be specified in the executable path.

Run : python scraping.py Date Month Year

Traverses all the links and all the available languages. Makes a directory for each year/month/date/Press_Release_Id, document is stored as Press_Release_Id[Language].txt . Corresponding parallel csv files are also produced for each month that stores the english filename and corresponding parallel language file name .
