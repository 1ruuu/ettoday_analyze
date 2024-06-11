from crawler.ettoday_crawler import ETtoday
from crawler.save_database import SaveDB
from datetime import datetime, timedelta
from crawler import settings
from dotenv import load_dotenv
import os

class Tools:
    """
    A class to Tools

    Methods
    -------
    get_news_info()
        Get ETtoday news
    save_to_database()
        Save to BigQuery DB
    """

    def __init__(self) -> None:

        self.news_tools = ETtoday()
        self.save_db = SaveDB()

    def get_news_info(self,
                      category: str='旅遊',
                      start_date: str='2024-05-01',
                      end_date: str='2024-05-03',
                      get_article: bool=False,
                      ):
        """
            Methods
            -------
            category:Str
                Select one of the categories: 政治,生活,社會,旅遊,時尚
            start_date:Str
                input start_date 'yyyy-mm-dd' e.g.'2024-05-01'
            end_date:Str
                input end_date 'yyyy-mm-dd' e.g.'2024-05-03'
            get_article:Bool
                if get article please input True, else input Flase
            """
        
        
        if category not in settings.CATEGORY_DICT:
            return('There is no such category. Please enter it again.')
        if end_date<start_date:
            return('End date is earlier than start date, please enter again.')

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        date_list = []
        current_date = start
        while current_date <= end:
            date_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        if len(date_list)>7:
            return('Too many days selected, the upper limit is 7 days')

        return self.news_tools.get_info(category, date_list, get_article)
    

    def save_to_database(self,
                         bq_json: str=None,
                         db_name: str=None,
                         table_name: str=None, 
                         file: str=None):
        """
            Methods
            -------
            bq_file:Str
                BigQuery Auth json file
            db_name:Str
                BQ Database name
            table_name:Str
                BQ Table name
            file:Str
                csv file to be inserted
            """
        
        is_env = load_dotenv()
        bq_json =  str(settings.FILE_PATH) + '/' + os.getenv('BIGQ_JSON') if is_env else bq_json
        db = os.getenv('DATASET_NAME') if is_env else db_name
        table = os.getenv('TABLE_NAME') if is_env else table_name
        file = str(settings.FILE_PATH) + '/' + settings.CSV_NAME if os.path.exists(str(settings.FILE_PATH) + '/' + settings.CSV_NAME) else file
        
        return self.save_db.save_data(bq_json, db, table, file)        


        