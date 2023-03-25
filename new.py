import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from datetime import datetime

class VergeScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.3"}
        self.url = "https://www.theverge.com/"

    

    def save_to_csv(self, article_list):
        now = datetime.now().strftime("%d%m%Y")
        file_name = f"{now}_verge.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "url", "headline", "author", "date"])
            writer.writeheader()
            writer.writerows(article_list)

    def create_database(self):
        conn = sqlite3.connect("verge_articles.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS articles 
                          (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)""")
        conn.commit()
        conn.close()

    def save_to_database(self, article_list):
        conn = sqlite3.connect("verge_articles.db")
        cursor = conn.cursor()

        for article in article_list:
            cursor.execute("""INSERT OR IGNORE INTO articles (id, url, headline, author, date) 
                              VALUES (?, ?, ?, ?, ?)""",
                           (article["id"], article["url"], article["headline"], article["author"], article["date"]))

        conn.commit()
        conn.close()

    def deduplicate_articles(self):
        conn = sqlite3.connect("verge_articles.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS articles_temp 
                          (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)""")
        cursor.execute("""INSERT INTO articles_temp (id, url, headline, author, date)
                          SELECT id, url, headline, author, date
                          FROM articles
                          WHERE date = ?
                          GROUP BY url""",
                       (datetime.now().strftime("%Y-%m-%d"),))

        cursor.execute("""DROP TABLE articles""")
        cursor.execute("""ALTER TABLE articles_temp RENAME TO articles""")
        conn.commit()
        conn.close()

    def run(self):
        article_list = self.get_articles()
        self.save_to_csv(article_list)
        self.create_database()
        self.save_to_database(article_list)
        self.deduplicate_articles()


if __name__ == "__main__":
    scraper = VergeScraper()
    scraper.run()
