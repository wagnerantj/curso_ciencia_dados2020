import datetime
import mpu
from chamada.auth_data import user, password
from chamada.scrapy import scrapy_students
import pandas as pd

history_pickle = './data/history.pickle'


def add_checking(exclude_list):
    try:
        history = pd.read_pickle(history_pickle)
    except FileNotFoundError as e:
        history = None
        pass
    students = scrapy_students(user, password, exclude_list=exclude_list, no_window=False)
    if history is None:
        history = pd.DataFrame(students)
    else:
        current = pd.DataFrame(students)
        history = history.merge(current, on='nome')
    print(history.to_markdown())
    history.to_pickle(history_pickle)


exclude_list = None #['Slackbot', 'alexlopespereira', 'Bruno Melo', 'Erick Muzart', 'stefanomozart', 'vronks']
with open('./data/exclude_list') as f:
  exclude_list = f.read().splitlines()

add_checking(exclude_list)
