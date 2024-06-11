from pathlib import Path


FILE_PATH = Path(__file__).parent.joinpath("src")
FILE_PATH.mkdir(parents=False, exist_ok=True)

CSV_NAME = '/news.csv'
CHROMEDRIVER = '/chromedriver.exe'
CATEGORY_DICT = {
    '政治':1,
    '生活':5,
    '社會':6,
    '旅遊':11,
    '時尚':30,
}