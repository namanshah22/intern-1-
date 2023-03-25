# Verge Article Scraper
This is a Python script that scrapes articles from theverge.com and saves them to a CSV file and an SQLite database. The script reads the headline, link, author, and date of each article and stores them in the database.


# Usage
* Clone this repository.
* Install the dependencies using pip install -r requirements.txt.
* Run the script using python scrapper.py.
* The script will create a new CSV file with the scraped data named ddmmyyy_verge.csv.
* The script will also create an SQLite database named verge_articles.db and store the scraped data in it.
* To deduplicate the articles in the database, run python scrapper.py --deduplicate.
# Options
* --deduplicate: Remove duplicate articles from the database.
