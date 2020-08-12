# PIB_Scraping

Scrape PIB website of all documents on given date , month and year. The required date,month and year is updated in the init function in scrap3_3.py 

sentence_extraction.py has the code for tokenization of scraped data. Tokenization in this file is carried out using a regular expression and not by calling the API endpoint for it. It also creates a csv file of all the tokenized sentences from the given file.

aligning.py is used for aligning the two parallel files. This is to be run after tokenization. It also creates a csv file of all the matched and almost matched sentences. 

The code only scraps Hindi and English parallel documents. The code scraps and generates a parallel lookup csv file in the current directory.
