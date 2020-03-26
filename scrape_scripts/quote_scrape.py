# Author: Jack Keane
# Date: 3/25/20
# Description: Script to scrape quotes from http://www.famousquotesandauthors.com

# Libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import string
from nltk.tokenize import sent_tokenize


# Code
quotes = urlopen("http://www.famousquotesandauthors.com/quotes_by_topic.html")
quotes_html = quotes.read()
quotes.close()

f = open("../acronym_data/quotes_data.csv", "w")

soup = bs(quotes_html, "html.parser")
soup_tr = soup.findAll("tr", {"height":"14"})   # Get list of quote topics

for topic in soup_tr:
    t_url = "http://famousquotesandauthors.com" + topic.a.get("href")

    t_quotes = urlopen(t_url)
    t_quotes_html = t_quotes.read()
    t_quotes.close()

    t_soup = bs(t_quotes_html, "html.parser")
    t_raw_quotes = t_soup.findAll("div", {"style":"font-size:12px;font-family:Arial;"})

    for quote in t_raw_quotes:
        quote_sents = sent_tokenize(quote.text)
        for s in quote_sents:
            processed_quote = s.translate(str.maketrans('', '', string.punctuation))
            f.write(processed_quote.lower().strip() + "\n")

f.close()
