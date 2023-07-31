import argparse
import datetime
import json

import pytz
import requests
from bs4 import BeautifulSoup


class TechCrunchScraper:
    """Parsers articles off of the tech crunch startups website, and returns the article content
    and metadata in memory"""

    def scrape_article_content(self, techcrunch_article_url):
        r = requests.get(techcrunch_article_url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all("h1", class_="article__title")[0].text
        article_content = soup.find_all('div', class_='article-content')[0]
        children = article_content.find_all('p')
        paragraphs = [child.text for child in children if child.text != '']
        # join paragraphs, so that we have single document
        content = '\n'.join(paragraphs)
        return {'title': title, 'content': content}

    def parse(self, from_date):
        # TODO: add logging
        page_number = 1
        articles = []
        while True:
            r = requests.get(
                f'https://techcrunch.com/wp-json/tc/v1/magazine?page={page_number}&_envelope=true&categories=20429'
            )
            data = r.json()

            for article_data in data['body']:
                article_date = pytz.utc.localize(
                    datetime.datetime.fromisoformat(article_data['date_gmt'])
                )
                if article_date < from_date:
                    return {'data': articles}
                article_url = article_data['link']
                article = {
                    'url': article_url,
                    'epoch_timestamp': article_date.timestamp(),
                }

                new_vals = self.scrape_article_content(article['url'])
                article.update(new_vals)
                articles.append(article)

            page_number += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--article_url', help='url of article to scrape', required=True)
    args = parser.parse_args()

    scraper = TechCrunchScraper()
    article = scraper.scrape_article_content(args.article_url)
    print(article)
