import datetime
import math
import os
from random import shuffle
import pandas as pd
import re
from unidecode import unidecode

history_pickle = './data/history.pickle'

def get_students():
    try:
        history = pd.read_pickle(history_pickle)
    except FileNotFoundError as e:
        pass
        return None
    students = history['nome'].to_list()
    return students

def add_checking(path_file, date_str, write_pickle=False):
    try:
        history = pd.read_pickle(history_pickle)
    except FileNotFoundError as e:
        history = None
        pass
    with open(path_file, 'r') as file:
        data = file.read()
    items = data.split('resente')
    students = set()
    today = date_str

    for i in items:
        if not i or len(i) < 2:
            continue
        name_hour = unidecode(i.split('PM')[0]).replace("A\'", "o")
        name = re.findall(r'[a-zA-Z\.\s]+', name_hour)[0].strip()
        if name:
            students.add(name)

    students_dict = [{'nome': x, date_str: 'Presente'} for x in list(students)]
    # for s in students:
    #     if s['nome'] not in no_duplicates:
    #         no_duplicates.append(s['nome'])
    #         students_no_duplicates.append(s)

    if history is None:
        history = pd.DataFrame(students_dict)
    else:
        current = pd.DataFrame(students_dict)
        history = history.merge(current, on='nome', how='outer')
    print(history.to_markdown())
    if write_pickle:
        history.to_pickle(history_pickle)
    return students_dict


def create_groups(students, groups, group_length):
    N = len(students)
    groups_rep = [[groups[g]] * group_length for g in range(math.ceil(N / group_length))]
    flat_groups = [item for sublist in groups_rep for item in sublist]
    flat_groups = flat_groups[:N]
    shuffle(students)
    df = pd.DataFrame(index=flat_groups, data=students)
    return df


def run(file, date_str):

    with open('data_teste/groups') as f:
      groups = f.read().splitlines()

    current = add_checking(file, date_str, write_pickle=True)
    # current_date = list(current[0].keys())[1]
    current = [s for s in current if s[date_str] == 'Presente']
    df = create_groups(current, groups, 4)
    print(df.sort_values('nome').to_markdown())
    df.sort_values('nome', inplace=True)
    df.to_excel('./data/chamada_{0}.xlsx'.format(date_str))


def save_chamada(output_path):
    try:
        history = pd.read_pickle(history_pickle)
    except FileNotFoundError as e:
        history = None
        return
    history = history.sort_values(by='nome')
    history.to_excel(f'{output_path}/chamada.xlsx')


# print(unidecode('Antônio'))
try:
    os.remove(history_pickle)
except Exception as e:
    pass

run('data_bootcamp/chamada20201013.txt', '20201013')
run('data_bootcamp/chamada20201014.txt', '20201014')
run('data_bootcamp/chamada20201015.txt', '20201015')
run('data_bootcamp/chamada20201016.txt', '20201016')
run('data_bootcamp/chamada20201019.txt', '20201019')
run('data_bootcamp/chamada20201020.txt', '20201020')
run('data_bootcamp/chamada20201021.txt', '20201021')
run('data_bootcamp/chamada20201022.txt', '20201022')
save_chamada('data_bootcamp')
