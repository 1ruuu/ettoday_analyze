"""

"""
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from crawler import settings
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import emoji
import re


class ETtoday:
    """
    A class to CrawlerETtoday

    Methods
    -------
    get_article()
        get news Article
    get_info()
        get news Title, Url
    """

    def get_article(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.select("div.story", itemprop="articleBody")
        title_list = []

        for articles in article:
            try:
                target = articles.find_all("strong")

                for child in target:
                    child.decompose()

                for content in articles.select("p"):
                    title_list.append(content.text)

                final_article = ''.join(title_list).replace('\r', '').replace('\n', '').replace(' ', '')
                result = emoji.replace_emoji(final_article, replace="")
                return result

            except Exception:
                result = None
                return result


    def get_info(self, 
                 category:str=None,
                 date_list:list=[],
                 get_article:bool=False):

        result = list()
        category_id = settings.CATEGORY_DICT[category]
        browser = webdriver.Chrome()
        browser.get(f"https://www.ettoday.net/news/news-list-{date_list[0]}-{category_id}.htm")
        browser.implicitly_wait(10)

        for count in range(len(date_list)):
            current_date = datetime.strptime(date_list[count], '%Y-%m-%d')
            current_month = re.sub(r'^0', '', current_date.strftime("%m"))
            current_day = re.sub(r'^0', '', current_date.strftime("%d"))
            start_time = datetime.strptime(current_date.strftime("%Y/%m/%d") + ' 0', '%Y/%m/%d %H')
            end_time = datetime.strptime(current_date.strftime("%Y/%m/%d") + ' 23', '%Y/%m/%d %H')

            select_month = Select(browser.find_element(By.ID, "selM"))
            select_month.select_by_value(current_month)

            select_day = Select(browser.find_element(By.ID, "selD"))
            select_day.select_by_value(current_day) 

            browser.find_element(By.ID, 'button').click()

            is_scroll = True

            while is_scroll:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "lxml")

                for article_date in soup.find(class_="part_list_2").find_all('h3'):
                    if datetime.strptime(article_date.find_all(class_="date")[-1].text, '%Y/%m/%d %H:%M') < end_time:
                        is_scroll = False
                        break
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "lxml")
                for a in soup.find(class_="part_list_2").find_all('h3'):
                    target_time = datetime.strptime(a.find(class_="date").text, '%Y/%m/%d %H:%M')
                    if start_time < target_time < end_time:
                        post_url = a.find_all('a')[-1]["href"]
                        title  = a.find_all('a')[-1].text
                        date =  a.find_all('span')[-1].text.split(' ')[0]
                        if get_article:
                            article = self.get_article(post_url)
                            if article:
                                news = {
                                    "TITLE": title,
                                    "ARTICLE": article,
                                    "SOURCE": "ETtoday",
                                    "POST_URL": post_url,
                                    "POST_DATE": date
                                }
                                result.append(news)
                        else:
                            news = {
                                    "TITLE": title,
                                    "SOURCE": "ETtoday",
                                    "POST_URL": post_url,
                                    "POST_DATE": date
                                }
                            result.append(news)

        browser.quit()
        df = pd.DataFrame(result)
        df.to_csv(str(settings.FILE_PATH) + settings.CSV_NAME, index=False, encoding='utf-8-sig')