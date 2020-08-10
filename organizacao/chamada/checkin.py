import math
from random import shuffle
from chamada.auth_data import user, password
from chamada.scrapy import scrapy_students
import pandas as pd

history_pickle = './data/history.pickle'

def get_students():
    try:
        history = pd.read_pickle(history_pickle)
    except FileNotFoundError as e:
        pass
        return None
    students = history['nome'].to_list()
    return students

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
        history = history.merge(current, on='nome', how='right')
    print(history.to_markdown())
    history.to_pickle(history_pickle)
    return students


def create_groups(students, groups, group_length):
    N = len(students)
    groups_rep = [[groups[g]] * group_length for g in range(math.ceil(N / group_length))]
    flat_groups = [item for sublist in groups_rep for item in sublist]
    flat_groups = flat_groups[:N]
    shuffle(students)
    df = pd.DataFrame(index=flat_groups, data=students)
    return df


def run():
    exclude_list = None
    groups = None

    with open('./data/exclude_list') as f:
      exclude_list = f.read().splitlines()

    with open('./data/groups') as f:
      groups = f.read().splitlines()


    current = add_checking(exclude_list)
    # students = get_students()
    df = create_groups(current, groups, 4)
    print(df.to_markdown())

run()